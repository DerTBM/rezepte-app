"""
FastAPI-Anwendung für die Rezepte-App. 
Definiert alle HTTP-Endpunkte, mappt Form-Daten auf DB-Operationen und rendert HTML-Templates über Jinja2.

Endpunkt-Struktur:
- /                         Landing Page mit Suche und Kategorien
- /rezepte/neu              Form zum Anlegen (GET) bzw. Speichern (POST)
- /rezepte/{id}             Detail-Anzeige eines Rezepts
- /rezepte/{id}/edit        Form zum Bearbeiten (GET) bzw. Speichern (POST)
- /rezepte/{id}/loeschen    Löschen (POST)
- /rezepte/{id}/favorit     Favoriten-Status umschalten (POST)
- /kategorie/{name}         Übersicht aller Rezepte einer Kategorie
- /suche?q=...              Suchergebnisse
"""
from typing import List

from fastapi import FastAPI, Request, Depends, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.db_models import Rezept, Zutat, Schritt, RezeptKategorie
from app.models import Einheit, THEMES, KATEGORIEN, Theme, get_theme, get_kategorie, EINHEITEN_OHNE_MENGE, menge_als_bruch
from app.crud import get_rezept, get_alle_rezepte, get_rezepte_nach_kategorie, suche_rezepte, get_favoriten, get_zufalls_rezepte
from app.file_upload import save_recipe_image, delete_recipe_image

# App-Setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Statische Dateien (CSS, Bilder) werden unter /static/... ausgeliefert
app.mount("/static", StaticFiles(directory="static"), name="static")

# Custom Filter für Templates: 0.25 -> "1/4"
templates.env.filters["bruch"] = menge_als_bruch

@app.exception_handler(404)
def not_found_handler(request: Request, exc: StarletteHTTPException):
    """
    Fängt alle 404-Fehler ab und rendert dann eine HTML-Seite, statt der Standard JSON-Antwort von FastAPI.

    Greift sowohl bei manuell geworfenen HTTPExceptions(404) (z.B. Rezept nicht gefunden) als auch bei URLs die keine Route haben.
    """
    return templates.TemplateResponse(request, "404.html", status_code=404)


def get_db():
    """
    Dependency: stellt die DB-Session bereit und schließt sie nach dem Request.

    FastAPI ruft diese Funktion bei jedem Request mit Depends(get_db) auf.
    Das yield übergibt die Session an den Endpunkt, das finally schließt sie.
    Egal ob der Endpunkt erfolgreich war oder eine Exception geworfen hat.
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
def landing(request: Request, db: Session = Depends(get_db), nur_favoriten: bool = False):
    """
    Startseite: zeigt Rezepte plus Kategorie-Auswahl und Suche.

    Der Query-Parameter ?nur_favoriten=true schaltet die Rezept-Liste
    auf reine Favoriten-Anzeige um. Ohne den Parameter werden alle Rezepte gezeigt.

    Zusätzlich werden zwei zufällige Rezepte für die "Zufalls-Vorschläge"-
    Sektion geladen - bei jedem Seitenaufruf neu gewürfelt.
    """
    if nur_favoriten:
        rezepte = get_favoriten(db)
    else:
        rezepte = get_alle_rezepte(db)

    zufalls_rezepte = get_zufalls_rezepte(db, 2)

    return templates.TemplateResponse(
        request, "landing.html",
        {
            "rezepte": rezepte,
            "kategorien": KATEGORIEN,
            "nur_favoriten": nur_favoriten,
            "zufalls_rezepte": zufalls_rezepte,
        }
    )


# ============================================================
# REZEPT ANLEGEN (Create)
# ============================================================

# Muss VOR! /rezepte/{rezept_id} registriert sein, sonst wird "neu" als ID
# interpretiert und FastAPI versucht es zu einem int zu casten -> Validation-Error.
@app.get("/rezepte/neu", response_class=HTMLResponse)
def rezepte_neu_form(request: Request):
    """Zeigt das leere Form zum Anlegen eines neuen Rezepts."""
    return templates.TemplateResponse(
        request, "recipe_form.html", {"themes": THEMES, "kategorien": KATEGORIEN}
    )


@app.post("/rezepte/neu")
def rezept_neu_speichern(
    title: str = Form(...),
    portionen: int = Form(...),
    zubereitungszeit: str = Form(""),
    theme: str = Form("Standard"),
    bild: UploadFile = File(None),
    kategorien: List[str] = Form([]),
    kalorien: int = Form(None),
    # Die List-Parameter kommen vom Form als mehrere Inputs mit gleichem name:
    # name="zutat_name" mehrfach -> zutat_name = ["Mehl", "Zucker", ...]
    zutat_menge: List[str] = Form([]),
    zutat_einheit: List[str] = Form([]),
    zutat_name: List[str] = Form([]),
    schritt_text: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    """Verarbeitet das Form-Submit beim Neuanlegen und schreibt das Rezept in die DB."""
    # Bild verarbeiten - leer wenn keines hochgeladen wurde
    bild_filename = ""
    if bild and bild.filename:
        bild_filename = save_recipe_image(bild)

    neues_rezept = Rezept(
        title=title,
        portionen=portionen,
        zubereitungszeit=zubereitungszeit,
        theme=theme,
        is_fav=False,
        bild=bild_filename,
        kalorien=kalorien,
    )

    # Zutaten zusammenbauen: zip() kombiniert die parallelen Listen
    # zu Tupeln (menge, einheit, name), enumerate() liefert dazu den Index.
    for i, (menge_str, einheit_str, name) in enumerate(zip(zutat_menge, zutat_einheit, zutat_name)):
        if not name.strip():
            continue
        einheit = Einheit(einheit_str)

        # Bei frei-Einheiten: Menge ignorieren, sonst parsen
        if einheit.value in EINHEITEN_OHNE_MENGE:
            menge = None
        else:
            # Komma-zu-Punkt-Konvertierung (Falls "0,5" statt "0.5")
            menge_clean = menge_str.replace(",", ".").strip()
            try:
                menge = float(menge_clean) if menge_clean else None
            except ValueError:
                # User hat was Nicht-Numerisches eingetippt (z.B. "sdf").
                # Statt zu crashen: Menge als None speichern.
                menge = None

        zutat = Zutat(name=name, menge=menge, einheit=einheit, position=i)
        neues_rezept.zutaten.append(zutat)

    # Schritte zusammenbauen
    for i, text in enumerate(schritt_text):
        if not text.strip():
            continue
        schritt = Schritt(text=text, position=i)
        neues_rezept.schritte.append(schritt)

    # Kategorien zusammenbauen
    for kat_name in kategorien:
        rk = RezeptKategorie(kategorie=kat_name)
        neues_rezept.kategorien_db.append(rk)

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

    # Theme-Farbe für die Karten-Optik der Edit-Seite holen
    try:
        aktuelle_theme_farbe = get_theme(rezept.theme).farbe
    except ValueError:
        aktuelle_theme_farbe = "#cccccc"

    return templates.TemplateResponse(
        request, "recipe_edit.html",
        {"rezept": rezept, "themes": THEMES, "kategorien": KATEGORIEN, "aktuelle_theme_farbe": aktuelle_theme_farbe}
    )


@app.post("/rezepte/{rezept_id}/edit")
def rezept_edit_speichern(
    rezept_id: int,
    title: str = Form(...),
    portionen: int = Form(...),
    zubereitungszeit: str = Form(""),
    theme: str = Form("Standard"),
    bild: UploadFile = File(None),
    kategorien: List[str] = Form([]),
    kalorien: int = Form(None),
    zutat_menge: List[str] = Form([]),
    zutat_einheit: List[str] = Form([]),
    zutat_name: List[str] = Form([]),
    schritt_text: List[str] = Form([]),
    db: Session = Depends(get_db),
):
    """
    Verarbeitet das Edit-Form-Submit.

    Strategie: Replace-All. Alle Zutaten, Schritte und Kategorien werden gelöscht
    und neu angelegt - statt zu mergen. Trade-off: einfacher Code, aber alte IDs
    gehen verloren. Für ein Familienprojekt akzeptabel.

    Beim Bild: nur ersetzen wenn ein neues hochgeladen wurde. Sonst bleibt das alte.
    """
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")

    # Neues Bild hochgeladen? Dann altes löschen und neuen Pfad setzen.
    # Kein Upload? Altes Bild bleibt unverändert.
    if bild and bild.filename:
        delete_recipe_image(rezept.bild)
        rezept.bild = save_recipe_image(bild)

    # Haupt-Felder updaten - SQLAlchemy trackt die Änderungen automatisch
    rezept.title = title
    rezept.portionen = portionen
    rezept.zubereitungszeit = zubereitungszeit
    rezept.theme = theme
    rezept.kalorien = kalorien

    # Alte Zutaten, Schritte und Kategorien raus. Dank cascade="all, delete-orphan"
    # werden die entsprechenden DB-Zeilen beim commit() gelöscht.
    rezept.zutaten.clear()
    rezept.schritte.clear()
    rezept.kategorien_db.clear()

    # Neue Zutaten anlegen
    for i, (menge_str, einheit_str, name) in enumerate(zip(zutat_menge, zutat_einheit, zutat_name)):
        if not name.strip():
            continue
        einheit = Einheit(einheit_str)

        # Bei frei-Einheiten: Menge ignorieren, sonst parsen
        if einheit.value in EINHEITEN_OHNE_MENGE:
            menge = None
        else:
            # Komma-zu-Punkt-Konvertierung (Falls "0,5" statt "0.5")
            menge_clean = menge_str.replace(",", ".").strip()
            try:
                menge = float(menge_clean) if menge_clean else None
            except ValueError:
                # User hat was Nicht-Numerisches eingetippt - Menge als None speichern.
                menge = None

        zutat = Zutat(
            name=name,
            menge=menge,
            einheit=einheit,
            position=i,
        )
        rezept.zutaten.append(zutat)

    # Neue Schritte anlegen
    for i, text in enumerate(schritt_text):
        if not text.strip():
            continue
        schritt = Schritt(text=text, position=i)
        rezept.schritte.append(schritt)

    # Neue Kategorien anlegen
    for kat_name in kategorien:
        rk = RezeptKategorie(kategorie=kat_name)
        rezept.kategorien_db.append(rk)

    db.commit()
    return RedirectResponse(url=f"/rezepte/{rezept_id}", status_code=303)


# ============================================================
# REZEPT LÖSCHEN (Delete)
# ============================================================

@app.post("/rezepte/{rezept_id}/loeschen")
def rezept_loeschen(rezept_id: int, db: Session = Depends(get_db)):
    """
    Löscht ein Rezept inkl. aller zugehörigen Zutaten/Schritte/Kategorie-Zuordnungen.

    Die abhängigen DB-Datensätze werden durch ON DELETE CASCADE im DB-Schema
    automatisch mitgelöscht. Das Bild aus dem Filesystem muss separat entfernt werden.
    """
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")

    # Bild-Datei aus dem Filesystem entfernen (falls vorhanden)
    delete_recipe_image(rezept.bild)

    db.delete(rezept)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


# ============================================================
# FAVORIT UMSCHALTEN
# ============================================================

@app.post("/rezepte/{rezept_id}/favorit")
def rezept_favorit_toggle(
    rezept_id: int,
    redirect_to: str = Form("/"),
    db: Session = Depends(get_db),
):
    """
    Schaltet den Favoriten-Status eines Rezepts um (True <-> False).

    redirect_to bestimmt, auf welche Seite nach dem Umschalten zurückgeleitet
    wird - das Formular schickt mit, von wo der Klick kam (Detail-Seite,
    Landing, Kategorie- oder Such-Seite).
    """
    rezept = db.get(Rezept, rezept_id)
    if rezept is None:
        raise HTTPException(status_code=404, detail="Rezept nicht gefunden")

    # Umschalten: aus True wird False, aus False wird True
    rezept.is_fav = not rezept.is_fav
    db.commit()

    # Sicherheitscheck: nur interne Pfade als Redirect-Ziel erlauben.
    # Verhindert, dass ein manipuliertes Formular auf eine fremde Seite umleitet
    # (sogenannter "Open Redirect").
    if not redirect_to.startswith("/"):
        redirect_to = "/"

    return RedirectResponse(url=redirect_to, status_code=303)


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