"""
Hilfsfunktion für Bilduploads.

Bilder werden in static/img/ gespeichert mit eindeutigem Dateinamen,
auf maximale Breite skaliert und als JPG umgewandelt.
"""
import uuid
from pathlib import Path
from PIL import Image
from fastapi import UploadFile, HTTPException

# Zielordner für Bilder (relativ zum Projekt-Root)
UPLOAD_DIR = Path("static/img")

# Maximale Breite in Pixeln - Bilder werden runterskaliert wenn größer.
# 1200px reicht für die Detail-Seite (Bild ist dort max. ~500px breit, mit Retina ~1000px).
MAX_WIDTH = 1200

# Maximale Dateigröße eines Uploads in Bytes.
# 10 MB - schützt den Server davor, dass ein riesiges Handy-Foto
# den Speicher beim Verarbeiten überlastet.
MAX_FILE_SIZE = 10 * 1024 * 1024


def save_recipe_image(upload: UploadFile) -> str:
    """
    Speichert ein hochgeladenes Bild im static/img-Ordner.

    - Prüft die Dateigröße gegen MAX_FILE_SIZE
    - Generiert einen zufälligen Dateinamen (UUID) um Kollisionen zu vermeiden
    - Skaliert das Bild auf maximal MAX_WIDTH herunter (Aspect Ratio bleibt)
    - Wandelt alles in JPG um (kleiner als PNG bei Fotos)

    Returns:
        Dateiname (nur der Name, kein Pfad), z.B. "a3f9c2.jpg"
        Wird in rezept.bild gespeichert. Anzeige im Template:
        /static/img/{rezept.bild}

    Raises:
        HTTPException 413, wenn die Datei größer als MAX_FILE_SIZE ist.
    """
    # Dateigröße prüfen, BEVOR wir das Bild in den Speicher laden.
    # upload.file ist ein Datei-Objekt - wir springen ans Ende um die
    # Größe zu ermitteln, dann zurück an den Anfang.
    upload.file.seek(0, 2)          # 2 = ans Ende der Datei springen
    groesse = upload.file.tell()    # aktuelle Position = Dateigröße in Bytes
    upload.file.seek(0)             # zurück an den Anfang, sonst liest Pillow nichts

    if groesse > MAX_FILE_SIZE:
        # HTTP 413 = "Payload Too Large", der passende Statuscode dafür
        raise HTTPException(
            status_code=413,
            detail=f"Das Bild ist zu groß (max. {MAX_FILE_SIZE // (1024 * 1024)} MB).",
        )

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