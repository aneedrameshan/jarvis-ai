import whisper
import sounddevice as sd
from scipy.io.wavfile import write


class VoiceAssistant:

    def __init__(self):

        self.model = whisper.load_model("base")


    def record_audio(self,
                     filename="command.wav",
                     duration=5,
                     sample_rate=44100):

        print("\nListening...\n")

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='int16'
        )

        sd.wait()

        write(filename, sample_rate, recording)

        print("Recording complete.\n")

        return filename


    def transcribe_audio(self, filename):

        result = self.model.transcribe(filename)

        text = result["text"]

        print(f"Transcribed Text: {text}\n")

        return text