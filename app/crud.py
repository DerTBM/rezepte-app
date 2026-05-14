"""
CRUD-Operationen für Rezepte: alle DB-Zugriffe zentral hier.

CRUD = Create, Read, Update, Delete.
Aktuell sind hier nur die Read-Operationen drin (get_*, suche_*).
Die Create/Update/Delete-Operationen sind direkt in main.py in den Endpunkten,
weil sie eng mit der HTTP-Logik (Form-Daten verarbeiten, redirecten) verwoben sind.

Falls main.py später zu groß wird, kann man die hierher auslagern.
"""
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.db_models import Rezept, RezeptKategorie


def get_rezept(session: Session, rezept_id: int) -> Rezept | None:
    """Lädt ein einzelnes Rezept anhand seiner ID. Gibt None zurück wenn nicht gefunden."""
    return session.get(Rezept, rezept_id)


def get_alle_rezepte(session: Session) -> list[Rezept]:
    """Lädt alle Rezepte aus der DB, sortiert nach ID."""
    return session.scalars(select(Rezept).order_by(Rezept.id)).all()


def get_rezepte_nach_kategorie(session: Session, kategorie_name: str) -> list[Rezept]:
    """
    Lädt alle Rezepte, die einer bestimmten Kategorie zugeordnet sind.

    Nutzt einen JOIN auf die Junction-Tabelle rezept_kategorie - SQLAlchemy
    schreibt das SQL automatisch anhand der relationship-Definition.
    """
    return session.scalars(
        select(Rezept)
        .join(Rezept.kategorien_db)
        .where(RezeptKategorie.kategorie == kategorie_name)
        .order_by(Rezept.id)
    ).all()


def suche_rezepte(session: Session, suchbegriff: str) -> list[Rezept]:
    """
    Sucht Rezepte, deren Titel den Suchbegriff enthält (case-insensitive).

    ilike() statt like(): das 'i' macht den Vergleich Groß-/Kleinschreibung-egal.
    Das %-Zeichen sind SQL-Wildcards: %text% = 'text' irgendwo im String.
    """
    return session.scalars(
        select(Rezept)
        .where(Rezept.title.ilike(f"%{suchbegriff}%"))
        .order_by(Rezept.id)
    ).all()


def get_favoriten(session: Session) -> list[Rezept]:
    """Lädt alle als Favorit markierten Rezepte, sortiert nach ID."""
    return session.scalars(
        select(Rezept)
        .where(Rezept.is_fav == True)
        .order_by(Rezept.id)
    ).all()


def get_zufalls_rezepte(session: Session, anzahl: int) -> list[Rezept]:
    """
    Lädt eine zufällige Auswahl von Rezepten.

    func.rand() ist die SQL-Funktion für Zufallssortierung in MariaDB -
    die DB würfelt die Reihenfolge, wir nehmen die ersten 'anzahl' davon.
    Bei weniger Rezepten als 'anzahl' kommen einfach entsprechend weniger zurück.
    """
    return session.scalars(
        select(Rezept)
        .order_by(func.rand())
        .limit(anzahl)
    ).all()