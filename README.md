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

- Datenmodell vollständig (app/models.py)
- FastAPI-Server mit JSON- und HTML-Endpunkt
- Bulma als CSS-Framework
- DB-Schema in schema.sql, noch nicht in Python angebunden

## Nächste Schritte

- Python-Anbindung an MariaDB (SQLAlchemy)
- CRUD-Operationen für Rezepte
- Bildupload
- Deployment

