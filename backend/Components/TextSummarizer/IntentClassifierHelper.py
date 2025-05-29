from transformers import pipeline

classifier = pipeline("zero-shot-classification")

def classify_intent(text, labels=None):
    if labels is None:
        labels = ["summarize", "compare documents", "transcribe", "read aloud", "run command", "search", "fetch data"]
    result = classifier(text, labels)
    return result['labels'][0]

def rank_intents(text, labels=None):
    if labels is None:
        labels = ["summarize", "compare", "transcribe", "read", "command"]
    result = classifier(text, labels)
    return list(zip(result['labels'], result['scores']))

def is_intent_match(text, intent):
    labels = [intent, "other"]
    result = classifier(text, labels)
    return result['labels'][0] == intent