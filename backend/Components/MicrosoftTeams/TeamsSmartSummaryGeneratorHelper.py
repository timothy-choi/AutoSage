import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_smart_summary(text: str, context: str = "team discussion") -> dict:
    prompt = (
        f"Summarize the following {context} in bullet points:\n\n{text}\n\nSummary:"
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes conversations."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        return {"error": str(e)}

async def generate_action_items(text: str, context: str = "team discussion") -> dict:
    prompt = (
        f"List actionable items from the following {context}.\n\n{text}\n\nAction Items:"
    )
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You extract action items from team discussions."},
                {"role": "user", "content": prompt}
            ]
        )
        actions = response.choices[0].message.content.strip()
        return {"action_items": actions}
    except Exception as e:
        return {"error": str(e)}