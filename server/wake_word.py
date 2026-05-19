import speech_recognition as sr


class WakeWordDetector:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone()


    def listen_for_wake_word(self):

        print("\nListening for wake word...\n")

        while True:

            with self.microphone as source:

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(source)

            try:

                text = self.recognizer.recognize_google(
                    audio
                ).lower()

                print(f"Heard: {text}")

                if "jarvis" in text:

                    print("\nWake word detected!\n")

                    return True

            except Exception:

                pass