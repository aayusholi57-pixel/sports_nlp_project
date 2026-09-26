import json
from collections import defaultdict

def generate_intelligence_summary(file_path: str):
    # 1. Load the processed NLP report
    with open(file_path, "r") as file:
        report = json.load(file)

    # Structure to track: mentions, positive count, negative count, and type
    entity_stats = defaultdict(lambda: {"mentions": 0, "POSITIVE": 0, "NEGATIVE": 0, "type": "UNKNOWN"})

    # 2. Iterate through each article's NLP results
    for article in report:
        sentiment_label = article["sentiment"]["label"].upper()
        
        # Use a set to count an entity only once per article
        unique_entities = {(e["text"], e["type"]) for e in article["entities"]}
        
        for ent_text, ent_type in unique_entities:
            entity_stats[ent_text]["mentions"] += 1
            entity_stats[ent_text]["type"] = ent_type
            
            # Standardize positive vs negative labeling
            if "POS" in sentiment_label or sentiment_label == "LABEL_1":
                entity_stats[ent_text]["POSITIVE"] += 1
            else:
                entity_stats[ent_text]["NEGATIVE"] += 1

    # 3. Print a formatted summary report
    print("\n📊 --- Sports Intelligence Summary ---")
    print(f"{'Entity Name':<22} | {'Type':<8} | {'Mentions':<8} | {'Sentiment Trend'}")
    print("-" * 65)

    summary_data = []
    for entity, stats in entity_stats.items():
        pos = stats["POSITIVE"]
        neg = stats["NEGATIVE"]
        
        if pos > neg:
            trend = "Positive 🟢"
        elif neg > pos:
            trend = "Negative 🔴"
        else:
            trend = "Neutral 🟡"

        print(f"{entity:<22} | {stats['type']:<8} | {stats['mentions']:<8} | {trend}")
        
        summary_data.append({
            "entity": entity,
            "type": stats["type"],
            "mentions": stats["mentions"],
            "trend": trend
        })

    # 4. Save the aggregated stats to summary.json
    with open("summary.json", "w") as file:
        json.dump(summary_data, file, indent=4)
        
    print("\nSaved aggregated metrics to summary.json!")

if __name__ == "__main__":
    generate_intelligence_summary("intelligence_report.json")