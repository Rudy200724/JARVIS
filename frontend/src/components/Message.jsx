
function Message({sender, text}){
    return (
        <div className={`message ${sender ==="JARVIS" ? "jarvis-message":"user-message"}`}>
            <p>{text}</p>
        </div>
    );
}
export default Message;