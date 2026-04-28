from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import get_rezept
from fastapi import HTTPException
from fastapi import Depends 
from fastapi import Form
from fastapi.responses import RedirectResponse
from typing import List 
from app.db_models import Rezept, Zutat, Schritt
from app.models import Einheit

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

@app.get("/rezepte/neu", response_class=HTMLResponse) # Muss vor Rezept_ID registriert sein, sonst interpretiert FastAPI neu als ID und versucht einen Integer draus zu machen
def rezepte_neu_form(request: Request):
    return templates.TemplateResponse(
        request, "recipe_form.html", {}
    )

@app.post("/rezepte/neu")
def rezept_neu_speichern(
    title: str = Form(...),
    portionen: int = Form(...),
    zubereitungszeit: str = Form(""),
    theme: str = Form("Standard"),
    zutat_menge: List[float] = Form([]),
    zutat_einheit: List[str] = Form([]),
    zutat_name: List[str] = Form([]),
    schritt_text: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    neues_rezept = Rezept(
        title=title,
        portionen=portionen,
        zubereitungszeit=zubereitungszeit,
        theme=theme,
        is_fav=False,
        bild="",
    )

    # Zutaten zusammenbauen
    for i, (menge, einheit_str, name) in enumerate(zip(zutat_menge, zutat_einheit, zutat_name)):
        if not name.strip():
            continue # Leere Zeile überspringen
        einheit = Einheit(einheit_str) #String -> Enum
        zutat = Zutat(name=name, menge=menge, einheit=einheit, position=i)
        neues_rezept.zutaten.append(zutat)

    # Schritte zusammenbauen
    for i, text in enumerate(schritt_text):
        if not text.strip():
            continue
        schritt = Schritt(text=text, position=i)
        neues_rezept.schritte.append(schritt)

    db.add(neues_rezept)
    db.commit()
    db.refresh(neues_rezept)

    return RedirectResponse(url=f"/rezepte/{neues_rezept.id}", status_code=303)

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