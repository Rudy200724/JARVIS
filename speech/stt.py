from RealtimeSTT import AudioToTextRecorder

class STT:

    def __init__(self):
        
        self.recorder= AudioToTextRecorder(
            model="base.en",
            language="en",
            spinner=False,
            compute_type="float32",
        )
    
    def listen(self):

        return self.recorder.text()
    
    def shutdown(self):
        self.recorder.shutdown()