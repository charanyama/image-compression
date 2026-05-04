from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.compress import router as compress_router
from app.routes.pages import router as pages_router

app = FastAPI()

app.include_router(pages_router)
app.include_router(compress_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
