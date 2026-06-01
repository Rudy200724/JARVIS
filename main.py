from core.assistant import Assistant

def main():
    assistant=Assistant()

    try:
        while True:
            mode=input("Choose mode (text/audio): ").lower()

            if mode=="text":

                assistant.run_text_mode()
                break

            elif mode=="audio":

                assistant.run_audio_mode()
                break

            else:
                print("Invalid mode.")
    
    finally:
        assistant.shutdown()

if __name__=="__main__":
    main()
