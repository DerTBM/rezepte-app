# Rezepte-App

Self-hosted Web-App für Familienrezepte. Aktuell in Entwicklung.

## Setup

1. Repository klonen
2. Virtual Environment erstellen und aktivieren

## Datenbank-Setup

1. MariaDB installieren
2. Datenbank anlegen:
```sql
   CREATE DATABASE rezepte CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
3. Schema einlesen:
mariadb -u root -p rezepte < schema.sql

## Aktueller Stand

- Datenmodell mit dataclasses (app/models.py)
- ORM-Modelle mit SQLAlchemy (app/db_models.py)
- DB-Schema in schema.sql
- FastAPI mit /rezepte/{id}-Route, lädt aus MariaDB und rendert HTML
- Bulma-Styling, Theme-Farben pro Rezept
- Seed-Skript: `python -m app.seed`

## Nächste Schritte

- CRUD Create/Update/Delete (Anlegen/Editieren/Löschen über UI)
- Bildupload
- Kategorie- und Theme-Verwaltung im Frontend
- Deployment

## Setup zuhause

1. Repository klonen
2. Virtual Environment:
```python
-m venv .venv
..venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
3. MariaDB installieren, Datenbank `rezepte` anlegen
4. `.env.example` zu `.env` kopieren, Passwort eintragen
5. Schema einlesen:
```
mariadb -u root -p rezepte < schema.sql
```
6. Test-Daten einfüllen:
```
python -m app.seed
```
7. Server starten:
```
uvicorn app.main:app --reload
```