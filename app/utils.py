from datetime import datetime

def serialize_review(review):
    return {
        "id": str(review.get("_id")),
        "restaurant_id": str(review.get("restaurant_id")),
        "text": review.get("text"),
        "sentiment": review.get("sentiment"),
        "timestamp": review.get("timestamp").isoformat() if isinstance(review.get("timestamp"), datetime) else None
    }