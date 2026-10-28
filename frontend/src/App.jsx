import { useEffect, useState } from "react";

import {
    MessageSquare,
    Brain,
    Code2,
    Activity,
    Box,
    Settings,
    Menu,
    X,
    LogOut
} from "lucide-react";

import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import Login from "./components/login";


const API_URL = import.meta.env.VITE_API_URL;


/* =========================================================
   SIDEBAR
   ========================================================= */

function Sidebar({
    onLogout,
    collapsed,
    mobileOpen,
    onClose
}) {

    return (
        <>
            {/* Mobile overlay */}

            <div
                className={`sidebar-overlay ${
                    mobileOpen ? "visible" : ""
                }`}
                onClick={onClose}
            />


            {/* Sidebar */}

            <aside
                className={`sidebar
                    ${collapsed ? "collapsed" : ""}
                    ${mobileOpen ? "mobile-open" : ""}
                `}
            >

                {/* -------------------------------------------------
                   BRAND
                   ------------------------------------------------- */}

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


                    {/* Mobile close button */}

                    <button
                        className="sidebar-mobile-close"
                        onClick={onClose}
                        aria-label="Close navigation"
                    >
                        <X />
                    </button>

                </div>


                {/* -------------------------------------------------
                   NAVIGATION
                   ------------------------------------------------- */}

                <nav className="sidebar-nav">

                    <button className="nav-item active">

                        <span className="nav-icon">
                            <MessageSquare />
                        </span>

                        <span>
                            CHAT
                        </span>

                    </button>


                    <button className="nav-item">

                        <span className="nav-icon">
                            <Brain />
                        </span>

                        <span>
                            MEMORY
                        </span>

                    </button>


                    <button className="nav-item">

                        <span className="nav-icon">
                            <Code2 />
                        </span>

                        <span>
                            CODE
                        </span>

                    </button>


                    <button className="nav-item">

                        <span className="nav-icon">
                            <Activity />
                        </span>

                        <span>
                            SYSTEM
                        </span>

                    </button>


                    <button className="nav-item">

                        <span className="nav-icon">
                            <Box />
                        </span>

                        <span>
                            TOOLS
                        </span>

                    </button>

                </nav>


                {/* -------------------------------------------------
                   SIDEBAR BOTTOM
                   ------------------------------------------------- */}

                <div className="sidebar-bottom">

                    <button className="nav-item">

                        <span className="nav-icon">
                            <Settings />
                        </span>

                        <span>
                            SETTINGS
                        </span>

                    </button>


                    <button
                        className="nav-item"
                        onClick={onLogout}
                    >

                        <span className="nav-icon">
                            <LogOut />
                        </span>

                        <span>
                            LOGOUT
                        </span>

                    </button>

                </div>

            </aside>
        </>
    );
}


/* =========================================================
   APP
   ========================================================= */

function App() {

    /* ---------------------------------------------------------
       AUTHENTICATION
       --------------------------------------------------------- */

    const [isAuthenticated, setIsAuthenticated] =
        useState(false);

    const [authChecking, setAuthChecking] =
        useState(true);


    /* ---------------------------------------------------------
       SIDEBAR STATE
       --------------------------------------------------------- */

    const [sidebarCollapsed, setSidebarCollapsed] =
        useState(
            () =>
                localStorage.getItem(
                    "jarvis_sidebar_collapsed"
                ) === "true"
        );


    const [mobileSidebarOpen, setMobileSidebarOpen] =
        useState(false);


    /* ---------------------------------------------------------
       CHECK AUTHENTICATION
       --------------------------------------------------------- */

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


    /* ---------------------------------------------------------
       LOGIN
       --------------------------------------------------------- */

    function handleLogin() {

        setIsAuthenticated(true);

    }


    /* ---------------------------------------------------------
       LOGOUT
       --------------------------------------------------------- */

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


    /* ---------------------------------------------------------
       SIDEBAR TOGGLE
       --------------------------------------------------------- */

    function toggleSidebar() {

        setSidebarCollapsed(previous => {

            const next = !previous;

            localStorage.setItem(
                "jarvis_sidebar_collapsed",
                String(next)
            );

            return next;

        });

    }


    /* ---------------------------------------------------------
       CHAT STATE
       --------------------------------------------------------- */

    const [message, setMessage] =
        useState("");

    const [messages, setMessages] =
        useState([]);

    const [isLoading, setIsLoading] =
        useState(false);

    const [error, setError] =
        useState("");


    /* ---------------------------------------------------------
       SEND MESSAGE
       --------------------------------------------------------- */

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


        setMessages(
            previousMessages => [
                ...previousMessages,
                newMessage
            ]
        );


        setMessage("");


        try {

            const response = await fetch(
                `${API_URL}/chat`,
                {
                    method: "POST",

                    credentials: "include",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


            if (!response.ok) {

                throw new Error(
                    "Server error"
                );

            }


            const reader =
                response.body.getReader();

            const decoder =
                new TextDecoder();


            let fullResponse = "";

            let jarvisMessageCreated =
                false;


            while (true) {

                const {
                    value,
                    done
                } = await reader.read();


                if (done) {

                    break;

                }


                const chunk =
                    decoder.decode(
                        value,
                        {
                            stream: true
                        }
                    );


                fullResponse += chunk;


                if (!jarvisMessageCreated) {

                    setMessages(
                        previousMessages => [
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
                        previousMessages => {

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


    /* ---------------------------------------------------------
       AUTH CHECK LOADING
       --------------------------------------------------------- */

    if (authChecking) {

        return null;

    }


    /* ---------------------------------------------------------
       LOGIN PAGE
       --------------------------------------------------------- */

    if (!isAuthenticated) {

        return (
            <Login
                onLogin={handleLogin}
            />
        );

    }


    /* ---------------------------------------------------------
       MAIN APPLICATION
       --------------------------------------------------------- */

    return (

        <div
            className={`app ${
                sidebarCollapsed
                    ? "sidebar-collapsed"
                    : ""
            }`}
        >

            <div className="ambient-glow"></div>


            {/* -------------------------------------------------
               DESKTOP SIDEBAR TOGGLE
               ------------------------------------------------- */}

            <button
                className="sidebar-toggle"
                onClick={toggleSidebar}
                aria-label={
                    sidebarCollapsed
                        ? "Expand sidebar"
                        : "Collapse sidebar"
                }
            >

                <Menu />

            </button>


            {/* -------------------------------------------------
               SIDEBAR
               ------------------------------------------------- */}

            <Sidebar
                onLogout={handleLogout}
                collapsed={sidebarCollapsed}
                mobileOpen={mobileSidebarOpen}
                onClose={() =>
                    setMobileSidebarOpen(false)
                }
            />


            {/* -------------------------------------------------
               MAIN AREA
               ------------------------------------------------- */}

            <main className="main-area">

                {/* Mobile hamburger */}

                <button
                    className="mobile-menu-button"
                    onClick={() =>
                        setMobileSidebarOpen(true)
                    }
                    aria-label="Open navigation"
                >

                    <Menu />

                </button>


                <div className="main-panel">

                    <Header />


                    {/* -------------------------------------------------
                       CHAT
                       ------------------------------------------------- */}

                    <section className="chat-container">

                        <ChatWindow
                            messages={messages}
                            isLoading={isLoading}
                            error={error}
                        />

                    </section>


                    {/* -------------------------------------------------
                       INPUT
                       ------------------------------------------------- */}

                    <InputBox
                        message={message}
                        setMessage={setMessage}
                        handleSend={handleSend}
                        isLoading={isLoading}
                    />


                    {/* -------------------------------------------------
                       SYSTEM STATUS
                       ------------------------------------------------- */}

                    <div className="system-status">

                        <span className="status-dot"></span>


                        <span>
                            SYSTEM STATUS:
                            <strong>
                                {" "}OPTIMAL
                            </strong>
                        </span>


                        <span className="status-divider">
                            |
                        </span>


                        <span>
                            MEMORY:
                            <strong>
                                {" "}READY
                            </strong>
                        </span>


                        <span className="status-divider">
                            |
                        </span>


                        <span>
                            CORE:
                            <strong>
                                {" "}ONLINE
                            </strong>
                        </span>

                    </div>

                </div>

            </main>

        </div>

    );

}


export default App;