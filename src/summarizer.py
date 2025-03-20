import json
import os
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

def summarize_text(text, num_sentences=3):
    """
    Summarizes the given text by selecting the first `num_sentences` sentences.
    """
    sentences = sent_tokenize(text)
    return " ".join(sentences[:num_sentences]) if sentences else "No summary available."

def summarize_sentiment_report(company):
    """
    Reads the sentiment analysis report and summarizes the findings.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root directory
    input_file = os.path.join(base_dir, f"data/{company}_sentiment.json")
    output_file = os.path.join(base_dir, f"data/{company}_summary.txt")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File {input_file} not found.")
        return

    total_articles = len(articles)
    positive = sum(1 for a in articles if a["sentiment"] == "Positive")
    negative = sum(1 for a in articles if a["sentiment"] == "Negative")
    neutral = sum(1 for a in articles if a["sentiment"] == "Neutral")

    summary_text = (
        f"The company {company} has {total_articles} recent news articles.\n"
        f"Out of these, {positive} articles are positive, {negative} are negative, "
        f"and {neutral} are neutral.\n"
        f"This indicates the overall sentiment about {company} is "
        f"{'mostly positive' if positive > negative else 'mostly negative' if negative > positive else 'neutral'}."
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure `data/` exists

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary_text)
    
    print(f"✅ Summary saved to {output_file}")
    return summary_text

if __name__ == "__main__":
    company_name = "Microsoft"
    summarize_sentiment_report(company_name)
