"""
FastAPI-Anwendung für die Rezepte-App.

Definiert alle HTTP-Endpunkte, mappt Form-Daten auf DB-Operationen und
rendert HTML-Templates über Jinja2.

Endpunkt-Struktur:
- /                          Landing Page mit Suche und Kategorien
- /rezepte/neu              Form zum Anlegen (GET) bzw. Speichern (POST)
- /rezepte/{id}             Detail-Anzeige eines Rezepts
- /rezepte/{id}/edit        Form zum Bearbeiten (GET) bzw. Speichern (POST)
- /rezepte/{id}/loeschen    Löschen (POST)
- /kategorie/{name}         Übersicht aller Rezepte einer Kategorie
- /suche?q=...              Suchergebnisse
"""
from typing import List

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.db_models import Rezept, Zutat, Schritt
from app.models import Einheit, THEMES, KATEGORIEN, Theme, get_theme, get_kategorie
from app.crud import get_rezept, get_alle_rezepte, get_rezepte_nach_kategorie, suche_rezepte


# App-Setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Statische Dateien (CSS, Bilder) werden unter /static/... ausgeliefert
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    """
    Dependency: stellt eine DB-Session bereit und schließt sie nach dem Request.

    FastAPI ruft diese Funktion bei jedem Request mit Depends(get_db) auf.
    Das yield übergibt die Session an den Endpunkt, das finally schließt sie -
    egal ob der Endpunkt erfolgreich war oder eine Exception geworfen hat.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# LANDING PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def landing(request: Request, db: Session = Depends(get_db)):
    """Startseite: zeigt alle Rezepte plus Kategorie-Auswahl und Suche."""
    rezepte = get_alle_rezepte(db)
    return templates.TemplateResponse(
        request, "landing.html", {"rezepte": rezepte, "kategorien": KATEGORIEN}
    )


# ============================================================
# REZEPT ANLEGEN (Create)
# ============================================================

# Muss VOR /rezepte/{rezept_id} registriert sein, sonst wird "neu" als ID
# interpretiert und FastAPI versucht es zu einem int zu casten -> Validation-Error.
@app.get("/rezepte/neu", response_class=HTMLResponse)
def rezepte_neu_form(request: Request):
    """Zeigt das leere Form zum Anlegen eines neuen Rezepts."""
    return templates.TemplateResponse(
        request, "recipe_form.html", {"themes": THEMES}
    )


@app.post("/rezepte/neu")
def rezept_neu_speichern(
    title: str = Form(...),
    portionen: int = Form(...),
    zubereitungszeit: str = Form(""),
    theme: str = Form("Standard"),
    # Die List-Parameter kommen vom Form als mehrere Inputs mit gleichem name:
    # name="zutat_name" mehrfach -> zutat_name = ["Mehl", "Zucker", ...]
    zutat_menge: List[float] = Form([]),
    zutat_einheit: List[str] = Form([]),
    zutat_name: List[str] = Form([]),
    schritt_text: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    """Verarbeitet das Form-Submit beim Neuanlegen und schreibt das Rezept in die DB."""
    neues_rezept = Rezept(
        title=title,
        portionen=portionen,
        zubereitungszeit=zubereitungszeit,
        theme=theme,
        is_fav=False,
        bild="",
    )

    # Zutaten zusammenbauen: zip() kombiniert die drei parallelen Listen
    # zu Tupeln (menge, einheit, name), enumerate() liefert dazu den Index.
    for i, (menge, einheit_str, name) in enumerate(zip(zutat_menge, zutat_einheit, zutat_name)):
        if not name.strip():
            continue  # leere Zeilen aus dem Form überspringen
        einheit = Einheit(einheit_str)  # String aus Form -> Enum-Wert
        zutat = Zutat(name=name, menge=menge, einheit=einheit, position=i)
        neues_rezept.zutaten.append(zutat)

    # Schritte analog zusammenbauen
    for i, text in enumerate(schritt_text):
        if not text.strip():
            continue
        schritt = Schritt(text=text, position=i)
        neues_rezept.schritte.append(schritt)

    # add() merkt das Objekt für den Insert vor, commit() führt's aus.
    # Dank der relationship-Definitionen werden Zutaten/Schritte automatisch mit-inserted.
    db.add(neues_rezept)
    db.commit()
    # refresh() lädt die DB-generierten Felder zurück (vor allem die auto-increment id)
    db.refresh(neues_rezept)

    # Post/Redirect/Get-Pattern: nach POST nicht direkt HTML zurückgeben,
    # sondern auf eine GET-URL umleiten. Verhindert dass ein Page-Reload
    # das Rezept doppelt anlegt.
    return RedirectResponse(url=f"/rezepte/{neues_rezept.id}", status_code=303)


# ============================================================
# REZEPT ANZEIGEN (Read)
# ============================================================

@app.get("/rezepte/{rezept_id}", response_class=HTMLResponse)
def rezept_html(rezept_id: int, request: Request, db: Session = Depends(get_db)):
    """Zeigt ein einzelnes Rezept als Detail-Seite mit Theme-Farben."""
    rezept = get_rezept(db, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")

    # Theme-Objekt zum gespeicherten Theme-Namen suchen.
    # Falls das Theme aus der THEMES-Liste entfernt wurde (z.B. nach Umbenennung),
    # nehmen wir einen grauen Default statt zu crashen.
    try:
        theme = get_theme(rezept.theme)
    except ValueError:
        theme = Theme(name="Standard", farbe="#cccccc")

    return templates.TemplateResponse(
        request, "recipe.html", {"rezept": rezept, "theme": theme}
    )


# ============================================================
# REZEPT BEARBEITEN (Update)
# ============================================================

@app.get("/rezepte/{rezept_id}/edit", response_class=HTMLResponse)
def rezept_edit_form(rezept_id: int, request: Request, db: Session = Depends(get_db)):
    """Zeigt das Edit-Form mit den aktuellen Werten des Rezepts vorausgefüllt."""
    rezept = get_rezept(db, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
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
    """
    Verarbeitet das Edit-Form-Submit.

    Strategie: Replace-All. Alle Zutaten und Schritte werden gelöscht und
    neu angelegt - statt zu mergen. Trade-off: einfacher Code, aber alte IDs
    gehen verloren. Für ein Familienprojekt akzeptabel.
    """
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")

    # Haupt-Felder updaten - SQLAlchemy trackt die Änderungen automatisch
    rezept.title = title
    rezept.portionen = portionen
    rezept.zubereitungszeit = zubereitungszeit
    rezept.theme = theme

    # Alte Zutaten und Schritte raus. Dank cascade="all, delete-orphan"
    # werden die entsprechenden DB-Zeilen beim commit() gelöscht.
    rezept.zutaten.clear()
    rezept.schritte.clear()

    # Neue Zutaten anlegen (Logik identisch zum Anlegen)
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


# ============================================================
# REZEPT LÖSCHEN (Delete)
# ============================================================

@app.post("/rezepte/{rezept_id}/loeschen")
def rezept_loeschen(rezept_id: int, db: Session = Depends(get_db)):
    """
    Löscht ein Rezept inkl. aller zugehörigen Zutaten/Schritte/Kategorie-Zuordnungen.

    Die abhängigen Datensätze werden durch ON DELETE CASCADE im DB-Schema
    automatisch mitgelöscht (siehe schema.sql).
    """
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")
    db.delete(rezept)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


# ============================================================
# KATEGORIE-ÜBERSICHT
# ============================================================

@app.get("/kategorie/{kategorie_name}", response_class=HTMLResponse)
def kategorie_seite(kategorie_name: str, request: Request, db: Session = Depends(get_db)):
    """Zeigt alle Rezepte einer bestimmten Kategorie."""
    # Kategorie-Objekt für Name + Farbe holen (für UI)
    try:
        kategorie = get_kategorie(kategorie_name)
    except ValueError:
        raise HTTPException(status_code=404, detail="Kategorie nicht gefunden")

    rezepte = get_rezepte_nach_kategorie(db, kategorie_name)

    return templates.TemplateResponse(
        request, "kategorie.html", {"kategorie": kategorie, "rezepte": rezepte}
    )


# ============================================================
# SUCHE
# ============================================================

@app.get("/suche", response_class=HTMLResponse)
def suche_seite(request: Request, q: str = "", db: Session = Depends(get_db)):
    """
    Sucht Rezepte nach Titel.

    Der Suchbegriff kommt als Query-Parameter (?q=...).
    Wenn leer, wird gar nicht gesucht sondern eine leere Liste angezeigt.
    """
    rezepte = suche_rezepte(db, q) if q else []
    return templates.TemplateResponse(
        request, "suche.html", {"suchbegriff": q, "rezepte": rezepte}
    )