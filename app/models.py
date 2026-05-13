"""
Domain-Modell für Kategorien, Themes und Einheiten.

Diese Klassen leben rein in Python, nicht in der DB.
Sie sind hardcoded, weil sich Kategorien und Themes selten ändern und
nicht über die UI verwaltet werden müssen.

Wichtig: Das eigentliche Rezept-Modell für die DB liegt in db_models.py.
"""
from enum import Enum
from dataclasses import dataclass


class Einheit(Enum):
    """
    Erlaubte Mengeneinheiten für Zutaten.

    Wird sowohl in Python (Zutat-Klasse) als auch in der DB (zutat.einheit-Spalte)
    verwendet. Bei Änderung hier muss auch das ENUM in schema.sql angepasst werden,
    sonst gibt's einen DataError beim Schreiben in die DB.
    """
    KILOGRAMM = "kg"
    GRAMM = "g"
    LITER = "l"
    MILLILITER = "ml"
    ESSLOEFFEL = "EL"
    TEELOEFFEL = "TL"
    STUECK = "Stk"
    PRISE = "Prise"
    SCHUSS = "Schuss"
    BUND = "Bund"
    ZEHE = "Zehe"
    DOSE = "Dose"
    PACKUNG = "Pck."
    ETWAS = "etwas"
    NACH_GESCHMACK = "n. Geschmack"

@dataclass
class Kategorie:
    """Eine Kategorie wie 'Vegan' oder 'Schwein', mit zugehöriger Farbe für die UI."""
    name: str
    farbe: str


@dataclass
class Theme:
    """
    Ein visuelles Theme wie 'Weihnachten' oder 'Standard'.
    Bestimmt die Hintergrund- und Akzentfarbe einer Rezept-Detailseite.
    """
    name: str
    farbe: str


# Feste Liste aller verfügbaren Kategorien.
# Wird in der UI als Multi-Select-Auswahl angezeigt.
KATEGORIEN = [
    Kategorie(name="Abendessen", farbe="#84a59d"),
    Kategorie(name="Schwein", farbe="#ffcad4"),
    Kategorie(name="Rind", farbe="#c02f32"),
    Kategorie(name="Geflügel", farbe="#f6bd60"),
    Kategorie(name="Sonstiges Fleisch", farbe="#f4a261"),
    Kategorie(name="Fisch", farbe="#3ea1ce"),
    Kategorie(name="Vegan/Vegetarisch", farbe="#6aa93e"),
    Kategorie(name="Desserts & Getränke", farbe="#cfbaf0"),
    Kategorie(name="Kuchen & Torten", farbe="#f1c0e8"),
    Kategorie(name="Festtagsessen", farbe="#bf0603"),
    Kategorie(name="Sous Vide", farbe="#dad7cd"),
]

# Feste Liste aller verfügbaren Themes.C
# 'Standard' ist der Default für neue Rezepte ohne spezifisches Theme.
THEMES = [
    Theme(name="Standard", farbe="#001524"),
    Theme(name="Abendessen", farbe="#84a59d"),
    Theme(name="Schwein", farbe="#ffcad4"),
    Theme(name="Rind", farbe="#c02f32"),
    Theme(name="Geflügel", farbe="#f6bd60"),
    Theme(name="Sonstiges Fleisch", farbe="#f4a261"),
    Theme(name="Fisch", farbe="#3ea1ce"),
    Theme(name="Vegan/Vegetarisch", farbe="#6aa93e"),
    Theme(name="Desserts & Getränke", farbe="#cfbaf0"),
    Theme(name="Kuchen & Torten", farbe="#f1c0e8"),
    Theme(name="Ostern", farbe="#588157"),
    Theme(name="Weihnachten", farbe="#bf0603"),
    Theme(name="Special", farbe="#8e19fe"),
]


def get_kategorie(name: str) -> Kategorie:
    """Lookup einer Kategorie per Name. Wirft ValueError wenn nicht gefunden."""
    for k in KATEGORIEN:
        if k.name == name:
            return k
    raise ValueError(f"Kategorie '{name}' nicht gefunden")


def get_theme(name: str) -> Theme:
    """Lookup eines Themes per Name. Wirft ValueError wenn nicht gefunden."""
    for t in THEMES:
        if t.name == name:
            return t
    raise ValueError(f"Theme '{name}' nicht gefunden")

# Einheiten ohne konkrete Menge - bei diesen wird im Form die Mengen-Eingabe
# ausgeblendet und in der DB als NULL gespeichert.
EINHEITEN_OHNE_MENGE = {"etwas", "n. Geschmack"}


def menge_als_bruch(wert: float) -> str:
    """
    Wandelt eine Dezimalzahl in eine schön lesbare Form um.
    Häufige Brüche werden als 1/4, 1/2 etc. dargestellt,
    ganze Zahlen ohne Nachkommastellen, der Rest mit Dezimal.

    Beispiele:
        0.25 -> "1/4"
        0.5  -> "1/2"
        2.0  -> "2"
        1.5  -> "1 1/2"
        0.7  -> "0.7"
    """
    if wert is None:
        return ""

    # Ganze Zahlen ohne Nachkommastellen
    if wert == int(wert):
        return str(int(wert))

    # Ganzzahliger Teil und Bruchanteil separieren
    ganzes = int(wert)
    rest = round(wert - ganzes, 2)

    # Bekannte Brüche zuordnen
    bruch_map = {
        0.25: "1/4",
        0.33: "1/3",
        0.5: "1/2",
        0.67: "2/3",
        0.75: "3/4",
    }

    if rest in bruch_map:
        bruch_str = bruch_map[rest]
        # "1 1/2" wenn ganzer Teil > 0, sonst nur "1/2"
        return f"{ganzes} {bruch_str}" if ganzes > 0 else bruch_str

    # Fallback: Dezimal-Anzeige ohne Nullen am Ende
    return f"{wert:g}"