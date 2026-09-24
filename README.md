# HaFaReFi - Rezepte-App

Selbst gehostete Web-App zur Verwaltung von Familienrezepten.

> Dieses Projekt entstand im Rahmen eines Ausbildungsprojekts zum Thema **„Coding mit KI"**
> Schwerpunkt war der kritische, reflektierte Umgang mit KI-Assistenz beim Entwickeln.

---

## Was die App kann

- Rezepte anlegen, bearbeiten, löschen, anzeigen
- Strukturierte Zutaten mit Menge, Einheit und Name (getrennte Felder)
- Zutaten und Schritte per Drag-and-Drop sortieren
- Bilder hochladen (automatisch auf 1200px skaliert, als JPG gespeichert)
- Multi-Kategorie-Zuordnung pro Rezept
- Theme-Farben pro Rezept (Detail-Seite passt sich farblich an)
- Portionsskalierung live auf der Detail-Seite (Zutatenmengen passen sich an)
- Kalorienangabe pro Rezept (optional)
- Favoriten markieren und gefiltert anzeigen
- Zufallsrezept-Vorschläge auf der Startseite
- Volltextsuche nach Rezept-Titel
- Kategorie-Übersichten
- Eigene 404-Seite
- Admin-Authentifizierung (Schreibzugriff geschützt)

---

## Tech-Stack

| Schicht | Technologie |
|---|---|
| Sprache | Python 3.13 |
| Web-Framework | FastAPI |
| Template-Engine | Jinja2 |
| Gestaltung | Bulma (Grundgerüst) + eigenes CSS |
| Datenbank | MariaDB 11.x |
| DB-Zugriff | SQLAlchemy ORM |
| Bildbearbeitung | Pillow |
| Application-Server | Gunicorn + Uvicorn-Worker |
| Reverse-Proxy | Nginx |
| Dienstverwaltung | systemd |
| Versionsverwaltung | Git / GitHub |

---

## Projektstruktur

```
rezepte-app/
├── app/
│   ├── main.py             FastAPI-App, alle HTTP-Endpunkte
│   ├── database.py         DB-Verbindung und Session-Setup
│   ├── models.py           Domain-Modell (Kategorien, Themes, Einheiten)
│   ├── db_models.py        ORM-Modelle (Rezept, Zutat, Schritt, RezeptKategorie)
│   ├── crud.py             Lese-Operationen auf der DB
│   ├── file_upload.py      Bildupload-Logik (skalieren, speichern, löschen)
│   └── __init__.py
├── templates/
│   ├── base.html           Master-Template
│   ├── landing.html        Startseite
│   ├── recipe.html         Detail-Seite
│   ├── recipe_form.html    Neu-Anlegen-Formular
│   ├── recipe_edit.html    Bearbeiten-Formular
│   ├── _rezept_kachel.html Wiederverwendbare Kachel-Komponente
│   ├── kategorie.html      Kategorie-Übersicht
│   ├── suche.html          Suchergebnisse
│   └── 404.html            Fehlerseite
├── static/
│   ├── css/
│   │   ├── style.css           @import-Einstiegsdatei + :root-Variablen
│   │   ├── base.css            Body, Typografie, Layout-Container
│   │   ├── topbar.css          Topbars und Navigations-Elemente
│   │   ├── recipe-detail.css   Detail-Seite, Karten-Look, Zutaten, Schritte
│   │   ├── overview.css        Landing, Kategorie-Grid, Rezept-Grid, Suche
│   │   └── form.css            Rezept-Formular (Felder, Action-Bar, Checkboxen)
│   ├── js/
│   │   ├── recipe_form.js      Dynamische Formular-Zeilen, Drag-and-Drop
│   │   ├── recipe_detail.js    Portionsskalierung auf der Detail-Seite
│   │   └── Sortable.min.js     SortableJS (Drag-and-Drop-Library)
│   ├── img/                    Hochgeladene Rezeptbilder (nicht in Git)
│   └── favicon.ico
├── schema.sql              DB-Schema (CREATE TABLE)
├── requirements.txt        Python-Abhängigkeiten
├── .env.example            Vorlage für .env
└── README.md
```

## Bekannte Einschränkungen (bewusste Entscheidungen)

| Thema | Status | Begründung |
|---|---|---|
| HTTPS | nicht umgesetzt | App läuft nur im Heimnetz |
| Benutzerverwaltung | eine Admin-Auth via `.env` | Familienprojekt, reicht aus |
| Automatisierte Tests | nicht umgesetzt | Für diesen Umfang unverhältnismäßig |
| Off-Device-Backup | nicht umgesetzt | Bewusst zurückgestellt |
| DB-Migrationen (Alembic) | nicht umgesetzt | Schema-Änderungen manuell per ALTER TABLE |

---

## Lizenz

Privat-Projekt, nicht für Veröffentlichung & Weiterverbreitung gedacht.
