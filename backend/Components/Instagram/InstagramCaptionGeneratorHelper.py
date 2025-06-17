import openai

async def generate_instagram_caption(prompt: str, openai_api_key: str) -> dict:
    openai.api_key = openai_api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes catchy and creative Instagram captions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.8
        )
        caption = response["choices"][0]["message"]["content"].strip()
        return {"caption": caption}
    except Exception as e:
        return {"error": str(e)}

async def generate_hashtags(topic: str, openai_api_key: str) -> dict:
    openai.api_key = openai_api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates relevant Instagram hashtags."},
                {"role": "user", "content": f"Give 10 trending hashtags for: {topic}"}
            ],
            max_tokens=60,
            temperature=0.7
        )
        hashtags = response["choices"][0]["message"]["content"].strip()
        return {"hashtags": hashtags}
    except Exception as e:
        return {"error": str(e)}

async def generate_emojified_caption(prompt: str, openai_api_key: str) -> dict:
    openai.api_key = openai_api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative assistant that writes Instagram captions with emojis."},
                {"role": "user", "content": f"Write a caption with emojis for: {prompt}"}
            ],
            max_tokens=60,
            temperature=0.85
        )
        caption = response["choices"][0]["message"]["content"].strip()
        return {"emojified_caption": caption}
    except Exception as e:
        return {"error": str(e)}