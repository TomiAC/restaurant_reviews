from fastapi import FastAPI, HTTPException, Request
from app.schemas import ReviewIn, ReviewOut, LeaderboardPage
from app.database import get_leaderboard
from bson import ObjectId
from app.npl_utils import analyze_sentiment
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers.restaurant import restaurants_router
from app.routers.reviews import reviews_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(reviews_router)
app.include_router(restaurants_router)

templates = Jinja2Templates(directory="templates")

# leaderboard = get_leaderboard()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/leaderboard")
async def send_leaderboard(page : int = 0):
    leaderboard = get_leaderboard()
    if len(leaderboard) > (page + 1) * 10:
        leaderboard = leaderboard[page * 10 : (page + 1) * 10]
    else:
        leaderboard = leaderboard[page * 10:]
    return {"leaderboard": leaderboard}