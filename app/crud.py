from sqlalchemy.orm import Session
from app.db_models import Rezept 

def get_rezept(session: Session, rezept_id: int) -> Rezept | None:
    """Lädt ein Rezept anhand seiner ID. Gibt None zurück, wenn nicht gefunden."""
    return session.get(Rezept, rezept_id)

def get_alle_rezepte(session: Session) -> list[Rezept]:
    """Lädt alle Rezepte, sortiert nach ID."""
    from sqlalchemy import select
    return session.scalars(select(Rezept).order_by(Rezept.id)).all()

def get_rezepte_nach_kategorie(session: Session, kategorie_name: str) -> list[Rezept]:
    """Lädt alle Rezepte einer bestimmten Kategorie."""
    from sqlalchemy import select
    from app.db_models import RezeptKategorie
    return session.scalars(
        select(Rezept)
        .join(Rezept.kategorien_db)
        .where(RezeptKategorie.kategorie == kategorie_name)
        .order_by(Rezept.id)
    ).all()

def suche_rezepte(session: Session, suchbegriff: str) -> list[Rezept]:
    """Sucht Rezepte, deren Titel den Suchbegriff entählt (case-insensitive)"""
    from sqlalchemy import select
    return session.scalars(
        select(Rezept)
        .where(Rezept.title.ilike(f"%{suchbegriff}%"))
        .order_by(Rezept.id)
    ).all()