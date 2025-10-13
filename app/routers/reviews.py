from fastapi import APIRouter, HTTPException
from app.schemas import ReviewIn, ReviewOut
from app.database import get_restaurant_by_id, save_review
from datetime import datetime
from bson import ObjectId
from app.npl_utils import analyze_sentiment
from app.redis_manager import redis_client

reviews_router = APIRouter(prefix="/reviews", tags=["Reviews"])

@reviews_router.post("/", response_model=ReviewOut)
def add_review(review: ReviewIn):
    restaurant = get_restaurant_by_id(review.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    sentiment = analyze_sentiment(review.text)
    new_review = {
        "restaurant_id": ObjectId(review.restaurant_id),
        "author_name": review.author_name,
        "rating": review.rating,
        "text": review.text,
        "sentiment": sentiment,
        "timestamp": datetime.utcnow()
    }

    save_review(new_review)
    redis_client.delete("leaderboard")

    #update_leaderboard(str(review.restaurant_id), sentiment)
    return {"sentiment": sentiment}