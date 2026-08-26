import { useEffect, useState } from "react";
import {
    MessageSquare,
    Brain,
    Code2,
    Activity,
    Box,
    Settings,
    Menu,
    X
}
from "lucide-react";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import Login from "./components/login";

const API_URL = import.meta.env.VITE_API_URL;

function Sidebar({
    onLogout,
    collapsed,
    mobileOpen,
    onClose
}) {

    return (
        <>
            <div
                className={`sidebar-overlay ${
                    mobileOpen ? "visible" : ""
                }`}
                onClick={onClose}
            />

            <aside
                className={`sidebar
                    ${collapsed ? "collapsed" : ""}
                    ${mobileOpen ? "mobile-open" : ""}
                `}
            >

                <div className="sidebar-brand">

                    <div className="core-logo">
                        <div className="core-logo-inner"></div>
                    </div>

                    <div className="sidebar-brand-name">
                        J.A.R.V.I.S
                    </div>

                    <div className="sidebar-brand-subtitle">
                        COMMAND CENTER
                    </div>

                    <button
                        className="sidebar-mobile-close"
                        onClick={onClose}
                        aria-label="Close navigation"
                    >
                        <X />
                    </button>

                </div>


                <nav className="sidebar-nav">

                    <button className="nav-item active">
                        <span className="nav-icon">
                            <MessageSquare />
                        </span>
                        <span>CHAT</span>
                    </button>

                    <button className="nav-item">
                        <span className="nav-icon">
                            <Brain />
                        </span>
                        <span>MEMORY</span>
                    </button>

                    <button className="nav-item">
                        <span className="nav-icon">
                            <Code2 />
                        </span>
                        <span>CODE</span>
                    </button>

                    <button className="nav-item">
                        <span className="nav-icon">
                            <Activity />
                        </span>
                        <span>SYSTEM</span>
                    </button>

                    <button className="nav-item">
                        <span className="nav-icon">
                            <Box />
                        </span>
                        <span>TOOLS</span>
                    </button>

                </nav>


                <div className="sidebar-bottom">

                    <button className="nav-item">

                        <span className="nav-icon">
                            <Settings />
                        </span>

                        <span>SETTINGS</span>

                    </button>

                    <button
                        className="nav-item"
                        onClick={onLogout}
                    >
                        <span className="nav-icon">
                            <X />
                        </span>

                        <span>LOGOUT</span>
                    </button>

                </div>

            </aside>
        </>
    );
}

function App() {

    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [authChecking, setAuthChecking] = useState(true);

    const [sidebarCollapsed, setSidebarCollapsed] =useState(false);
    const [mobileSidebarOpen, setMobileSidebarOpen] =useState(false);

    useEffect(() => {

    async function checkAuthentication() {

        try {

            const response = await fetch(
                `${API_URL}/auth/me`,
                {
                    credentials: "include"
                }
            );

            if (response.ok) {

                setIsAuthenticated(true);

            } else {

                setIsAuthenticated(false);

            }

        } catch (error) {

            console.error(
                "Authentication check failed:",
                error
            );

            setIsAuthenticated(false);

        } finally {

            setAuthChecking(false);

        }
    }

    checkAuthentication();

    }, []);

    function handleLogin() {

        setIsAuthenticated(true);
    }

    async function handleLogout() {

    try {

        await fetch(
            `${API_URL}/auth/logout`,
            {
                method: "POST",
                credentials: "include"
            }
        );

    } finally {

        setIsAuthenticated(false);

    }
}

    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");


    async function handleSend() {

        if (!message.trim()) {
            return;
        }

        setError("");
        setIsLoading(true);

        const newMessage = {
            text: message,
            sender: "user"
        };

        setMessages((previousMessages) => [
            ...previousMessages,
            newMessage
        ]);

        setMessage("");

        try {

            const response = await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    credentials: "include",

                    headers: {
                        "Content-Type": "application/json",
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );

            if (!response.ok) {
                throw new Error("Server error");
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let fullResponse = "";
            let jarvisMessageCreated = false;

            while (true) {

                const { value, done } =
                    await reader.read();

                if (done) {
                    break;
                }

                const chunk = decoder.decode(
                    value,
                    {
                        stream: true
                    }
                );

                fullResponse += chunk;

                if (!jarvisMessageCreated) {

                    setMessages(
                        (previousMessages) => [
                            ...previousMessages,
                            {
                                text: fullResponse,
                                sender: "jarvis"
                            }
                        ]
                    );

                    jarvisMessageCreated = true;

                } else {

                    setMessages(
                        (previousMessages) => {

                            const updatedMessages = [
                                ...previousMessages
                            ];

                            updatedMessages[
                                updatedMessages.length - 1
                            ] = {
                                text: fullResponse,
                                sender: "jarvis"
                            };

                            return updatedMessages;
                        }
                    );
                }
            }

        } catch (error) {

            console.error(
                "Error connecting to JARVIS:",
                error
            );

            setError(
                "JARVIS is currently unavailable."
            );

        } finally {

            setIsLoading(false);

        }
    }

    if (authChecking){
        return null;
    }

    if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
    }

    return (

        <div className="app">

            <div className="ambient-glow"></div>

            <button
                className="sidebar-toggle"
                onClick={() => setSidebarCollapsed(previous => !previous)}
                aria-label={
                    sidebarCollapsed
                        ? "Expand sidebar"
                        : "Collapse sidebar"
                }
            >
                <Menu />
            </button>

            <Sidebar
            onLogout={handleLogout}
            collapsed={sidebarCollapsed}
            mobileOpen={mobileSidebarOpen}
            onClose={() => setMobileSidebarOpen(false)}
            />


            <main className="main-area">

                <button
                    className="mobile-menu-button"
                    onClick={() => setMobileSidebarOpen(true)}
                    aria-label="Open navigation"
                >
                    <Menu />
                </button>

                <div className="main-panel">

                    <Header />


                    <section className="chat-container">

                        <ChatWindow
                            messages={messages}
                            isLoading={isLoading}
                            error={error}
                        />

                    </section>


                    <InputBox
                        message={message}
                        setMessage={setMessage}
                        handleSend={handleSend}
                        isLoading={isLoading}
                    />


                    <div className="system-status">

                        <span className="status-dot"></span>

                        <span>
                            SYSTEM STATUS:
                            <strong> OPTIMAL</strong>
                        </span>

                        <span className="status-divider">
                            |
                        </span>

                        <span>
                            MEMORY:
                            <strong> READY</strong>
                        </span>

                        <span className="status-divider">
                            |
                        </span>

                        <span>
                            CORE:
                            <strong> ONLINE</strong>
                        </span>

                    </div>

                </div>

            </main>

        </div>
    );
}


export default App;