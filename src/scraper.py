import requests
import json
from bs4 import BeautifulSoup
from googlesearch import search  

def get_news(company):
    """Fetches top 10 news articles for a given company using Google Search."""
    query = f"{company} latest news"
    news_links = list(search(query, num_results=11))  

    articles = []
    for link in news_links:
        try:
            response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "No Title"
            
            articles.append({"title": title, "link": link})
        except:
            continue  

    return articles

def save_news_to_file(company, articles):
    """Saves news articles to a JSON file."""
    filename = f"data/{company}_news.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    print(f"✅ News articles saved to {filename}")

if __name__ == "__main__":
    company_name = "Microsoft"
    news = get_news(company_name)

    if news:
        save_news_to_file(company_name, news)
    else:
        print("No news found.")
