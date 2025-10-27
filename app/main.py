from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import pages, api

app = FastAPI()

# Mount static files in main app
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(pages.router)
app.include_router(api.router)