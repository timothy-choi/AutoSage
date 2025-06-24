import openai
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_youtube_video_id(url_or_id: str) -> str:
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        if "v=" in url_or_id:
            return url_or_id.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in url_or_id:
            return url_or_id.split("youtu.be/")[-1].split("?")[0]
    return url_or_id.strip()

def fetch_transcript_text(video_id: str) -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        return ""
    except Exception as e:
        raise RuntimeError(f"Error fetching transcript: {str(e)}")

def generate_caption_from_transcript(transcript_text: str) -> str:
    if not transcript_text:
        return "Transcript not available or disabled for this video."

    prompt = f"Summarize the following YouTube transcript into a compelling caption or description:\n\n{transcript_text}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error generating caption: {str(e)}]"

def auto_generate_youtube_caption(url_or_id: str) -> dict:
    video_id = get_youtube_video_id(url_or_id)
    transcript = fetch_transcript_text(video_id)

    if not transcript:
        return {"status": "error", "message": "Transcript not available for this video."}

    caption = generate_caption_from_transcript(transcript)
    return {
        "status": "success",
        "video_id": video_id,
        "caption": caption
    }