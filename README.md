# Familienrezepte
Selbst gehostete Web-App zur Sammlung und Verwaltung von Familienrezepten.
Geplant für den Einsatz auf einem Kühlschrank-Tablet oder im Heimnetzwerk.

Projektthema: Web-App mit Python + "KI-Unterstützung beim Coden, Segen oder Fluch?"

## Was die App kann
- Rezepte anlegen, bearbeiten, löschen, anzeigen
- Strukturierte Zutaten mit Menge, Einheit und optionaler Notiz
- Bilder hochladen (werden automatisch auf 1200px skaliert und als JPG gespeichert)
- Multi-Kategorie-Zuordnung pro Rezept
- Theme-Farben pro Rezept (Detail-Seite passt sich farblich an)
- Volltextsuche nach Rezept-Titel
- Kategorie-Übersichten

## Tech-Stack
- **Backend:** Python 3.13, FastAPI, SQLAlchemy ORM, Pillow für Bildbearbeitung
- **Frontend:** Jinja2-Templates, Bulma CSS (Grundgerüst), Custom CSS für eigenen Look
- **Datenbank:** MariaDB 11.x
- **Webserver:** Uvicorn (Entwicklung), geplant Gunicorn + Nginx (Produktion)

## Projektstruktur
```
rezepte-app/
├── app/                    Python-Anwendung
│   ├── main.py             FastAPI-Endpunkte
│   ├── database.py         DB-Verbindung und Session-Setup
│   ├── models.py           Domain-Modell (Kategorien, Themes, Einheiten)
│   ├── db_models.py        ORM-Modelle (Rezept, Zutat, Schritt, RezeptKategorie)
│   ├── crud.py             Lese-Operationen auf der DB
│   ├── file_upload.py      Bildupload-Logik (skalieren, speichern, löschen)
│   └── seed.py             Initial-Seed-Skript (auskommentiert, als Lerncode)
├── templates/              Jinja2-Templates
│   ├── base.html           Master-Template (Boilerplate)
│   ├── landing.html        Startseite
│   ├── recipe.html         Detail-Seite eines Rezepts
│   ├── recipe_form.html    Anlegen-Formular
│   ├── recipe_edit.html    Bearbeiten-Formular
│   ├── kategorie.html      Rezepte einer Kategorie
│   └── suche.html          Such-Ergebnisseite
├── static/css              Statische Assets
│   ├── style.css           nur noch @import-Anweisungen + :root-Variablen
│   ├── base.css            body, Typografie, globale Defaults
│   ├── topbar.css          recipe-topbar, page-topbar, alle Topbar-Varianten
│   ├── recipe-detail.css   recipe-card, hero, zutaten-list, schritte-list, tags
│   ├── overview.css        landing, kategorie-grid, rezept-grid, suche, kategorie-hero, empty-state
│   └── form.css            alles zum Rezept-Form (form-section, form-input, action-bar, kategorie-checkboxes)
├── static/js/              Skripte
│   ├── recipe_form.js      JavaScript für dynamische Form-Zeilen
├── img/                    Hochgeladene Rezept-Bilder
│   └── favicon.ico
├── schema.sql              DB-Schema (CREATE TABLE Statements)
├── requirements.txt        Python-Abhängigkeiten
├── .env.example            Vorlage für .env (DB-Verbindung)
└── README.md               Diese Datei
```

## Setup auf einem neuen Rechner
1. **Repository klonen**

   ```
   git clone https://github.com/DerTBM/rezepte-app
   cd rezepte-app
   ```

2. **Virtual Environment anlegen und Pakete installieren**

   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

   Falls PowerShell die Aktivierung mit Skript-Restriktionen blockiert:

   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **MariaDB einrichten**

   - MariaDB lokal installieren (https://mariadb.org/download/)
   - Datenbank `rezepte` anlegen (z.B. in HeidiSQL)
   - Schema einspielen:

     ```
     mariadb -u root -p rezepte < schema.sql
     ```

4. **Konfiguration**

   `.env.example` zu `.env` kopieren (im Projekt-Root, NICHT in `app/`!) und Passwort eintragen:

   ```
   DATABASE_URL=mysql+pymysql://root:DEIN_PASSWORT@127.0.0.1:3306/rezepte?charset=utf8mb4
   ```

5. **Bilder-Ordner anlegen**

   ```
   mkdir static\img
   ```

6. **Server starten**

   ```
   uvicorn app.main:app --reload
   ```

   Aufrufen im Browser: http://127.0.0.1:8000

## Aktueller Stand
Phase 6+ abgeschlossen. Implementiert:
- CRUD komplett (Create, Read, Update, Delete)
- Landing Page mit Kategorien-Grid und Suche
- Detail-Seite mit Theme-Farben und "Karten"-Look
- Kategorie-Seiten mit Kategorie-Farbe
- Such-Funktion (case-insensitive Titel-Match)
- Multi-Kategorie-Auswahl im Form
- Bildupload mit automatischer Skalierung (Pillow)
- Strukturierte Zutaten mit optionaler Notiz und erweiterten Einheiten (Prise, Schuss, etc.)
- Bruch-Anzeige (0.25 → "1/4")
- `base.html` als Master-Template (Template Inheritance)

## Geplant (Roadmap)
- Favoriten-UI (Flag `is_fav` existiert, UI fehlt)
- Zufallsrezept-Funktion auf Landing
- Form-Seiten optisch polieren (aktuell Bulma-Default)
- Phase 9: Deployment auf FritzBox/RaspberryPi mit Gunicorn + Nginx
- DB-Migrationen mit Alembic
- Automatische Backups
- Authentifizierung (aktuell offen für alle im Netzwerk)

## Daten-Sync zwischen Rechnern (DB-Dump)
Die DB läuft lokal pro Rechner. Um Rezepte zwischen Rechnern zu syncen:

### Auf dem Quell-Rechner (mit aktueller DB):
1. HeidiSQL öffnen, Rechtsklick auf `rezepte`-Datenbank
2. "Datenbank als SQL exportieren..."
3. Einstellungen: "Drop & Create" für Tabellen, "INSERT" für Daten, Ausgabe `data_dump.sql` im Projekt-Root
4. Im Git committen und pushen:

```
git add data_dump.sql
git commit -m "DB-Dump aktualisieren"
git push
```

### Auf dem Ziel-Rechner (alte DB überschreiben):
1. `git pull` im Projekt-Ordner
2. HeidiSQL: `rezepte`-Datenbank löschen, neu anlegen (utf8mb4_unicode_ci)
3. Datenbank aktivieren (Doppelklick)
4. "Datei → SQL-Datei laden..." → `data_dump.sql` ausführen

## Lizenz
Privat-Projekt, nicht für Veröffentlichung gedacht.
