"""
Hilfsfunktion für Bilduploads.

Bilder werden in static/img/ gespeichert mit eindeutigem Dateinamen,
auf maximale Breite skaliert und als JPG umgewandelt.
"""
import uuid 
from pathlib import Path
from PIL import Image 
from fastapi import UploadFile

# Zielordner für Bilder (relativ zum Projekt-Root)
UPLOAD_DIR = Path("static/img")

# Maximale Breite in Pixeln - Bilder werden runterskaliert wenn größer.
# 1200px reicht für die Detail-Seite (Bild ist dort max. ~500px breit, mit Retina ~1000px).
MAX_WIDTH = 1200

def save_recipe_image(upload: UploadFile) -> str: 
    """
    Speichert eine hochgeladenes Bild im static/img-Ordner.

    - Generiert einen zufälligen Dateinamen (UUID) um Kollisionen zu vermeiden
    - Skaliert das BIld auf maximal MAX_WIDTH herunter (Aspect Ratio bleibt)
    - Wandelt alles in JPG um (kleiner als PNG bei Fotos)

    Returns:
        Dateiname (nur der Name, kein Pfad), z.B. "a3f9c2.jpg"
        Wird in rezept-bild gespeichert. Anzeige im Teplate:
        /static/img/{rezept.bild}
    """
    # Sicherstellen, dass der Ordner existiert
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Eindeutigen Dateinamen generieren (kurze UUID)
    # Originaler Dateiname wird verworfen - vermeidet Sonderzeichen-Probleme
    # und schützt vor Path-Traversal-Angriffen ("../../etc/passwd" als Name)
    filename = f"{uuid.uuid4().hex[:12]}.jpg"
    filepath = UPLOAD_DIR / filename

    # Bild öffnen und ggf. skalieren
    img = Image.open(upload.file) 

    # Modus konvertieren, falls nötig (z.B. PNG mit Alpha-Kanal -> RGB für JPG)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    # Skalieren wenn breiter als MAX_WIDTH. Höhe wird proportional angepasst.
    if img.width > MAX_WIDTH:
        new_height = int(img.height * MAX_WIDTH / img.width)
        # LANCZOS ist ein hochwertiger Resize-Algo, ideal für Fotos
        img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

    # Als JPG speichern mit gutem Qualitäts/Größenkompromiss
    img.save(filepath, "JPEG", quality=85, optimize=True)

    return filename

def delete_recipe_image(filename: str) -> None:
    """
    Löscht ein Bild aus dem static/img-Ordner.
    """
    if not filename:
        return
    filepath = UPLOAD_DIR / filename
    filepath.unlink(missing_ok=True)