from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
import random
from datetime import datetime, timedelta

app = FastAPI()

# Use directories relative to this file, not the current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static directory for CSS and JS
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Try to get API keys from environment
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
GOLD_API_KEY = os.getenv("GOLD_API_KEY", "")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/gold-rate")
def get_gold_rate():
    # If we have a real API key, we could fetch it here.
    # For now, let's mock it since we don't have a specific API endpoint configured.
    # In a real scenario:
    # url = f"https://api.gold-api.com/price?key={GOLD_API_KEY}"
    # response = requests.get(url)
    # return response.json()
    
    # Mock Response
    mock_price = round(random.uniform(70000, 75000), 2) # Mocking INR gold price per 10g
    return {"price": mock_price, "currency": "INR", "unit": "10g"}

@app.get("/gold-news/{date}")
def get_gold_news(date: str):
    if NEWS_API_KEY:
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q=gold&from={date}&to={date}"
            f"&sortBy=publishedAt"
            f"&language=en"
            f"&apiKey={NEWS_API_KEY}"
        )
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("status") == "ok":
                return data
        except Exception as e:
            print(f"Error fetching news: {e}")
            pass

    # Mock Response if no API key or if API fails
    return {
        "status": "ok",
        "totalResults": 3,
        "articles": [
            {
                "title": f"Gold Prices Surge on {date}",
                "description": "Global markets react as gold prices hit a new high today amidst economic uncertainty.",
                "url": "#",
                "source": {"name": "Finance Daily"}
            },
            {
                "title": "Should You Invest in Gold Right Now?",
                "description": "Experts weigh in on the recent fluctuations in the precious metals market.",
                "url": "#",
                "source": {"name": "Market Watch"}
            },
            {
                "title": "Central Banks Increase Gold Reserves",
                "description": "A new report shows a significant increase in gold purchases by central banks worldwide.",
                "url": "#",
                "source": {"name": "Economic Times"}
            }
        ]
    }
