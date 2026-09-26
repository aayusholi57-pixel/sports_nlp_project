const entityStyles = { PERSON: "entity-person", ORG: "entity-org", GPE: "entity-gpe", LOC: "entity-loc", DATE: "entity-date", EVENT: "entity-event", FAC: "entity-fac" };

async function analyzeSportsText(text) {
  const response = await fetch("/api/v1/analyze", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Analysis failed");
  return data;
}

async function loadAnalysisHistory(limit = 20) {
  const response = await fetch("/api/v1/history?limit=" + limit);
  if (!response.ok) throw new Error("Unable to load analysis history");
  return response.json();
}

window.sportsNLP = { analyzeSportsText, loadAnalysisHistory, entityStyles };
