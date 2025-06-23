import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_linkedin_content(content: str, tone: str = "professional", length: str = "short") -> str:
    prompt = f"""
Summarize the following LinkedIn content in a {tone} tone. Keep the summary {length}.

Original content:
\"\"\"{content}\"\"\"
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200 if length == "short" else 400,
            temperature=0.5
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Error generating summary: {str(e)}]"