from core.brain import Brain
from speech.tts import TTS
from speech.stt import STT
from tools.system import execute_command

class Assistant:

    def __init__(self):
        
        self.brain=Brain()
        self.stt=None
        self.tts=None
    
    def generate_response(self,user_input:str)->str:

        full_reply=[]

        for chunk in self.brain.get_response(user_input):

            full_reply.append(chunk)

        return "".join(full_reply)
    
    def shutdown(self):
        try:
            if self.stt:
                self.stt.shutdown()

        except Exception as e:
            print(f"Shutdown Error: {e}")
    
    def run_text_mode(self):

        while True:

            user_input=input("You: ")
            
            if user_input.lower() in ["exit","shutdown","quit"]:
                break

            reply = self.chat(user_input)

            print(f"JARVIS: {reply}")
    
    def run_audio_mode(self):

        self.stt=STT()
        self.tts=TTS()

        while True:
            
            print("Listening....")

            user_input=self.stt.listen()

            if not user_input:
                continue
            
            if user_input.lower() in ["exit.","shut down.","quit."]:
                break

            print(f"You: {user_input}")

            reply=self.chat(user_input)

            print(f"JARVIS: {reply}")
            
            self.tts.speak(reply)

    def chat(self,user_input:str)->str:

        tool_response = execute_command(user_input)

        if tool_response:
            return tool_response

        return self.generate_response(user_input)
