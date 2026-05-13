"""
ORM-Modelle: bilden die Datenbank-Tabellen als Python-Klassen ab.

SQLAlchemy übersetzt zwischen diesen Klassen und den SQL-Tabellen automatisch.
Das Schema selbst (CREATE TABLE) liegt in schema.sql - die Klassen hier
müssen mit dem Schema übereinstimmen.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.models import Einheit  # Enum für die einheit-Spalte


class Rezept(Base):
    """Haupt-Entität: ein Rezept mit allen Metadaten."""
    __tablename__ = "rezept"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    portionen = Column(Integer, nullable=False, default=2)
    zubereitungszeit = Column(String(100))
    bild = Column(String(255))
    is_fav = Column(Boolean, nullable=False, default=False)
    # Theme als String gespeichert, Lookup auf Theme-Objekt passiert in Python (models.py)
    theme = Column(String(50), nullable=False, default="Standard")
    # Audit-Spalten - DB setzt die Werte selbst beim INSERT/UPDATE
    erstellt = Column(DateTime, server_default=func.now())
    aktualisiert = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Beziehungen zu den abhängigen Tabellen.
    # cascade="all, delete-orphan": beim Löschen des Rezepts werden Zutaten/Schritte/
    # Kategorien automatisch mitgelöscht. Verhindert verwaiste Datensätze.
    zutaten = relationship("Zutat", back_populates="rezept", cascade="all, delete-orphan")
    schritte = relationship("Schritt", back_populates="rezept", cascade="all, delete-orphan")
    kategorien_db = relationship("RezeptKategorie", back_populates="rezept", cascade="all, delete-orphan")


class Zutat(Base):
    """Eine einzelne Zutat eines Rezepts (Menge + Einheit + Name)."""
    __tablename__ = "zutat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rezept_id = Column(Integer, ForeignKey("rezept.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    menge = Column(DECIMAL(8, 2), nullable=False)
    # values_callable: speichert den Enum-Wert ("g") statt des Namens ("GRAMM"),
    # passend zum ENUM-Typ in der DB-Tabelle
    einheit = Column(SQLEnum(Einheit, values_callable=lambda x: [e.value for e in x]), nullable=False)
    # Position bestimmt die Reihenfolge in der UI (Drag-and-Drop später möglich)
    position = Column(Integer, nullable=False, default=0)

    rezept = relationship("Rezept", back_populates="zutaten")


class Schritt(Base):
    """Ein einzelner Zubereitungsschritt mit Position und Text."""
    __tablename__ = "schritt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rezept_id = Column(Integer, ForeignKey("rezept.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    rezept = relationship("Rezept", back_populates="schritte")


class RezeptKategorie(Base):
    """
    Junction-Tabelle für die n:m-Beziehung zwischen Rezept und Kategorie.

    Kategorie ist als String gespeichert (nicht als Foreign Key auf eine Kategorie-Tabelle),
    weil Kategorien hardcoded in models.py leben - keine eigene DB-Tabelle nötig.
    Trade-off: Bei Umbenennung einer Kategorie müssen Daten manuell migriert werden.
    """
    __tablename__ = "rezept_kategorie"

    rezept_id = Column(Integer, ForeignKey("rezept.id", ondelete="CASCADE"), primary_key=True)
    kategorie = Column(String(50), primary_key=True)

    rezept = relationship("Rezept", back_populates="kategorien_db")