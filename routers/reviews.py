from fastapi import APIRouter, HTTPException
from schemas import ReviewIn, ReviewOut
from database import get_restaurant_by_id, save_review
from datetime import datetime
from bson import ObjectId
from npl_utils import analyze_sentiment

reviews_router = APIRouter(prefix="/reviews", tags=["Reviews"])

@reviews_router.post("/", response_model=ReviewOut)
def add_review(review: ReviewIn):
    print("Ingreso al add review")
    print(review.restaurant_id)
    restaurant = get_restaurant_by_id(review.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurante no encontrado")
    print(restaurant)
    sentiment = analyze_sentiment(review.text)
    print(sentiment)
    new_review = {
        "restaurant_id": ObjectId(review.restaurant_id),
        "author_name": review.author_name,
        "rating": review.rating,
        "text": review.text,
        "sentiment": sentiment,
        "timestamp": datetime.utcnow()
    }

    save_review(new_review)

    #update_leaderboard(str(review.restaurant_id), sentiment)
    return {"sentiment": sentiment}