from fastapi import FastAPI, Depends, HTTPException, APIRouter
from database import get_reviews_by_restaurant_id, search_restaurants
from schemas import Restaurant
from bson import ObjectId
from utils import serialize_review

restaurants_router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@restaurants_router.get("/{restaurant_id}/reviews")
def get_reviews_for_restaurant(restaurant_id: str):
    try:
        obj_id = ObjectId(restaurant_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid restaurant ID")

    reviews = get_reviews_by_restaurant_id(obj_id)

    print(reviews)
    
    if not reviews:
        return {"message": "No reviews found for this restaurant"}
    
    serialized_reviews = [serialize_review(r) for r in reviews]

    return {"reviews": serialized_reviews}

@restaurants_router.get("/search")
def search_restaurants_by_name(name: str):
    return search_restaurants(name)