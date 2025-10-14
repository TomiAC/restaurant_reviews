from pymongo import MongoClient, DESCENDING
from app.hashing import verify_password
import os
from dotenv import load_dotenv
from bson import ObjectId
from app.redis_manager import redis_client
import json

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)
db = client["restaurant_reviews"]

restaurants_collection = db["restaurants"]
reviews_collection = db["reviews"]
user_collection = db["users"]

def get_reviews_for_restaurant(restaurant_id):
    return reviews_collection.find({"restaurant_id": restaurant_id})

def get_restaurant_by_id(restaurant_id):
    obj_id = ObjectId(restaurant_id)
    return restaurants_collection.find_one({"_id": obj_id})

def get_restaurants():
    return restaurants_collection.find()

def get_reviews():
    return reviews_collection.find()

def save_review(review):
    reviews_collection.insert_one(review)

def save_restaurant(restaurant):
    restaurants_collection.insert_one(restaurant)

def save_user(user):
    user_collection.insert_one(user)

def get_user_by_email(email):
    return user_collection.find_one({"email": email})

def get_user_by_id(user_id):
    user_id = ObjectId(user_id)
    return user_collection.find_one({"_id": user_id})

def check_credentials(email, password):
    user = get_user_by_email(email)
    if user and verify_password(password, user["password"]):
        return True
    return False

def search_restaurants(name: str):
    cursor = restaurants_collection.find({"name": {"$regex": name, "$options": "i"}}).limit(5)
    return [{"_id": str(r["_id"]), "name": r["name"]} for r in cursor]

def get_leaderboard():
    cached_leaderboard = redis_client.get("leaderboard")
    if cached_leaderboard:
        return json.loads(cached_leaderboard)

    pipeline = [
        {
            "$group": {
                "_id": "$restaurant_id",
                "positive_reviews": {
                    "$sum": {
                        "$cond": [{"$eq": ["$sentiment", "positive"]}, 1, 0]
                    }
                },
                "negative_reviews": {
                    "$sum": {
                        "$cond": [{"$eq": ["$sentiment", "negative"]}, 1, 0]
                    }
                },
            },
        },
        {
            "$lookup": {
                "from": "restaurants",
                "localField": "_id",
                "foreignField": "_id",
                "as": "restaurant",
            }
        },
        {"$unwind": "$restaurant"},
        {
            "$project": {
                "_id": 0, # Exclude the default _id
                "name": "$restaurant.name",
                "positive_reviews": "$positive_reviews",
                "negative_reviews": "$negative_reviews",
                "score": {"$subtract": ["$positive_reviews", "$negative_reviews"]},
            }
        },
        {"$sort": {"score": -1}},
    ]
    leaderboard = list(reviews_collection.aggregate(pipeline))
    redis_client.set("leaderboard", json.dumps(leaderboard), ex=3600)
    return leaderboard

def get_reviews_by_restaurant_id(restaurant_id: ObjectId):
    return list(reviews_collection.find(
        {"restaurant_id": restaurant_id}
    ))