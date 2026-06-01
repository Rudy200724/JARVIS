from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from config import elevenlabs_key

class TTS:
    def __init__(self):
        
        self.client=ElevenLabs(api_key=elevenlabs_key)
        self.voice_id="JBFqnCBsd6RMkjVDRZzb"
        self.model_id= "eleven_flash_v2_5"
        self.output_format="mp3_44100_128"
    
    def speak(self,text):

        try:
            audio=self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format=self.output_format,
            )
            stream(audio)
        
        except Exception as e:
            print(f"TTS Error:{e}")