from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import json
import os

from core import SportsIntelAnalyzer
import scraper
import pipeline
import aggregate

# Initialize FastAPI application
app = FastAPI(
    title="Sports Intelligence NLP API",
    description="Production API for real-time sports news sentiment and entity extraction.",
    version="1.0.0"
)

# Load NLP Engine into memory on startup
print("Initializing NLP Engine for API...")
analyzer = SportsIntelAnalyzer()


# Define request payload schema using Pydantic
class TextAnalysisRequest(BaseModel):
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Real Madrid played a fantastic match against Rayo Vallecano today in Spain."
            }
        }


@app.get("/")
def root():
    return {"status": "online", "message": "Sports Intelligence API is running."}


@app.post("/api/v1/analyze", summary="Analyze a single text payload")
def analyze_text(payload: TextAnalysisRequest):
    """Pass raw sports commentary or news to extract entities and sentiment."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text payload cannot be empty.")
    
    result = analyzer.analyze(payload.text)
    return result


@app.get("/api/v1/summary", summary="Retrieve aggregated trend metrics")
def get_summary():
    """Returns the latest aggregated metrics from summary.json."""
    if not os.path.exists("summary.json"):
        raise HTTPException(
            status_code=404, 
            detail="No summary file found. Run the pipeline first."
        )
    
    with open("summary.json", "r") as f:
        data = json.load(f)
    return {"total_tracked": len(data), "metrics": data}


def run_full_pipeline_task():
    """Background worker to execute scraping and aggregation."""
    scraper.scrape_live_news()
    # Reload articles and run pipeline
    with open("raw_news.json", "r") as f:
        articles = json.load(f)
        
    reports = []
    for a in articles:
        res = analyzer.analyze(a["text"])
        res["id"] = a["id"]
        reports.append(res)
        
    with open("intelligence_report.json", "w") as f:
        json.dump(reports, f, indent=4)
        
    aggregate.generate_intelligence_summary("intelligence_report.json")


@app.post("/api/v1/pipeline/run", summary="Trigger full automated refresh")
def trigger_pipeline(background_tasks: BackgroundTasks):
    """Triggers live web scraping and reprocessing asynchronously in the background."""
    background_tasks.add_task(run_full_pipeline_task)
    return {
        "status": "accepted",
        "message": "Pipeline execution started in the background."
    }

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

from core import SportsIntelAnalyzer
from database import init_db, save_analysis, fetch_all_analyses
import scraper
import json

app = FastAPI(
    title="Sports Intelligence NLP API",
    version="2.0.0"
)

# Initialize Database and NLP Engine on startup
init_db()
analyzer = SportsIntelAnalyzer()


class TextRequest(BaseModel):
    text: str


@app.post("/api/v1/analyze", summary="Analyze text and persist to SQLite")
def analyze_and_store(payload: TextRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text payload cannot be empty.")
    
    # 1. Run NLP pipeline
    result = analyzer.analyze(payload.text)
    
    # 2. Persist directly to SQLite database
    db_id = save_analysis(
        text=result["text"],
        sentiment=result["sentiment"],
        entities=result["entities"]
    )
    
    result["db_id"] = db_id
    return result


@app.get("/api/v1/history", summary="Fetch analysis history from SQLite")
def get_history():
    """Retrieves all past NLP analyses stored in the database."""
    records = fetch_all_analyses()
    return {"total_records": len(records), "history": records}
app.mount("/", StaticFiles(directory="static", html=True), name="static")