import whisper
import os

import whisper
import os

def generate_transcript(
    audio_path: str,
    model_size: str = "base",
    save_to: str = None,
    format: str = "txt"
) -> dict:
    if not os.path.exists(audio_path):
        raise FileNotFoundError("File not found.")

    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)

    text = result.get("text", "")
    segments = result.get("segments", [])

    if save_to:
        if format == "txt":
            with open(save_to, "w", encoding="utf-8") as f:
                f.write(text)
        elif format == "srt":
            with open(save_to, "w", encoding="utf-8") as f:
                for i, segment in enumerate(segments):
                    start = format_timestamp(segment["start"])
                    end = format_timestamp(segment["end"])
                    f.write(f"{i+1}\n{start} --> {end}\n{segment['text'].strip()}\n\n")
        else:
            raise ValueError("Unsupported format: choose 'txt' or 'srt'")

    return {
        "text": text,
        "segments": segments,
        "saved_to": save_to if save_to else None
    }

def format_timestamp(seconds: float) -> str:
    hrs, rem = divmod(int(seconds), 3600)
    mins, secs = divmod(rem, 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"
