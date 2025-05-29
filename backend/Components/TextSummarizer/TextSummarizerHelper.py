from transformers import pipeline

def summarize_text(text, max_length=150, min_length=40):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def summarize_paragraphs(paragraphs, max_length=100):
    summaries = [summarize_text(p, max_length=max_length) for p in paragraphs]
    return "\n".join(summaries)

def summarize_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return summarize_text(text)