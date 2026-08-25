import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function CodeBlock({ className, children }) {

    const [copied, setCopied] = useState(false);

    const code = String(children).replace(/\n$/, "");

    const language = className
        ? className.replace("language-", "")
        : "";

    async function handleCopy() {

        await navigator.clipboard.writeText(code);

        setCopied(true);

        setTimeout(() => {
            setCopied(false);
        }, 1500);
    }

    return (
        <div className="jarvis-code-block">

            <div className="jarvis-code-header">

                <span className="jarvis-code-language">
                    {language || "code"}
                </span>

                <button
                    className="copy-button"
                    onClick={handleCopy}
                >
                    {copied ? "Copied ✓" : "Copy"}
                </button>

            </div>

            <pre>
                <code className={className}>
                    {children}
                </code>
            </pre>

        </div>
    );
}

function ChatWindow({ messages, isLoading, error }) {

    const bottomRef = useRef(null);
    const chatWindowRef = useRef(null);
    const shouldAutoScroll = useRef(true);
    const [showScrollButton, setShowScrollButton] = useState(false);

    function scrollToBottom() {

    shouldAutoScroll.current = true;

    bottomRef.current?.scrollIntoView({
        behavior: "smooth"
    });

    setShowScrollButton(false);
    }


    useEffect(() => {

        const chatWindow = chatWindowRef.current;

        if (!chatWindow) {
            return;
        }

        function handleScroll() {

            const distanceFromBottom =
                chatWindow.scrollHeight -
                chatWindow.scrollTop -
                chatWindow.clientHeight;   

            const atBottom = distanceFromBottom <= 50;
            shouldAutoScroll.current = atBottom;

            setShowScrollButton(!atBottom);
        }
 

        chatWindow.addEventListener(
            "scroll",
            handleScroll
        );


        return () => {

            chatWindow.removeEventListener(
                "scroll",
                handleScroll
            );

        };

    }, []);


    useEffect(() => {

        if (!shouldAutoScroll.current) {
            return;
        }

        bottomRef.current?.scrollIntoView({
            behavior: "auto"
        });

    }, [messages, isLoading]);


    return (

        <div
            className="chat-window"
            ref={chatWindowRef}
        >

            {messages.map((message, index) => (

                <div
                    key={index}
                    className={`message ${
                        message.sender === "user"
                            ? "user-message"
                            : "jarvis-message"
                    }`}
                >

                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}

                        components={{

                            code({ className, children }) {

                                const isCodeBlock =
                                    className?.startsWith(
                                        "language-"
                                    );


                                if (isCodeBlock) {

                                    return (

                                        <CodeBlock
                                            className={className}
                                        >
                                            {children}
                                        </CodeBlock>

                                    );

                                }


                                return (

                                    <code className={className}>
                                        {children}
                                    </code>

                                );

                            }

                        }}
                    >

                        {message.text}

                    </ReactMarkdown>

                </div>

            ))}


            {isLoading && (

                <div className="jarvis-thinking">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>

            )}


            {error && (

                <div className="jarvis-error">
                    {error}
                </div>

            )}

            {showScrollButton &&(
                <button
                    className="scroll-to-bottom"
                    onClick={scrollToBottom}
                >
                    ↓ New messages
                </button>
            )}

            {/* Invisible element used as the scroll target */}

            <div ref={bottomRef} />

        </div>

    );
}


export default ChatWindow;