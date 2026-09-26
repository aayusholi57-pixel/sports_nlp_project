import json
from core import SportsIntelAnalyzer # Imports the class we built in Phase 1

# 1. Create our raw input data
raw_news = [
    {"id": 1, "text": "Real Madrid played a fantastic match against Rayo Vallecano today, absolutely brilliant!"},
    {"id": 2, "text": "The weather during the Manchester United vs Manchester City game was terrible, and the referee was completely unfair."},
    {"id": 3, "text": "A quiet 0-0 draw between Arsenal and Chelsea. Nothing much happened."}
]

# 2. Write the data to a file (Creates the file automatically)
with open("raw_news.json", "w") as file:
    json.dump(raw_news, file, indent=4)
    
print("Created raw_news.json!")

# 3. Read the raw data back from the file
with open("raw_news.json", "r") as file:
    articles = json.load(file)

# 4. Initialize our NLP Engine
analyzer = SportsIntelAnalyzer()

# 5. Process each article
intelligence_report = []
for article in articles:
    print(f"Analyzing article {article['id']}...")
    result = analyzer.analyze(article["text"])
    
    # Add the ID back into the result so we can track it
    result["id"] = article["id"]
    intelligence_report.append(result)

# 6. Save the final analyzed intelligence to a new file
with open("intelligence_report.json", "w") as file:
    json.dump(intelligence_report, file, indent=4)
    
print("Pipeline complete! Check intelligence_report.json for the results.")