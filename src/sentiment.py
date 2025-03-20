import json
from textblob import TextBlob
import os

def analyze_sentiment(text):
    """
    Determines the sentiment of the given text.
    Returns: Positive, Negative, or Neutral.
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def analyze_articles(company):
    """
    Reads the stored news file, analyzes sentiment for each article, 
    and saves the results in a new file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root directory
    input_file = os.path.join(base_dir, f"data/{company}_news.json")
    output_file = os.path.join(base_dir, f"data/{company}_sentiment.json")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File {input_file} not found.")
        return

    results = []
    for article in articles:
        sentiment = analyze_sentiment(article["title"])
        results.append({
            "title": article["title"],
            "link": article["link"],
            "sentiment": sentiment
        })

    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure `data/` exists

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Sentiment report saved to {output_file}")

if __name__ == "__main__":
    company_name = "Microsoft"  # Change this if testing with another company
    analyze_articles(company_name)
