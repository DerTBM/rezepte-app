from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import get_rezept
from fastapi import HTTPException
from fastapi import Depends 

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    """Stellt eine DB-Session bereit, schließt sie nach dem Request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/rezepte/{rezept_id}", response_class=HTMLResponse)
def rezept_html(rezept_id: int, request: Request, db: Session = Depends(get_db)):
    rezept = get_rezept(db, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    return templates.TemplateResponse(
        request, "recipe.html", {"rezept": rezept}
    )

# Alt
# @app.get("/")
# def hello():
#     return {"message": "Hallo Welt"}

# @app.get("/rezepte/ofgy")
# def get_ofgy():
#     return build_ofgy()

# @app.get("/rezept-html", response_class=HTMLResponse)
# def rezept_html(request: Request):
#     rezept = build_ofgy()
#     return templates.TemplateResponse(
#         request, "recipe.html", {"rezept": rezept}
#     )