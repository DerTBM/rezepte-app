/*
 * JavaScript für die dynamischen Zutat- und Schritt-Zeilen
 * im Rezept-Form (anlegen und bearbeiten).
 *
 * Wird sowohl von recipe_form.html als auch recipe_edit.html eingebunden.
 *
 * Globale Funktionen:
 *   - addZutat():    fügt eine neue leere Zutat-Zeile hinzu
 *   - addSchritt():  fügt eine neue leere Schritt-Zeile hinzu
 *
 * Beide werden über onclick-Handler im HTML aufgerufen.
 */


/**
 * Fügt eine neue leere Zutat-Zeile zum #zutaten-container hinzu.
 * Eine Zutat-Zeile besteht aus: Menge, Einheit-Dropdown, Name, Notiz, Lösch-Button.
 */
function addZutat() {
    const container = document.getElementById("zutaten-container");
    const div = document.createElement("div");
    div.className = "field is-grouped mb-2";
    div.innerHTML = `
        <div class="control">
            <input class="input" type="text" name="zutat_menge" placeholder="Menge">
        </div>
        <div class="control">
            <div class="select">
                <select name="zutat_einheit" required>
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
        <div class="control is-expanded">
            <input class="input" type="text" name="zutat_name" placeholder="Zutat" required>
        </div>
        <div class="control is-expanded">
            <input class="input" type="text" name="zutat_notiz" placeholder="Notiz (optional)">
        </div>
        <div class="control">
            <button type="button" class="button is-danger" onclick="this.closest('.field').remove()">×</button>
        </div>
    `;
    container.appendChild(div);
}


/**
 * Fügt eine neue leere Schritt-Zeile zum #schritte-container hinzu.
 */
function addSchritt() {
    const container = document.getElementById("schritte-container");
    const div = document.createElement("div");
    div.className = "field is-grouped mb-2";
    div.innerHTML = `
        <div class="control is-expanded">
            <input class="input" type="text" name="schritt_text" placeholder="Schrittbeschreibung" required>
        </div>
        <div class="control">
            <button type="button" class="button is-danger" onclick="this.closest('.field').remove()">×</button>
        </div>
    `;
    container.appendChild(div);
}