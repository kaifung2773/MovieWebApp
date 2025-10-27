from fastapi import FastAPI, Query, HTTPException, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pymongo import MongoClient
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from database import movies_collection

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def read_index():
    return FileResponse('app/static/index.html')

@router.get("/movies")
async def read_movies_page():
    return FileResponse('app/static/movies.html')

@router.get("/movies/{id}", response_class=HTMLResponse)
async def movie_detail_page(request: Request, id: str):
    movie = movies_collection.find_one({"_id": ObjectId(id)})
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie["_id"] = str(movie["_id"])
    
    return templates.TemplateResponse(
        "movie_detail.html",
        {"request": request, "movie": movie}
    )