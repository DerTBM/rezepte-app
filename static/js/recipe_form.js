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
                    <option value="Schuss">Schuss</option>
                    <option value="Bund">Bund</option>
                    <option value="Zehe">Zehe</option>
                    <option value="Dose">Dose</option>
                    <option value="Pck.">Pck.</option>
                    <option value="etwas">etwas</option>
                    <option value="n. Geschmack">n. Geschmack</option>
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