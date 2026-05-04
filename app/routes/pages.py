from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def landing_page(req: Request):
    return templates.TemplateResponse(request=req, name="landing.html")


@router.get("/compress")
async def compress_page(req: Request):
    return templates.TemplateResponse(request=req, name="compress.html")
