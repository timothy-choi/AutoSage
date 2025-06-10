import os
import aiohttp
import tempfile
import speech_recognition as sr

async def download_audio_file(file_url: str, token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url, headers=headers) as resp:
            if resp.status == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(await resp.read())
                    return tmp.name
            raise Exception(f"Failed to download file: {resp.status}")

def generate_transcript(audio_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError as e:
            return f"API error: {e}"