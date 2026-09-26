import database
import api

class FakeAnalyzer:
    def analyze(self, text):
        return {"text": text.strip(), "sentiment": {"label": "POSITIVE", "confidence": 0.98}, "entities": [{"text": "Arsenal", "type": "ORG"}]}

def test_health_and_analyze(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_NAME", str(tmp_path / "api.db"))
    monkeypatch.setattr(api, "get_analyzer", lambda: FakeAnalyzer())
    from fastapi.testclient import TestClient
    with TestClient(api.app) as client:
        assert client.get("/api/health").json() == {"status": "healthy"}
        response = client.post("/api/v1/analyze", json={"text": "Arsenal won"})
    assert response.status_code == 200
    assert response.json()["db_id"] == 1

def test_empty_text_is_rejected():
    from fastapi.testclient import TestClient
    with TestClient(api.app) as client:
        response = client.post("/api/v1/analyze", json={"text": "   "})
    assert response.status_code == 422
