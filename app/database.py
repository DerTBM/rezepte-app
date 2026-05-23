"""
Datenbank-Setup für die Rezepte-App.

Stellt die Verbindung zur MariaDB her, definiert die SQLAlchemy-Session
und die Base-Klasse für ORM-Modelle.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env-Datei aus dem Projekt-Root laden (DATABASE_URL kommt da raus)
load_dotenv()

# Verbindungs-URL aus Umgebungsvariable holen.
# Format: mysql+pymysql://user:passwort@host:port/datenbank?charset=utf8mb4
DATABASE_URL = os.getenv("DATABASE_URL")

# Fail-Fast: Wenn die .env fehlt oder DATABASE_URL nicht gesetzt ist,
# direkt einen klaren Fehler werfen statt später kryptische DB-Errors zu kriegen
if DATABASE_URL is None:
    raise RuntimeError(
        "DATABASE_URL nicht gesetzt. Lege eine .env Datei an (siehe .env.example)"
    )

# Engine ist SQLAlchemys Verbindungsmanager.
# echo=True schreibt jede SQL-Query ins Terminal - sehr nützlich beim Lernen,
# in Produktion abschalten (oder Logging anders konfigurieren)
# echo=False: SQL-Queries werden NICHT mehr ins Terminal geschrieben.
# pool_pre_ping=True: SQLAlchemy prüft vor jedem Request ob die Verbindung
# noch lebt. Ist sie eingeschlafen (MariaDB-Timeout), wird sie automatisch
# neu aufgebaut statt einen OperationalError zu werfen.
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# SessionLocal ist eine Fabrik für DB-Sessions.
# Eine Session ist eine Arbeitseinheit: Daten abfragen, ändern, dann commit/rollback.
# autocommit=False: Änderungen werden erst beim expliziten commit() geschrieben
# autoflush=False: Änderungen werden nicht automatisch vor jeder Query gesynct
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base-Klasse, von der alle ORM-Klassen (Rezept, Zutat, etc.) erben werden.
# SQLAlchemy nutzt diese als Wurzel für sein internes Mapping zwischen Klassen und Tabellen.
Base = declarative_base()


# Verbindungstest beim direkten Ausführen der Datei: python app/database.py
if __name__ == "__main__":
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text("SELECT 1"))
        print("Verbindung OK:", result.scalar())