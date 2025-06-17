import aiohttp
import zipfile
import os
from datetime import datetime
import csv

async def export_user_media_archive(user_id: str, access_token: str, export_dir: str = "/tmp") -> dict:
    media_url = f"https://graph.facebook.com/v19.0/{user_id}/media?fields=id,caption,media_type,media_url,timestamp&access_token={access_token}"
    zip_filename = os.path.join(export_dir, f"instagram_archive_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
    csv_filename = os.path.join(export_dir, f"instagram_metadata_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")

    async with aiohttp.ClientSession() as session:
        async with session.get(media_url) as resp:
            if resp.status != 200:
                return {"error": f"Failed to fetch media: HTTP {resp.status}", "details": await resp.text()}
            media_data = await resp.json()

        with zipfile.ZipFile(zip_filename, 'w') as zipf, open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'caption', 'media_type', 'media_url', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in media_data.get("data", []):
                writer.writerow({
                    'id': item.get("id"),
                    'caption': item.get("caption"),
                    'media_type': item.get("media_type"),
                    'media_url': item.get("media_url"),
                    'timestamp': item.get("timestamp")
                })

                media_url = item.get("media_url")
                media_id = item.get("id")
                if media_url:
                    async with session.get(media_url) as media_resp:
                        if media_resp.status == 200:
                            media_content = await media_resp.read()
                            file_ext = media_url.split(".")[-1].split("?")[0]
                            file_path = os.path.join(export_dir, f"{media_id}.{file_ext}")
                            with open(file_path, "wb") as f:
                                f.write(media_content)
                            zipf.write(file_path, os.path.basename(file_path))
                            os.remove(file_path)
            zipf.write(csv_filename, os.path.basename(csv_filename))
            os.remove(csv_filename)

    return {"zip_path": zip_filename}