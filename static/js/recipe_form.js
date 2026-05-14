/*
 * JavaScript für die dynamischen Zutat- und Schritt-Zeilen
 * im Rezept-Form (anlegen und bearbeiten).
 *
 * Globale Funktionen:
 *   - addZutat():    fügt eine neue leere Zutat-Zeile hinzu
 *   - addSchritt():  fügt eine neue leere Schritt-Zeile hinzu
 *
 * Beide werden über onclick-Handler im HTML aufgerufen.
 */

/**
 * Fügt eine neue leere Zutat-Zeile zum #zutaten-container hinzu.
 */
function addZutat() {
    const container = document.getElementById("zutaten-container");
    const div = document.createElement("div");
    div.className = "form-row-card";
    div.innerHTML = `
        <div class="form-field">
            <input class="form-input" type="text" name="zutat_menge" placeholder="Menge">
        </div>
        <div class="form-field">
            <div class="form-select-wrapper">
                <select class="form-select" name="zutat_einheit" required>
                    <option value="g">g</option>
                    <option value="kg">kg</option>
                    <option value="ml">ml</option>
                    <option value="cl">cl</option>
                    <option value="l">l</option>
                    <option value="EL">EL</option>
                    <option value="TL">TL</option>
                    <option value="Stk">Stk</option>
                    <option value="Prise">Prise</option>
                    <option value="Msp.">Msp.</option>
                    <option value="Schuss">Schuss</option>
                    <option value="Bund">Bund</option>
                    <option value="Zehe/n">Zehe/n</option>
                    <option value="Dose">Dose</option>
                    <option value="Pck.">Pck.</option>
                    <option value="etwas">etwas</option>
                    <option value="...">...</option>
                </select>
            </div>
        </div>
        <div class="form-field form-field-expand">
            <input class="form-input" type="text" name="zutat_name" placeholder="Zutat" required>
        </div>
        <div class="form-field form-field-expand">
            <input class="form-input" type="text" name="zutat_notiz" placeholder="Notiz (optional)">
        </div>
        <button type="button" class="form-remove-button" onclick="this.closest('.form-row-card').remove()">×</button>
    `;
    container.appendChild(div);
}

/**
 * Fügt eine neue leere Schritt-Zeile zum #schritte-container hinzu.
 */
function addSchritt() {
    const container = document.getElementById("schritte-container");
    const div = document.createElement("div");
    div.className = "form-row-card";
    div.innerHTML = `
        <div class="form-field form-field-expand">
            <input class="form-input" type="text" name="schritt_text" placeholder="Schrittbeschreibung" required>
        </div>
        <button type="button" class="form-remove-button" onclick="this.closest('.form-row-card').remove()">×</button>
    `;
    container.appendChild(div);
}

/**
 * Zeigt eine Vorschau des gewählten Bildes, sobald der Nutzer
 * im Datei-Dialog eine Datei auswählt - noch vor dem Upload.
 *
 * Nutzt die FileReader-API: liest die lokal gewählte Datei als
 * Daten-URL ein und steckt sie direkt ins <img>-Tag. Kein
 * Server-Roundtrip nötig, alles passiert im Browser.
 *
 * @param {HTMLInputElement} input - das file-Input-Element
 */
function zeigeBildVorschau(input) {
    // input.files ist eine Liste - wir nehmen die erste (und einzige) Datei
    const datei = input.files[0];
    if (!datei) {
        return;  // Nutzer hat den Dialog abgebrochen, nichts zu tun
    }

    const container = document.getElementById("bild-vorschau-container");
    const vorschauBild = document.getElementById("bild-vorschau");
    const vorschauText = document.getElementById("bild-vorschau-text");

    // FileReader liest die Datei asynchron ein
    const reader = new FileReader();

    // onload feuert, sobald die Datei fertig eingelesen ist.
    // reader.result enthält dann die Datei als Daten-URL (base64).
    reader.onload = function (event) {
        vorschauBild.src = event.target.result;
        vorschauText.textContent = "Vorschau des neuen Bildes. Wird beim Speichern übernommen.";
        container.style.display = "";  // Container sichtbar machen (falls vorher versteckt)
    };

    // Lese-Vorgang starten - triggert am Ende das onload oben
    reader.readAsDataURL(datei);
}