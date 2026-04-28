from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, DECIMAL, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models import Einheit # Bestehende Enum in models.py weiter nutzen

class Rezept(Base):
    __tablename__ = "rezept"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    portionen = Column(Integer, nullable=False, default=2)
    zubereitungszeit = Column(String(100))
    bild = Column(String(255))
    is_fav = Column(Boolean, nullable=False, default=False)
    theme = Column(String(50), nullable=False, default="Standard")
    erstellt = Column(DateTime, server_default=func.now())
    aktualisiert = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Beziehung zu anderen Tabellen
    zutaten = relationship("Zutat", back_populates="rezept", cascade="all, delete-orphan")
    schritte = relationship("Schritt", back_populates="rezept", cascade="all, delete-orphan")
    kategorien_db = relationship("RezeptKategorie", back_populates="rezept", cascade="all, delete-orphan")

class Zutat(Base):
    __tablename__ = "zutat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rezept_id = Column(Integer, ForeignKey("rezept.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    menge = Column(DECIMAL(8,2), nullable=False)
    einheit = Column(SQLEnum(Einheit, values_callable=lambda x: [e.value for e in x]), nullable=False)
    position = Column(Integer, nullable=False, default=0)

    rezept = relationship("Rezept", back_populates="zutaten")

class Schritt(Base):
    __tablename__ = "schritt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rezept_id = Column(Integer, ForeignKey("rezept.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)

    rezept = relationship("Rezept", back_populates="schritte")

class RezeptKategorie(Base):
    __tablename__ = "rezept_kategorie"

    rezept_id = Column(Integer, ForeignKey("rezept.id", ondelete="CASCADE"), primary_key=True)
    kategorie = Column(String(50), primary_key=True)

    rezept = relationship("Rezept", back_populates="kategorien_db")