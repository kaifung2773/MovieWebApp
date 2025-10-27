from fastapi import Query, HTTPException, APIRouter
from pymongo import MongoClient
from bson import ObjectId
from database import movies_collection

router = APIRouter(prefix="/api")

# Route for many movies
@router.get("/movies")
async def get_movies(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(12, ge=1, le=100, description="Items per page"),
    genre: str = Query(None, description="Filter by genre"),
    year: int = Query(None, description="Filter by year"),
    search: str = Query(None, description="Search movies by title")
):
    try:
        # Build query filter
        filter_query = {}
        if genre:
            filter_query["genre"] = {"$regex": genre, "$options": "i"}
        if year:
            filter_query["year"] = year
        if search:
            filter_query["title"] = {"$regex": search, "$options": "i"}
        
        # Calculate skip for pagination
        skip = (page - 1) * limit
        
        # Get movies from database
        movies_cursor = movies_collection.find(filter_query).skip(skip).limit(limit)
        movies = list(movies_cursor)
        
        # Convert ObjectId to string for JSON serialization
        for movie in movies:
            movie["_id"] = str(movie["_id"])
        
        # Get total count for pagination info
        total_count = movies_collection.count_documents(filter_query)
        
        return {
            "movies": movies,
            "page": page,
            "limit": limit,
            "total_count": total_count,
            "total_returned": len(movies),
            "has_more": skip + limit < total_count
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "movies": [],
            "page": page,
            "limit": limit,
            "total_count": 0,
            "total_returned": 0,
            "has_more": False
        }
    

# Route for a single movie
@router.get("/movies/{movie_id}")
async def get_movie(movie_id:str):
    try:
        movie = movies_collection.find_one({"_id": ObjectId(movie_id)})

        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        movie["_id"] = str(movie["_id"])

        return {"movie": movie}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
