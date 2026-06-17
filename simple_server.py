import http.server
import socketserver
import json
import random
import urllib.request
import urllib.error
import urllib.parse
from urllib.parse import urlparse
import os

PORT = 8000
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure the server serves files relative to this script location.
os.chdir(BASE_DIR)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # Endpoint: /gold-rate
        if parsed_path.path == '/gold-rate':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            mock_price = round(random.uniform(70000, 75000), 2)
            response = {"price": mock_price, "currency": "INR", "unit": "10g"}
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Endpoint: /gold-news/{date}
        elif parsed_path.path.startswith('/gold-news/'):
            date = parsed_path.path.split('/')[-1]
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if NEWS_API_KEY:
                url = f"https://newsapi.org/v2/everything?q=gold&from={date}&to={date}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        data = json.loads(response.read().decode())
                        if data.get("status") == "ok":
                            self.wfile.write(json.dumps(data).encode())
                            return
                except Exception as e:
                    print(f"Error fetching real news: {e}")
            
            # Mock Response
            mock_data = {
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
            self.wfile.write(json.dumps(mock_data).encode())
            return
            
        # Serve static files and index.html
        if self.path == '/':
            self.path = '/templates/index.html'
            
        return super().do_GET()

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
