from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(message: str) -> dict:
    scores = analyzer.polarity_scores(message)
    compound = scores['compound']

    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {
        "sentiment": label,
        "compound": compound,
        "details": scores  
    }