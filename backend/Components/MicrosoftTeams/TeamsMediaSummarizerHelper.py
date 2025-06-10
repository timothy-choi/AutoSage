import aiohttp
import tempfile
import os
from PIL import Image
import pytesseract

async def download_image(file_url: str, token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url, headers=headers) as resp:
            if resp.status == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    tmp.write(await resp.read())
                    return tmp.name
            raise Exception(f"Failed to download image: {resp.status}")

def summarize_image_text(image_path: str) -> str:
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "No readable text found in image."
    except Exception as e:
        return f"Image processing error: {e}"