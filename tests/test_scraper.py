import scraper

def test_scraper_parses_rss(monkeypatch, tmp_path):
    class FakeResponse:
        content = b"<?xml version='1.0'?><rss><channel><item><title>Arsenal win</title><description>Great performance</description></item></channel></rss>"
        def raise_for_status(self): pass
    monkeypatch.setattr(scraper.requests, "get", lambda *args, **kwargs: FakeResponse())
    result = scraper.scrape_live_news(str(tmp_path / "news.json"), limit=5)
    assert result[0]["text"] == "Arsenal win. Great performance"
