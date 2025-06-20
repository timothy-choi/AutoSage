import openai

async def generate_smart_reply(message_text: str, conversation_context: str = "") -> str:
    prompt = f"You are an Instagram assistant. Respond helpfully and concisely.\n\nContext: {conversation_context}\nUser: {message_text}\nReply:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful Instagram bot."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating reply: {str(e)}"

async def extract_intent(message_text: str) -> str:
    prompt = f"Classify the intent of this Instagram message in one word (e.g., greeting, complaint, question, feedback, spam):\n\n'{message_text}'"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an intent classifier for Instagram DMs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=10
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        return f"error: {str(e)}"

async def suggest_canned_response(intent: str) -> str:
    responses = {
        "greeting": "Hi there! Thanks for reaching out 😊",
        "complaint": "I'm really sorry to hear that. Let me look into it right away.",
        "question": "Great question! Let me get the answer for you.",
        "feedback": "Thanks for your feedback — we really appreciate it!",
        "spam": "This message has been flagged as inappropriate."
    }
    return responses.get(intent, "Thanks for messaging us! We'll get back to you shortly.")