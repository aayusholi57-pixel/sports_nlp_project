"""Aggregate sentiment trends across analyzed sports entities."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def generate_intelligence_summary(file_path: str, output_path: str = "summary.json") -> list[dict[str, Any]]:
    with open(file_path, encoding="utf-8") as file:
        report = json.load(file)

    entity_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"mentions": 0, "POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0, "type": "UNKNOWN"}
    )

    for article in report:
        label = str(article["sentiment"]["label"]).upper()
        sentiment = "POSITIVE" if "POS" in label or label == "LABEL_1" else "NEGATIVE" if "NEG" in label or label == "LABEL_0" else "NEUTRAL"
        unique_entities = {(e["text"], e["type"]) for e in article.get("entities", [])}
        for entity, entity_type in unique_entities:
            stats = entity_stats[entity]
            stats["mentions"] += 1
            stats["type"] = entity_type
            stats[sentiment] += 1

    summary: list[dict[str, Any]] = []
    for entity, stats in sorted(entity_stats.items(), key=lambda item: (-item[1]["mentions"], item[0].lower())):
        counts = {key: stats[key] for key in ("POSITIVE", "NEGATIVE", "NEUTRAL")}
        trend = max(counts, key=counts.get) if stats["mentions"] else "NEUTRAL"
        summary.append({"entity": entity, "type": stats["type"], "mentions": stats["mentions"], "trend": trend, "sentiment_counts": counts})

    Path(output_path).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(generate_intelligence_summary("intelligence_report.json"), indent=2))
