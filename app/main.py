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


# Muss vor Rezept_ID registriert sein, sonst interpretiert FastAPI neu als ID und versucht einen Integer draus zu machen
@app.get("/rezepte/neu", response_class=HTMLResponse)
def rezepte_neu_form(request: Request):
    from app.models import THEMES
    return templates.TemplateResponse(
        request, "recipe_form.html", {"themes": THEMES}
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
            continue  # Leere Zeile überspringen
        einheit = Einheit(einheit_str)  # String -> Enum
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

# Rezept HTML-Seite
@app.get("/rezepte/{rezept_id}", response_class=HTMLResponse)
def rezept_html(rezept_id: int, request: Request, db: Session = Depends(get_db)):
    rezept = get_rezept(db, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    
    # Theme-Objekt nachschlagen anhand des Theme-Namens aus dem Rezept
    from app.models import get_theme, Theme
    try:
        theme = get_theme(rezept.theme)
    except ValueError:
        # Falls Theme-Name nicht in der Liste, nimm einen Default
        theme = Theme(name="Standard", farbe="#cccccc")

    return templates.TemplateResponse(
        request, "recipe.html", {"rezept": rezept, "theme": theme}
    )

# Rezept löschen
@app.post("/rezepte/{rezept_id}/loeschen")
def rezept_loeschen(rezept_id: int, db: Session = Depends(get_db)):
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    db.delete(rezept)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/rezepte/{rezept_id}/edit", response_class=HTMLResponse)
def rezept_edit_form(rezept_id: int, request: Request, db: Session = Depends(get_db)):
    rezept = get_rezept(db, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    from app.models import THEMES
    return templates.TemplateResponse(
        request, "recipe_edit.html", {"rezept": rezept, "themes": THEMES}
    )


@app.post("/rezepte/{rezept_id}/edit")
def rezept_edit_speichern(
    rezept_id: int,
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
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")


    # Hauptdaten updaten
    rezept.title = title
    rezept.portionen = portionen
    rezept.zubereitungszeit = zubereitungszeit
    rezept.theme = theme

    # Replace-All: Alte Zutateten und Schritte be gone
    rezept.zutaten.clear()
    rezept.schritte.clear()

    # Neue Zutaten anlegen
    for i, (menge, einheit_str, name) in enumerate(zip(zutat_menge, zutat_einheit, zutat_name)):
        if not name.strip():
            continue
        einheit = Einheit(einheit_str)
        zutat = Zutat(name=name, menge=menge, einheit=einheit, position=i)
        rezept.zutaten.append(zutat)

    # Neue Schritte anlegen
    for i, text in enumerate(schritt_text):
        if not text.strip():
            continue
        schritt = Schritt(text=text, position=i)
        rezept.schritte.append(schritt)

    db.commit()

    return RedirectResponse(url=f"/rezepte/{rezept_id}", status_code=303)

@app.get("/kategorie/{kategorie_name}", response_class=HTMLResponse)
def kategorie_seite(kategorie_name: str, request: Request, db: Session = Depends(get_db)):
    from app.crud import get_rezepte_nach_kategorie
    from app.models import get_kategorie

    rezepte = get_rezepte_nach_kategorie(db, kategorie_name)

    try:
        kategorie = get_kategorie(kategorie_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")
    
    return templates.TemplateResponse(
        request, "kategorie.html", {"kategorie": kategorie, "rezepte": rezepte}
    )

@app.get("/suche", response_class=HTMLResponse)
def suche_seite(request: Request, q: str = "", db: Session = Depends(get_db)):
    from app.crud import suche_rezepte
    
    rezepte = suche_rezepte(db, q) if q else []

    return templates.TemplateResponse(
        request, "suche.html", {"suchbegriff": q, "rezepte":rezepte}
    )

@app.get("/", response_class=HTMLResponse)
def landing(request: Request, db: Session = Depends(get_db)):
    from app.crud import get_alle_rezepte
    from app.models import KATEGORIEN
    rezepte = get_alle_rezepte(db)
    return templates.TemplateResponse(
        request, "landing.html", {"rezepte": rezepte, "kategorien": KATEGORIEN}
    )