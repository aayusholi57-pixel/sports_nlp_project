"""FastAPI service for sports NLP analysis and pipeline history."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from aggregate import generate_intelligence_summary
from core import get_analyzer
from database import fetch_all_analyses, init_db, save_analysis
from pipeline import run_pipeline


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Sports Intelligence NLP API",
    description="Production-oriented NLP API for sports sentiment analysis, named-entity extraction, persistence, and batch refresh.",
    version="2.1.0",
)


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=int(os.getenv("MAX_TEXT_LENGTH", "5000")))

    model_config = {"json_schema_extra": {"example": {"text": "Real Madrid produced a fantastic performance against Rayo Vallecano in Spain."}}}


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"status": "online", "service": "sports-intelligence-nlp", "docs": "/docs"}


@app.get("/api/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/api/v1/analyze", tags=["analysis"])
def analyze_and_store(payload: TextRequest) -> dict[str, Any]:
    try:
        result = get_analyzer().analyze(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db_id = save_analysis(result["text"], result["sentiment"], result["entities"])
    result["db_id"] = db_id
    return result


@app.get("/api/v1/history", tags=["analysis"])
def get_history(limit: int = Query(100, ge=1, le=500)) -> dict[str, Any]:
    history = fetch_all_analyses(limit)
    return {"total_records": len(history), "history": history}


@app.get("/api/v1/summary", tags=["analysis"])
def get_summary() -> dict[str, Any]:
    if not os.path.exists("summary.json"):
        raise HTTPException(status_code=404, detail="No summary file found. Run the pipeline first.")
    import json
    with open("summary.json", encoding="utf-8") as file:
        data = json.load(file)
    return {"total_tracked": len(data), "metrics": data}


def _run_pipeline() -> None:
    run_pipeline(fetch_live=True)


@app.post("/api/v1/pipeline/run", status_code=202, tags=["pipeline"])
def trigger_pipeline(background_tasks: BackgroundTasks) -> dict[str, str]:
    background_tasks.add_task(_run_pipeline)
    return {"status": "accepted", "message": "Pipeline execution started in the background."}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
