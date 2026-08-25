import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import Message from "./Message";

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

function ChatWindow({messages, isLoading, error}){

    const bottomRef =useRef(null);

    useEffect(() => {
    bottomRef.current?.scrollIntoView({
        behavior: "smooth"
        });
    }, [messages, isLoading]);

    return (
        <div className="chat-window">
            {messages.map((message, index) => (
                <div
                    key={index}
                    className={`message ${message.sender ==="user" ? "user-message": "jarvis-message"}`}
                >
                    <ReactMarkdown
    remarkPlugins={[remarkGfm]}
    components={{
        code({ className, children }) {
            
            const isCodeBlock = className?.startsWith("language-");

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
            <div ref={bottomRef}/>
        </div>
    );
}
export default ChatWindow