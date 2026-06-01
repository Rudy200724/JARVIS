from openai import OpenAI
from config import openrouter_key,MODELS,messages

class Brain:

    def __init__(self):

            self.client=OpenAI(
                  api_key=openrouter_key,
                  base_url="https://openrouter.ai/api/v1",               
            )

            self.models=MODELS
            self.current_model=0
            self.messages=messages.copy()
            self.total_tokens=0
            self.failed_attempts={}
    
    def switch_model(self):
          
          self.current_model=(self.current_model+1) % len(self.models)

    def get_response(self,user_input):
          
        self.messages.append({
                
                "role":"user",
                "content":user_input
          })
        
        for _ in range(len(self.models)):

            try:
                response=self.client.chat.completions.create(
                model=self.models[self.current_model],
                messages=self.messages,
                stream=True,
                stream_options={"include_usage":True},
                )

                full_response=[]

                for chunk in response:
                     
                    if chunk.choices:   
                        delta=chunk.choices[0].delta.content

                        if delta:
                            full_response.append(delta)

                            yield delta
                    
                    if hasattr(chunk,"usage") and chunk.usage:
                         
                         self.total_tokens+=chunk.usage.total_tokens
        
                reply="".join(full_response)

                self.messages.append({
                    "role": "assistant",
                    "content": reply
                })

                return

            except Exception as e:
                
                print(f"Model {self.models[self.current_model]} failed:")
                print(f"{e},\nSwitching model")
                
                self.switch_model()
        
        yield "All models failed, Sir."