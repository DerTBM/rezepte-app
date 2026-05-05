from enum import Enum
from dataclasses import dataclass


class Einheit(Enum):
    KILOGRAMM = "kg"
    GRAMM = "g"
    LITER = "l"
    MILLILITER = "ml"
    ESSLOEFFEL = "EL"
    TEELOEFFEL = "TL"
    STUECK = "Stk"


@dataclass
class Kategorie:
    name: str
    farbe: str


@dataclass
class Theme:
    name: str
    farbe: str


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
    for k in KATEGORIEN:
        if k.name == name:
            return k
    raise ValueError(f"Kategorie '{name}' nicht gefunden")


def get_theme(name: str) -> Theme:
    for t in THEMES:
        if t.name == name:
            return t
    raise ValueError(f"Theme '{name}' nicht gefunden")