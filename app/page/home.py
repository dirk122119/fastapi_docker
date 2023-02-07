from fastapi import FastAPI, APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/home/{id}", response_class=HTMLResponse)
def read_item( request: Request,id:str):
    context ={"request": request,"id":id}
    return templates.TemplateResponse("item.html",context)