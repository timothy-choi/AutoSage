import pyttsx3

engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def save_speech(text, filename="output.mp3"):
    engine.save_to_file(text, filename)
    engine.runAndWait()

def set_voice(voice_name):
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice_name.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            return True
    return False