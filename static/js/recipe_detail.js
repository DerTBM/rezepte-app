/**
 * Interaktivität für die Rezept-Detail-Seite.
 */

function mengeAlsBruch(wert) {
    if (wert === null || wert === undefined) return "";
    if (wert === Math.floor(wert)) return String(Math.floor(wert));

    const ganzes = Math.floor(wert);
    const rest = Math.round((wert - ganzes) * 100) / 100;

    const bruchMap = {
        0.25: "1/4", 0.33: "1/3", 0.5: "1/2",
        0.67: "2/3", 0.75: "3/4"
    };

    if (bruchMap[rest]) {
        const bruch = bruchMap[rest];
        return ganzes > 0 ? `${ganzes} ${bruch}` : bruch;
    }
    return String(Math.round(wert * 10) / 10);
}

function aktualisiereZutaten(faktor) {
    document.querySelectorAll(".zutaten-menge[data-original]").forEach(el => {
        const original = parseFloat(el.dataset.original);
        const einheit = el.dataset.einheit;
        const neu = original * faktor;
        const neuFormatiert = mengeAlsBruch(neu);

        if (einheit === "...") {
            el.textContent = neuFormatiert;
        } else {
            el.textContent = neuFormatiert + " " + einheit;
        }
    });
}

// DOMContentLoaded: erst ausführen wenn die Seite fertig geladen ist
document.addEventListener("DOMContentLoaded", () => {
    const portionenEl = document.getElementById("portionen-aktuell");
    if (!portionenEl) return; // Sicherheit falls mal auf anderer Seite geladen

    const originalPortionen = parseInt(portionenEl.dataset.original);

    document.getElementById("portionen-plus").addEventListener("click", () => {
        const aktuell = parseInt(portionenEl.textContent);
        const neu = aktuell + 1;
        portionenEl.textContent = neu;
        aktualisiereZutaten(neu / originalPortionen);
    });

    document.getElementById("portionen-minus").addEventListener("click", () => {
        const aktuell = parseInt(portionenEl.textContent);
        if (aktuell <= 1) return;
        const neu = aktuell - 1;
        portionenEl.textContent = neu;
        aktualisiereZutaten(neu / originalPortionen);
    });
});