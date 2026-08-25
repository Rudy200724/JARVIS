
function InputBox({message, setMessage, handleSend, isLoading}){

    return (
        <div className="input-box">

        <input 
            type="text"
            className="input-message"
            placeholder="Type a message..."
            value={message}
            onChange={(e)=> setMessage(e.target.value)}
            onKeyDown={(e)=> e.key === "Enter" && !isLoading? handleSend():null}

        />
        <button
            className="send-button"
            onClick={handleSend}
            disabled={isLoading}
        >
            ➤
        </button>
        </div>
    );
}
export default InputBox