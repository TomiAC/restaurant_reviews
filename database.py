from pymongo import MongoClient, DESCENDING
from hashing import hash_password, verify_password
import os
from dotenv import load_dotenv
from npl_utils import analyze_sentiment
from collections import defaultdict
from bson import ObjectId

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
    cursor = db.restaurants.find({"name": {"$regex": name, "$options": "i"}}).limit(5)
    return [{"_id": str(r["_id"]), "name": r["name"]} for r in cursor]

def get_leaderboard():
    restaurants = get_restaurants()  # Lista de restaurantes desde Mongo
    reviews = get_reviews()          # Lista de reviews desde Mongo
    
    # Agrupamos las reviews por restaurant_id
    reviews_by_restaurant = defaultdict(list)
    for review in reviews:
        reviews_by_restaurant[review["restaurant_id"]].append(review)

    leaderboard = []
    for restaurant in restaurants:
        rest_id = restaurant["_id"]
        pos = sum(1 for r in reviews_by_restaurant.get(rest_id, []) if r["sentiment"] == "positive")
        neg = sum(1 for r in reviews_by_restaurant.get(rest_id, []) if r["sentiment"] == "negative")
        
        leaderboard.append({
            "name": restaurant["name"],
            "positive_reviews": pos,
            "negative_reviews": neg,
            "score": pos - neg
        })

    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return leaderboard

def get_reviews_by_restaurant_id(restaurant_id: ObjectId):
    return list(reviews_collection.find(
        {"restaurant_id": restaurant_id}
    ))