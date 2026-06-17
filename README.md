# Gold News Dashboard ✨

A sleek, premium web application that displays live gold rates and recent news articles related to gold based on a selected date. This project is built using a **Vanilla JavaScript / HTML / CSS** frontend and a lightweight **Python** backend.

## 🚀 Features
- **Live Gold Rate:** Fetches and displays the current gold rate.
- **Dynamic News Fetching:** Select a date from the last 5 days to get the most relevant gold news.
- **Premium UI/UX:** Built with dark mode aesthetics, glassmorphism, subtle animations, and smooth transitions.
- **Zero-Dependency Backend Option:** Includes a built-in Python server that runs without needing `pip` or any external packages.

## 🛠️ Technologies Used
- **Frontend:** HTML5, CSS3 (Custom Variables, Flexbox, CSS Grid), Vanilla JavaScript
- **Backend:** Python 3 (`http.server` for zero-dependency running OR `FastAPI` for production)
- **External APIs (Optional):** NewsAPI, GoldAPI

---

## 🏃‍♂️ How to Run the Project

You have two options to run the backend server. The **Zero-Dependency Setup** is recommended for quick testing since it requires no package installations.

### Option 1: Zero-Dependency Setup (Recommended for quick start)
This option uses Python's built-in standard library to serve the app and mock the APIs. You don't need to install anything!

1. Open your terminal.
2. Navigate to the project directory:
   ```bash
   cd /path/to/fastapi-gold-news-app
   ```
3. Run the simple python server:
   ```bash
   python3 simple_server.py
   ```
4. Open your browser and navigate to: **`http://localhost:8000`**

### Option 2: FastAPI Setup (Production ready)
If you want to use the actual FastAPI implementation (`app.py`), you need to install the required Python packages.

1. Ensure you have `python3-venv` and `python3-pip` installed on your system.
2. Navigate to the project directory.
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```
6. Open your browser and navigate to: **`http://127.0.0.1:8000`**

---

## 🔑 Using Real Data (API Keys)

By default, the application returns **Mock Data** so you can test the UI without needing API keys. If you want to fetch real data, you need to provide your API keys via environment variables before starting the server.

**For Linux/Mac:**
```bash
export NEWS_API_KEY="your_newsapi_key_here"
export GOLD_API_KEY="your_gold_api_key_here"

# Then run the server:
python3 simple_server.py
```

*Note: The NewsAPI key can be obtained from [newsapi.org](https://newsapi.org/).*

## 📁 Project Structure

```text
fastapi-gold-news-app/
│
├── app.py                  # The robust FastAPI backend
├── simple_server.py        # The zero-dependency built-in Python backend
├── requirements.txt        # Python package dependencies for FastAPI
│
├── templates/
│   └── index.html          # Main HTML Dashboard
│
└── static/
    ├── style.css           # Premium styling and animations
    └── script.js           # Vanilla JS logic for fetching data
```
