from core.brain import Brain
from speech.tts import TTS
from speech.stt import STT
from tools.system import execute_command

class Assistant:

    def __init__(self):
        
        self.brain=Brain()
        self.stt=None
        self.tts=None
    
    def process_response(self,user_input):

        print("JARVIS: ",end="")

        full_reply=[]

        for chunk in self.brain.get_response(user_input):

            print(chunk,end="",flush=True)

            full_reply.append(chunk)

        print()

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
            
            tool_response=execute_command(user_input)

            if tool_response:
                print(f"JARVIS: {tool_response}")
                continue
            
            self.process_response(user_input)
    
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

            tool_response = execute_command(user_input)

            if tool_response:

                print(f"JARVIS: {tool_response}")

                self.tts.speak(tool_response)

                continue

            reply=self.process_response(user_input)
            
            self.tts.speak(reply)
