import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from fastapi import FastAPI, Query
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import re

def summarize_content(text: str, num_sentences: int = 3) -> str:
    try:
        sentences = re.split(r'(?<=[.!?]) +', text)
        if len(sentences) <= num_sentences:
            return text

        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(sentences)

        kmeans = KMeans(n_clusters=num_sentences, random_state=0, n_init=10)
        kmeans.fit(X)

        summary = []
        for i in range(num_sentences):
            idx = kmeans.labels_ == i
            selected = [sentences[j] for j, match in enumerate(idx) if match]
            if selected:
                summary.append(selected[0])

        return ' '.join(summary)
    except Exception as e:
        return f"Error summarizing content: {str(e)}"