import whisper

model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result['text']

def detect_language(file_path):
    result = model.transcribe(file_path)
    return result['language']

def transcribe_with_timestamps(file_path):
    result = model.transcribe(file_path, verbose=True)
    return result['segments']