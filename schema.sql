-- Rezept-Tabelle: die Hauptdaten eines Rezepts
CREATE TABLE rezept (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    portion INT NOT NULL DEFAULT 2,
    time VARCHAR(100),
    bild VARCHAR(255),
    is_fav BOOLEAN NOT NULL DEFAULT FALSE,
    theme VARCHAR(50) NOT NULL DEFAULT 'Standard',
    erstellt DATETIME DEFAULT CURRENT_TIMESTAMP,
    aktualisiert DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Zutaten: gehören jeweils zu einem Rezept
CREATE TABLE zutat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rezept_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    menge DECIMAL(8,2) NOT NULL,
    einheit ENUM('kg', 'g', 'l', 'ml', 'EL', 'TL', 'Stk') NOT NULL,
    position INT NOT NULL DEFAULT 0,
    FOREIGN KEY (rezept_id) REFERENCES rezept(id) ON DELETE CASCADE
);

-- Schritte: gehören jeweils zu einem Rezept, mit Reihenfolge
CREATE TABLE schritt (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rezept_id INT NOT NULL,
    position INT NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (rezept_id) REFERENCES rezept(id) ON DELETE CASCADE
);

-- Junction Table: Rezept zu Kategorien (n:m), Kategorie als String
CREATE TABLE rezept_kategorie (
    rezept_id INT NOT NULL,
    kategorie VARCHAR(50) NOT NULL,
    PRIMARY KEY (rezept_id, kategorie),
    FOREIGN KEY (rezept_id) REFERENCES rezept(id) ON DELETE CASCADE
);