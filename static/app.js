document.addEventListener("DOMContentLoaded", loadHistory);

// Dictionary to style different entity types beautifully
const entityStyles = {
    "PERSON": "bg-purple-100 text-purple-700 border-purple-200", // Players/Managers
    "ORG": "bg-blue-100 text-blue-700 border-blue-200",         // Teams/Clubs
    "GPE": "bg-emerald-100 text-emerald-700 border-emerald-200", // Countries/Cities
    "LOC": "bg-teal-100 text-teal-700 border-teal-200",         // Locations/Stadiums
    "DATE": "bg-amber-100 text-amber-700 border-amber-200",     // Dates
    "DEFAULT": "bg-slate-100 text-slate-600 border-slate-200"
};

// Helper: Paste example text into textarea
function setExample(button) {
    document.getElementById("newsInput").value = button.innerText;
}

// Helper: Clear textarea
function clearText() {
    document.getElementById("newsInput").value = "";
    document.getElementById("resultsCard").classList.add("opacity-0", "translate-y-2", "hidden");
}

async function analyzeText() {
    const textInput = document.getElementById("newsInput").value;
    if (!textInput.trim()) {
        alert("Please paste some text first!");
        return;
    }

    // 1. UI Loading State
    const btnText = document.getElementById("btnText");
    const btnSpinner = document.getElementById("btnSpinner");
    const analyzeBtn = document.getElementById("analyzeBtn");
    
    btnText.innerText = "Analyzing...";
    btnSpinner.classList.remove("hidden");
    analyzeBtn.disabled = true;
    analyzeBtn.classList.add("opacity-75", "cursor-not-allowed");

    try {
        // 2. Call the FastAPI Backend
        const response = await fetch("/api/v1/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textInput })
        });

        const data = await response.json();
        
        // 3. Render Sentiment
        const badge = document.getElementById("sentimentBadge");
        const isPos = data.sentiment.label.includes("POS") || data.sentiment.label === "LABEL_1";
        
        badge.innerHTML = isPos 
            ? `** Positive (${(data.sentiment.confidence * 100).toFixed(1)}%)`
            : `** Negative (${(data.sentiment.confidence * 100).toFixed(1)}%)`;
        
        badge.className = isPos 
            ? "inline-flex items-center gap-2 px-4 py-2 rounded-lg font-bold text-sm bg-green-100 text-green-700 border border-green-200 shadow-sm"
            : "inline-flex items-center gap-2 px-4 py-2 rounded-lg font-bold text-sm bg-red-100 text-red-700 border border-red-200 shadow-sm";

        // 4. Render Entities
        const entitiesList = document.getElementById("entitiesList");
        entitiesList.innerHTML = "";
        
        if (data.entities.length === 0) {
            entitiesList.innerHTML = `No major entities found.`;
        } else {
            data.entities.forEach(ent => {
                const styleClass = entityStyles[ent.type] || entityStyles["DEFAULT"];
                entitiesList.innerHTML += `
Unimplemented node type: 7
            `;
        });
    }

    // Reveal Results Card smoothly
    const resultsCard = document.getElementById("resultsCard");
    resultsCard.classList.remove("hidden");
    // small delay to allow display:block to apply before animating opacity
    setTimeout(() => {
        resultsCard.classList.remove("opacity-0", "translate-y-2");
    }, 10);
    
    // Refresh history immediately
    loadHistory();

} catch (error) {
    console.error("Analysis Error:", error);
    alert("Something went wrong connecting to the AI Engine.");
} finally {
    // Restore Button State
    btnText.innerText = "Run AI Engine";
    btnSpinner.classList.add("hidden");
    analyzeBtn.disabled = false;
    analyzeBtn.classList.remove("opacity-75", "cursor-not-allowed");
}
}

async function loadHistory() {
try {
const response = await fetch("/api/v1/history");
const data = await response.json();

    const feed = document.getElementById("historyFeed");
    feed.innerHTML = "";

    if (data.history.length === 0) {
        feed.innerHTML = `
Unimplemented node type: 7
`;
return;
}

        data.history.forEach(item => {
            const isPos = item.sentiment.label.includes("POS") || item.sentiment.label === "LABEL_1";
            const icon = isPos ? '**' : '**';
            
            // Format the SQLite timestamp nicely
            const dateObj = new Date(item.created_at);
            const timeStr = dateObj.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            const dateStr = dateObj.toLocaleDateString([], {month: 'short', day: 'numeric'});

            feed.innerHTML += `
Unimplemented node type: 7
    `;
});
} catch (error) {
document.getElementById("historyFeed").innerHTML = `

Failed to load history.

`;
}
}
