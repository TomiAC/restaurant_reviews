from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class ReviewIn(BaseModel):
    restaurant_id: str
    text: str
    rating: int
    author_name: str

class ReviewOut(BaseModel):
    sentiment: str

class Restaurant(BaseModel):
    name: str
    description: Optional[str]

class LeaderboardPage(BaseModel):
    page: int = 0