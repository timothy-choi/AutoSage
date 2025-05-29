from transformers import pipeline

generator = pipeline("text2text-generation", model="google/flan-t5-base")

def interpret_command(text):
    prompt = f"Convert this instruction into a shell command: {text}"
    result = generator(prompt, max_length=64)
    return result[0]['generated_text']

def explain_command(text):
    prompt = f"Explain what this shell command does: {text}"
    result = generator(prompt, max_length=128)
    return result[0]['generated_text']

def suggest_command_variants(text):
    prompt = f"Suggest alternative ways to achieve: {text}"
    result = generator(prompt, max_length=128)
    return result[0]['generated_text']