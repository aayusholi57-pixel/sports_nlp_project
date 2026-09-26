import sqlite3
import json

DB_NAME = "sports_intel.db"

def init_db():
    """Creates the articles table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment_label TEXT NOT NULL,
            sentiment_score REAL NOT NULL,
            entities TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_analysis(text: str, sentiment: dict, entities: list):
    """Inserts a new NLP analysis record into SQLite."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO articles (text, sentiment_label, sentiment_score, entities)
        VALUES (?, ?, ?, ?)
    ''', (
        text, 
        sentiment['label'], 
        sentiment['confidence'], 
        json.dumps(entities)
    ))
    
    conn.commit()
    article_id = cursor.lastrowid
    conn.close()
    return article_id

def fetch_all_analyses():
    """Retrieves all processed analyses ordered by most recent."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, text, sentiment_label, sentiment_score, entities, created_at 
        FROM articles 
        ORDER BY created_at DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "text": row[1],
            "sentiment": {
                "label": row[2], 
                "confidence": row[3]
            },
            "entities": json.loads(row[4]),
            "created_at": row[5]
        })
    return results