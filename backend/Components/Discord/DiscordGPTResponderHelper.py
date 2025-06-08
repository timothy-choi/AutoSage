from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openai import ChatCompletion
from deep_translator import GoogleTranslator
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
analyzer = SentimentIntensityAnalyzer()

async def get_gpt_response(message: str) -> str:
    result = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        max_tokens=100
    )
    return result.choices[0].message["content"]

def summarize_conversation(messages: list[str]) -> str:
    joined = " ".join(messages)
    return f"Summary: This user has been talking mostly about: {joined[:75]}..."

def respond_to_sentiment(message: str) -> str:
    score = analyzer.polarity_scores(message)['compound']
    if score > 0.3:
        return "😊 I'm glad you're feeling good!"
    elif score < -0.3:
        return "😟 Sorry to hear that. Want to talk about it?"
    else:
        return "🙂 I'm here if you need anything."

def auto_translate_response(response: str, target_lang: str = "es") -> str:
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(response)
    except:
        return response

def detect_question_topic(message: str) -> str:
    if "deploy" in message:
        return "devops"
    if "train model" in message:
        return "machine learning"
    if "login" in message or "auth" in message:
        return "authentication"
    return "general"