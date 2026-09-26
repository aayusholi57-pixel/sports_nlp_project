import json
from aggregate import generate_intelligence_summary

def test_aggregate_counts_unique_entities(tmp_path):
    report = [{"sentiment": {"label": "POSITIVE"}, "entities": [{"text": "Arsenal", "type": "ORG"}, {"text": "Arsenal", "type": "ORG"}]}, {"sentiment": {"label": "NEGATIVE"}, "entities": [{"text": "Arsenal", "type": "ORG"}]}]
    source, output = tmp_path / "report.json", tmp_path / "summary.json"
    source.write_text(json.dumps(report), encoding="utf-8")
    result = generate_intelligence_summary(str(source), str(output))
    assert result[0]["mentions"] == 2
    assert result[0]["sentiment_counts"] == {"POSITIVE": 1, "NEGATIVE": 1, "NEUTRAL": 0}
