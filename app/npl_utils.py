from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    return "positive" if TextBlob(text).sentiment.polarity >= 0 else "negative"