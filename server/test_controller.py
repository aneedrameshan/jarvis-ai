from agent import JarvisAgent
from voice import VoiceAssistant
from wake_word import WakeWordDetector


agent = JarvisAgent()

voice = VoiceAssistant()

wake_word = WakeWordDetector()


while True:

    wake_word.listen_for_wake_word()

    print("\nJarvis: Yes?\n")

    audio_file = voice.record_audio()

    command = voice.transcribe_audio(audio_file)

    agent.run_command(command)
    
    agent.analyze_screen()
