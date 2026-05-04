from sqlalchemy.orm import Session
from app.db_models import Rezept 

def get_rezept(session: Session, rezept_id: int) -> Rezept | None:
    """Lädt ein Rezept anhand seiner ID. Gibt None zurück, wenn nicht gefunden."""
    return session.get(Rezept, rezept_id)

def get_alle_rezepte(session: Session) -> list[Rezept]:
    """Lädt alle Rezepte, sortiert nach ID."""
    from sqlalchemy import select
    return session.scalars(select(Rezept).order_by(Rezept.id)).all()