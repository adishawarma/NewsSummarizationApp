from fastapi import FastAPI
import json
import os
from tts import text_to_speech

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root directory
DATA_DIR = os.path.join(BASE_DIR, "data")

@app.get("/")
def home():
    return {"message": "Welcome to the News Summarization & Sentiment Analysis API!"}

@app.get("/fetch_news")
def fetch_news(company: str = "Microsoft"):
    """
    Fetches the scraped news articles from JSON file.
    """
    file_path = os.path.join(DATA_DIR, f"{company}_news.json")
    
    if not os.path.exists(file_path):
        return {"error": f"News data for {company} not found."}

    with open(file_path, "r", encoding="utf-8") as f:
        news_data = json.load(f)
    
    return {"company": company, "articles": news_data}

@app.get("/fetch_sentiment")
def fetch_sentiment(company: str = "Microsoft"):
    """
    Fetches the sentiment analysis report from JSON file.
    """
    file_path = os.path.join(DATA_DIR, f"{company}_sentiment.json")
    
    if not os.path.exists(file_path):
        return {"error": f"Sentiment data for {company} not found."}

    with open(file_path, "r", encoding="utf-8") as f:
        sentiment_data = json.load(f)
    
    return {"company": company, "sentiment_analysis": sentiment_data}

@app.get("/fetch_summary")
def fetch_summary(company: str = "Microsoft"):
    """
    Fetches the summary of sentiment analysis from TXT file.
    """
    file_path = os.path.join(DATA_DIR, f"{company}_summary.txt")
    
    if not os.path.exists(file_path):
        return {"error": f"Summary report for {company} not found."}

    with open(file_path, "r", encoding="utf-8") as f:
        summary_text = f.read()
    
    return {"company": company, "summary": summary_text}

@app.get("/generate_tts")
def generate_tts(company: str = "Microsoft"):
    """
    Generates and returns the path of the Hindi TTS file.
    """
    text_to_speech(company)  # Generate TTS
    file_path = os.path.join(DATA_DIR, f"{company}_summary.mp3")

    if not os.path.exists(file_path):
        return {"error": "TTS file not generated."}

    return {"message": "TTS generated successfully.", "file_path": file_path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
