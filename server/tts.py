import pyttsx3


class TextToSpeech:

    def speak(self, text):

        print(f"\nJarvis: {text}\n")

        engine = pyttsx3.init()

        engine.setProperty('rate', 170)

        engine.say(text)

        engine.runAndWait()

        engine.stop()