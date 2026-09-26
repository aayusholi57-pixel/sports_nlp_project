"""Run the end-to-end sports news NLP pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from aggregate import generate_intelligence_summary
from core import get_analyzer
from scraper import scrape_live_news


def run_pipeline(fetch_live: bool = True, input_path: str = "raw_news.json") -> list[dict[str, Any]]:
    if fetch_live:
        articles = scrape_live_news(input_path)
    else:
        articles = json.loads(Path(input_path).read_text(encoding="utf-8"))

    analyzer = get_analyzer()
    reports = []
    for article in articles:
        result = analyzer.analyze(str(article["text"]))
        result["id"] = article["id"]
        reports.append(result)

    Path("intelligence_report.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    generate_intelligence_summary("intelligence_report.json")
    return reports


if __name__ == "__main__":
    results = run_pipeline()
    print(f"Pipeline complete: {len(results)} articles analyzed")
