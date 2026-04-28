import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env-Datei aus dem Projekt-Root laden
load_dotenv()

# Verbindungs-URL aus Umgebungsvariable holen
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError(
        "DATABASE_URL nicht gesetzt. Lege eine .env Datei an (siehe .env.example)"
    )

# Engine ist der Verbindungsmanager. SQLAlchemy nutzt den für alle DB-Aktionen.
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal ist eine Fabrik für Datenbank-Sessions.
# Eine Session ist eine Arbeits-Einheit: Daten abfragen ändern, commit/rollback

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base-Klasse, von der alle ORM-Klassen erben werden.
Base = declarative_base()

if __name__ == "__main__":
    # Kurzer Verbindungstest
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text("SELECT 1"))
        print("Verbindung OK:", result.scalar())