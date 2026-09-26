import database

def test_database_round_trip(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_NAME", str(tmp_path / "sports.db"))
    database.init_db()
    record_id = database.save_analysis("Arsenal won", {"label": "POSITIVE", "confidence": 0.99}, [{"text": "Arsenal", "type": "ORG"}])
    rows = database.fetch_all_analyses()
    assert record_id == 1
    assert rows[0]["sentiment"]["label"] == "POSITIVE"
    assert rows[0]["entities"][0]["text"] == "Arsenal"
