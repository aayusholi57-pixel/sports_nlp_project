import spacy
from transformers import pipeline

class SportsIntelAnalyzer:
    def __init__(self):
        print("Loading NLP models (this might take a few seconds)...")
        # Load spaCy for lightning-fast Named Entity Recognition
        self.nlp = spacy.load("en_core_web_sm")
        
        # Load Hugging Face for nuanced Sentiment Analysis
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        print("Models loaded and ready!")

    def analyze(self, text: str) -> dict:
        """Processes text to extract named entities and sentiment scores."""
        
        # 1. Run Sentiment Analysis
        sentiment_result = self.sentiment_analyzer(text)[0]
        
        # 2. Run Entity Extraction
        doc = self.nlp(text)
        
        # Clean up the entities into a structured list
        entities = []
        for ent in doc.ents:
            # Filter for entity types most relevant to sports and news
            if ent.label_ in ["PERSON", "ORG", "GPE", "LOC", "DATE"]:
                entities.append({
                    "text": ent.text,
                    "type": ent.label_
                })
                
        # 3. Package and return the structured intelligence
        return {
            "text": text,
            "sentiment": {
                "label": sentiment_result['label'],
                "confidence": round(sentiment_result['score'], 4)
            },
            "entities": entities
        }

# Test the engine with a sample match report
if __name__ == "__main__":
    analyzer = SportsIntelAnalyzer()
    
    sample_news = "Manchester City dominated Manchester United in a thrilling match today, though the refereeing was questionable."
    
    result = analyzer.analyze(sample_news)
    
    print("\n--- Pipeline Analysis Result ---")
    print(f"Sentiment: {result['sentiment']['label']} ({result['sentiment']['confidence']})")
    print("Entities Found:")
    for e in result['entities']:
        print(f" - {e['text']} ({e['type']})")