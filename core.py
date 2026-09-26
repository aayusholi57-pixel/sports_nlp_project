"""Core NLP inference engine for sports text intelligence."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import spacy
from transformers import pipeline


SPORTS_ENTITY_TYPES = {"PERSON", "ORG", "GPE", "LOC", "DATE", "EVENT", "FAC"}


class SportsIntelAnalyzer:
    """Combine transformer sentiment analysis with spaCy NER."""

    def __init__(self) -> None:
        model_name = os.getenv("SENTIMENT_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
        spacy_model = os.getenv("SPACY_MODEL", "en_core_web_sm")
        self.max_text_length = int(os.getenv("MAX_TEXT_LENGTH", "5000"))

        self.nlp = spacy.load(spacy_model)
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

    def analyze(self, text: str) -> dict[str, Any]:
        """Return sentiment and relevant named entities for one text payload."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must contain non-whitespace characters")
        if len(text) > self.max_text_length:
            raise ValueError(f"text exceeds the {self.max_text_length} character limit")

        cleaned_text = text.strip()
        sentiment_result = self.sentiment_analyzer(cleaned_text, truncation=True)[0]
        doc = self.nlp(cleaned_text)

        seen: set[tuple[str, str]] = set()
        entities: list[dict[str, str]] = []
        for ent in doc.ents:
            if ent.label_ not in SPORTS_ENTITY_TYPES:
                continue
            key = (ent.text, ent.label_)
            if key in seen:
                continue
            seen.add(key)
            entities.append({"text": ent.text, "type": ent.label_})

        return {
            "text": cleaned_text,
            "sentiment": {
                "label": str(sentiment_result["label"]).upper(),
                "confidence": round(float(sentiment_result["score"]), 4),
            },
            "entities": entities,
        }


@lru_cache(maxsize=1)
def get_analyzer() -> SportsIntelAnalyzer:
    """Create the model-backed analyzer once per process."""
    return SportsIntelAnalyzer()


if __name__ == "__main__":
    result = get_analyzer().analyze(
        "Manchester City dominated Manchester United in a thrilling match today."
    )
    print(result)
