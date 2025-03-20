import requests
from bs4 import BeautifulSoup
from googlesearch import search  # Correct import

def get_news(company):
    """Fetches top 10 news articles for a given company using Google Search."""
    query = f"{company} latest news"
    news_links = list(search(query, num_results=11))  # ✅ Use num_results instead of max_results

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
            continue  # Skip if any issue occurs

    return articles

if __name__ == "__main__":
    company_name = "Microsoft"
    news = get_news(company_name)
    
    if not news:
        print("No news found.")
    else:
        for idx, article in enumerate(news):
            print(f"{idx+1}. {article['title']}")
            print(f"   {article['link']}\n")
