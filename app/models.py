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
    Kategorie(name="Abendessen", farbe="#a594a8"),
    Kategorie(name="Schwein", farbe="#f3c3d2"),
    Kategorie(name="Rind", farbe="#f99374"),
    Kategorie(name="Geflügel", farbe="#cbe0ed"),
    Kategorie(name="Sonstiges Fleisch", farbe="#539da3"),
    Kategorie(name="Fisch", farbe="#3ea1ce"),
    Kategorie(name="Vegan/Vegetarisch", farbe="#6aa93e"),
    Kategorie(name="Desserts & Getränke", farbe="#e7aede"),
    Kategorie(name="Kuchen & Torten", farbe="#cc8335"),
    Kategorie(name="Festtagsessen", farbe="#ca1103"),
]

# Feste Liste aller verfügbaren Themes.
# 'Standard' ist der Default für neue Rezepte ohne spezifisches Theme.
THEMES = [
    Theme(name="Standard", farbe="#cccccc"),
    Theme(name="Abendessen", farbe="#a594a8"),
    Theme(name="Schwein", farbe="#f3c3d2"),
    Theme(name="Rind", farbe="#f99374"),
    Theme(name="Geflügel", farbe="#cbe0ed"),
    Theme(name="Sonstiges Fleisch", farbe="#539da3"),
    Theme(name="Fisch", farbe="#3ea1ce"),
    Theme(name="Vegan/Vegetarisch", farbe="#6aa93e"),
    Theme(name="Desserts & Getränke", farbe="#e7aede"),
    Theme(name="Kuchen & Torten", farbe="#cc8335"),
    Theme(name="Ostern", farbe="#99cb38"),
    Theme(name="Weihnachten", farbe="#ca1103"),
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