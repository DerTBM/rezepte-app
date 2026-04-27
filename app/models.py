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
    Kategorie(name="Sous Vide", farbe="#ffffff"),
]

THEMES = [
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
    for k in KATEGORIEN:
        if k.name == name:
            return k
    raise ValueError(f"Kategorie '{name}' nicht gefunden")

def get_theme(name: str) -> Theme:
    for t in THEMES:
        if t.name == name:
            return t
    raise ValueError(f"Theme '{name}' nicht gefunden")

def build_ofgy() -> Rezept:
    return Rezept(
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
    

if __name__ == "__main__":
    print(build_ofgy())