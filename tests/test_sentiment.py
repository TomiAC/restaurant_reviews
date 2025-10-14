from app.npl_utils import analyze_sentiment

def test_analyze_sentiment():
    assert analyze_sentiment("I love this restaurant!") == "positive"
    assert analyze_sentiment("This is the worst service ever.") == "negative"
    assert analyze_sentiment("The food was okay, nothing special.") == "positive"