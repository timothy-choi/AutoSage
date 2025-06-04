import os
import tempfile
from moviepy import VideoFileClip
import speech_recognition as sr
from typing import Optional

def generate_subtitles_from_video(video_path: str, language: str = 'en-US') -> Optional[str]:
    try:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        video = VideoFileClip(video_path)
        audio_path = tempfile.mktemp(suffix=".wav")
        video.audio.write_audiofile(audio_path)

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        transcript = recognizer.recognize_google(audio_data, language=language)

        srt_path = os.path.splitext(video_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            srt_file.write("1\n")
            srt_file.write("00:00:00,000 --> 00:00:10,000\n") 
            srt_file.write(transcript + "\n")

        os.remove(audio_path)
        return srt_path

    except Exception as e:
        print(f"Error generating subtitles: {e}")
        return None