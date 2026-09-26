"""Fetch football news from the BBC Sport RSS feed."""

from __future__ import annotations

import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BBC_FOOTBALL_RSS = "https://feeds.bbci.co.uk/sport/football/rss.xml"


def scrape_live_news(output_path: str = "raw_news.json", limit: int = 15) -> list[dict[str, object]]:
    response = requests.get(BBC_FOOTBALL_RSS, timeout=15, headers={"User-Agent": "sports-nlp-project/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.content, features="xml")

    articles = []
    for index, item in enumerate(soup.find_all("item")[:limit], start=1):
        title = item.find("title")
        description = item.find("description")
        if not title:
            continue
        text = f"{title.get_text(strip=True)}. {description.get_text(' ', strip=True) if description else ''}".strip()
        articles.append({"id": index, "text": text})

    Path(output_path).write_text(json.dumps(articles, indent=2), encoding="utf-8")
    return articles


if __name__ == "__main__":
    articles = scrape_live_news()
    print(f"Fetched {len(articles)} football articles")
