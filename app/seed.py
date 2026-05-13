"""
Seed-Skript: legt ein Test-Rezept (Ofengyros) in der Datenbank an.

NICHT MEHR AKTIV - Das Rezept ist längst in der DB.
Erneutes Ausführen würde ein zweites identisches Rezept anlegen.

Bleibt als Lern-Referenz: zeigt wie man mit SQLAlchemy ein verschachteltes
Objekt (Rezept mit Zutaten, Schritten, Kategorien) in einem Commit anlegt.
"""
# from app.database import SessionLocal
# from app.db_models import Rezept, Zutat, Schritt, RezeptKategorie
# from app.models import Einheit


# def seed():
#     # Eine Session öffnen
#     session = SessionLocal()
#     try:
#         # Rezept-Objekt bauen, mit allen Beziehungen direkt drin.
#         # Dank der relationship-Definitionen kann man hier Zutaten/Schritte/
#         # Kategorien direkt mitübergeben - SQLAlchemy macht die Foreign Keys selbst.
#         ofgy = Rezept(
#             title="Ofengyros",
#             portionen=2,
#             zubereitungszeit="40 Minuten + 10 Minuten Gehzeit",
#             bild="ofgy.jpg",
#             is_fav=True,
#             theme="Abendessen",
#             zutaten=[
#                 Zutat(name="Kartoffeln", menge=200, einheit=Einheit.GRAMM, position=0),
#                 Zutat(name="Gyros", menge=402, einheit=Einheit.GRAMM, position=1),
#                 Zutat(name="Paprika", menge=2, einheit=Einheit.STUECK, position=2),
#             ],
#             schritte=[
#                 Schritt(text="Kartoffeln schneiden.", position=0),
#                 Schritt(text="Alles aufs Blech packen.", position=1),
#                 Schritt(text="Backen.", position=2),
#             ],
#             kategorien_db=[
#                 RezeptKategorie(kategorie="Abendessen"),
#                 RezeptKategorie(kategorie="Schwein"),
#             ],
#         )

#         # add() merkt das Objekt vor, commit() schreibt's in einer Transaktion
#         session.add(ofgy)
#         session.commit()
#         print(f"Rezept gespeichert mit ID: {ofgy.id}")

#     except Exception as e:
#         # Bei Fehler: alle Änderungen zurückrollen
#         session.rollback()
#         print(f"Fehler beim Speichern {e}")
#         raise
#     finally:
#         # Session immer schließen, auch bei Exception
#         session.close()


# if __name__ == "__main__":
#     seed()