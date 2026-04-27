from enum import Enum
from dataclasses import dataclass

# Erst die primitiven Klassen
@dataclass
class Schritt:
    text: str

@dataclass
class Kategorie:
    name: str
    farbe: str

@dataclass
class Theme:
    name: str
    farbe: str


class Einheit(Enum):
    KILOGRAMM = "kg"
    GRAMM = "g"
    LITER = "l"
    MILLILITER = "ml"
    ESSLOEFFEL = "EL"
    TEELOEFFEL = "TL"
    STUECK = "Stk"

@dataclass
class Zutat:
    name: str
    menge: float
    einheit: Einheit

@dataclass
class Rezept: # Ans Ende weil Python von oben nach unten liest und erst Zutat, Schritt, Kategorie braucht
    title: str
    is_fav: bool
    time: str
    zutaten: list[Zutat] # Eine Liste von Zutat-Objekten
    schritte: list[Schritt] # Eine Liste von Schritt-Objekten
    kategorien: list[Kategorie] # Eine Liste von Kategorie-Objekten, Plural weil Multi-Select
    theme: Theme
    portion: int
    bild: str

KATEGORIEN = [
    Kategorie(name="Abendessen", farbe="#fff"),
    Kategorie(name="Schwein", farbe="#fff"),
    Kategorie(name="Rind", farbe="#fff"),
    Kategorie(name="Geflügel", farbe="#fff"),
    Kategorie(name="Sonstiges Fleisch", farbe="#fff"),
    Kategorie(name="Fisch", farbe="#fff"),
    Kategorie(name="Vegan/Vegetarisch", farbe="#99cb38"),
    Kategorie(name="Desserts & Getränke", farbe="#fff"),
    Kategorie(name="Kuchen & Torten", farbe="#fff"),
    Kategorie(name="Festtagsessen", farbe="#fff"),
    Kategorie(name="Sous Vide", farbe="#fff"),
]

THEMES = [
    Theme(name="Abendessen", farbe="#fff"),
    Theme(name="Schwein", farbe="#fff"),
    Theme(name="Rind", farbe="#fff"),
    Theme(name="Geflügel", farbe="#fff"),
    Theme(name="Sonstiges Fleisch", farbe="#fff"),
    Theme(name="Fisch", farbe="#fff"),
    Theme(name="Vegan/Vegetarisch", farbe="#99cb38"),
    Theme(name="Desserts & Getränke", farbe="#fff"),
    Theme(name="Kuchen & Torten", farbe="#fff"),
    Theme(name="Ostern", farbe="#fff"),
    Theme(name="Weihnachten", farbe="#fff"),
    Theme(name="Special", farbe="#fff"),
]

def get_kategorie(name: str) -> Kategorie:
    for k in KATEGORIEN:
        if k.name == name:
            return k
    raise ValueError(f"Kategorie '{name}' nicht gefunden")

def get_theme(name: str) -> Theme:
    for t in THEMES:
        if t.name == name:
            return t
    raise ValueError(f"Theme '{name}' nicht gefunden")

# Test: Rezept im Speicher konstruieren
ofgy = Rezept(
    title="Ofengyros",
    is_fav=True,
    time="40 Minuten",
    zutaten=[
        Zutat(name="Kartoffeln", menge=200, einheit=Einheit.GRAMM),
        Zutat(name="Gyros", menge=402, einheit=Einheit.GRAMM),
        Zutat(name="Paprika", menge=2, einheit=Einheit.STUECK),
    ],
    schritte=[
        Schritt(text="Kartoffeln schneiden."),
        Schritt(text="Alles aufs Blech packen."),
        Schritt(text="Backen"),
    ],
    kategorien=[get_kategorie("Abendessen"), get_kategorie("Schwein")],  # Sollte Abendessen und Schwein sein
    theme=get_theme("Abendessen"),              # Sollte Abendessen sein
    portion=2,
    bild="ofgy.jpg",
)

print(ofgy)
print(ofgy.kategorien)