from fastapi import Request
import xml.etree.ElementTree as ET

def handle_youtube_verification(request: Request):
    challenge = request.query_params.get("hub.challenge")
    mode = request.query_params.get("hub.mode")
    topic = request.query_params.get("hub.topic")

    if mode == "subscribe":
        return {"challenge": challenge}
    return {"message": f"Unhandled mode: {mode}"}

def parse_youtube_notification(xml_body: str) -> dict:
    try:
        root = ET.fromstring(xml_body)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entry = root.find("atom:entry", ns)
        if entry is None:
            return {"message": "No entry found (likely unsubscribe notification)"}

        video_id = entry.find("atom:id", ns).text.split(":")[-1]
        title = entry.find("atom:title", ns).text
        published = entry.find("atom:published", ns).text
        updated = entry.find("atom:updated", ns).text
        channel_id = entry.find("atom:author/atom:uri", ns).text.split("/")[-1]

        return {
            "video_id": video_id,
            "title": title,
            "published": published,
            "updated": updated,
            "channel_id": channel_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}"
        }
    except Exception as e:
        return {"error": str(e), "raw": xml_body}