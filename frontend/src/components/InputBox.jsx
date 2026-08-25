import { useRef } from "react";
import {
    Paperclip,
    Image,
    Mic,
    Send
} from "lucide-react";


function InputBox({
    message,
    setMessage,
    handleSend,
    isLoading
}) {

    const fileInputRef = useRef(null);


    function handleAttachment() {

        fileInputRef.current?.click();

    }


    function handleFileChange(event) {

        const files = event.target.files;

        if (!files || files.length === 0) {
            return;
        }

        console.log(
            "Selected files:",
            files
        );

        /*
         * File uploading will be connected
         * to the backend later.
         */
    }


    function handleVoiceClick() {

        /*
         * Voice mode will be connected
         * to the STT backend later.
         */

        console.log("Voice mode clicked");

    }


    return (

        <div className="input-area">

            <div className="input-box">


                <div className="input-actions-left">

                    <button
                        className="input-action"
                        type="button"
                        onClick={handleAttachment}
                        title="Attach file"
                    >
                        <Paperclip/>
                    </button>


                    <button
                        className="input-action"
                        type="button"
                        onClick={handleAttachment}
                        title="Add media"
                    >
                        <Image/>
                    </button>


                    <button
                        className="input-action"
                        type="button"
                        onClick={handleVoiceClick}
                        title="Voice mode"
                    >
                        <Mic/>
                    </button>

                </div>


                <input
                    ref={fileInputRef}

                    type="file"

                    className="hidden-file-input"

                    multiple

                    accept="
                        image/*,
                        audio/*,
                        video/*,
                        .pdf,
                        .txt,
                        .doc,
                        .docx,
                        .csv,
                        .json
                    "

                    onChange={handleFileChange}
                />


                <div className="input-divider"></div>


                <input
                    type="text"

                    className="input-message"

                    placeholder="Type a message..."

                    value={message}

                    onChange={(event) =>
                        setMessage(event.target.value)
                    }

                    onKeyDown={(event) => {

                        if (
                            event.key === "Enter" &&
                            !event.shiftKey &&
                            !isLoading
                        ) {
                            event.preventDefault();

                            handleSend();
                        }

                    }}

                    disabled={isLoading}
                />


                <button
                    className="send-button"
                    onClick={handleSend}
                    disabled={
                        isLoading ||
                        !message.trim()
                    }

                    title="Send message"
                >

                    <Send className="send-icon"/>

                </button>

            </div>

        </div>
    );
}


export default InputBox;