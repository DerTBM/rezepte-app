from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.models import build_ofgy

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def hello():
    return {"message": "Hallo Welt"}

@app.get("/rezepte/ofgy")
def get_ofgy():
    return build_ofgy()

@app.get("/rezept-html", response_class=HTMLResponse)
def rezept_html(request: Request):
    rezept = build_ofgy()
    return templates.TemplateResponse(
        request, "recipe.html", {"rezept": rezept}
    )