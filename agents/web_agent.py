import os
from dotenv import load_dotenv
import requests

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

class WebResearchAgent:
    def __init__(self, max_results=5):
        self.api_key = SERPAPI_API_KEY
        self.max_results = max_results

    def run(self, query: str) -> list:
        """Search web using SerpAPI and return structured results."""
        print(f"[WebResearchAgent] Searching web for: {query}")
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": self.max_results
        }

        try:
            res = requests.get("https://serpapi.com/search", params=params)
            results = res.json()

            articles = []
            for result in results.get("organic_results", [])[:self.max_results]:
                articles.append({
                    "type": "web",
                    "title": result.get("title"),
                    "summary": result.get("snippet"),
                    "link": result.get("link")
                })

            return articles

        except Exception as e:
            print(f"[WebResearchAgent] Error: {e}")
            return []
