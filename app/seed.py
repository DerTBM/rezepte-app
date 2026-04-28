from app.database import SessionLocal
from app.db_models import Rezept, Zutat, Schritt, RezeptKategorie
from app.models import Einheit

def seed():
    # Eine Session öffnen)
    session = SessionLocal()

    try:
        # Rezept-Objekt bauen, mit allen Beziehungen drin
        ofgy = Rezept(
            title="Ofengyros",
            portionen=2,
            zubereitungszeit="40 Minuten + 10 Minuten Gehzeit",
            bild="ofgy.jpg",
            is_fav=True,
            theme="Abendessen",
            zutaten=[
                Zutat(name="Kartoffeln", menge=200, einheit=Einheit.GRAMM, position=0),
                Zutat(name="Gyros", menge=402, einheit=Einheit.GRAMM, position=1),
                Zutat(name="Paprika", menge=2, einheit=Einheit.STUECK, position=2),
            ],
            schritte=[
                Schritt(text="Kartoffeln schneiden.", position=0),
                Schritt(text="Alles aufs Blech packen.", position=1),
                Schritt(text="Backen.", position=2),
            ],
            kategorien_db=[
                RezeptKategorie(kategorie="Abendessen"),
                RezeptKategorie(kategorie="Schwein"),
            ],
        )

        # Rezept zur Session hinzufügen und committen
        session.add(ofgy)
        session.commit()

        print(f"Rezept gespeichert mit ID: {ofgy.id}")

    except Exception as e:
        session.rollback()
        print(f"Fehler beim Speichern {e}")
        raise 
    finally:
        session.close()

if __name__ == "__main__":
    seed()