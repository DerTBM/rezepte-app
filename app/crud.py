from sqlalchemy.orm import Session
from app.db_models import Rezept 

def get_rezept(session: Session, rezept_id: int) -> Rezept | None:
    """Lädt ein Rezept anhand seiner ID. Gibt None zurück, wenn nicht gefunden."""
    return session.get(Rezept, rezept_id)