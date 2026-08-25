import { useState } from "react";

import Header from "./components/Header"
import ChatWindow from "./components/ChatWindow"
import InputBox from "./components/InputBox"

function App(){

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

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: message
      })
    });

    if (!response.ok) {
      throw new Error("Server error");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let fullResponse = "";
    let jarvisMessageCreated = false;

    while (true) {

      const { value, done } = await reader.read();

      if (done) {
        break;
      }

      const chunk = decoder.decode(value, {
        stream: true
      });

      fullResponse += chunk;

      if (!jarvisMessageCreated) {

        setMessages((previousMessages) => [
          ...previousMessages,
          {
            text: fullResponse,
            sender: "jarvis"
          }
        ]);

        jarvisMessageCreated = true;

      } else {
        setMessages((previousMessages) => {

          const updatedMessages = [...previousMessages];

          updatedMessages[updatedMessages.length - 1] = {
            text: fullResponse,
            sender: "jarvis"
          };

          return updatedMessages;
        });
      }
    }

  } catch (error) {

    console.error("Error connecting to JARVIS:", error);

    setError("JARVIS is currently unavailable.");

  } finally {

    setIsLoading(false);

  }
}

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <div className="app">
    <Header/>
    <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}

    />
    <InputBox
          message={message}
          setMessage={setMessage}
          handleSend={handleSend}
          isLoading={isLoading}
    />
    </div>
  );
}

export default App;