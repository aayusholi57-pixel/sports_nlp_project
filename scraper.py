import requests
from bs4 import BeautifulSoup
import json

def scrape_live_news():
    print("🌐 Fetching live football news from BBC Sport...")
    # RSS feeds are perfect for scraping because they provide clean, structured XML data
    url = "http://feeds.bbci.co.uk/sport/football/rss.xml"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the XML content
        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll('item')
        
        live_news = []
        
        # Grab the latest 15 news items
        for i, item in enumerate(items[:15]):
            title = item.find('title').text
            description = item.find('description').text
            
            # Combine title and description for richer text analysis
            full_text = f"{title}. {description}"
            
            live_news.append({
                "id": i + 1,
                "text": full_text
            })
            
        # Overwrite our existing raw_news.json file with live data
        with open("raw_news.json", "w") as file:
            json.dump(live_news, file, indent=4)
            
        print(f"✅ Successfully scraped {len(live_news)} live articles and saved to raw_news.json!")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")

if __name__ == "__main__":
    scrape_live_news()