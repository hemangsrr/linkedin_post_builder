import requests

class WebResearchAgent:
    def __init__(self, max_results=5):
        self.api_key = None  # Will be set via set_api_key
        self.max_results = max_results

    def set_api_key(self, api_key: str):
        """Set the SERP API key dynamically."""
        self.api_key = api_key

    def run(self, query: str) -> list:
        """Search web using SerpAPI and return structured results.
        
        Args:
            query: Search query string
            
        Returns:
            List of article dictionaries or empty list if error occurs
        """
        if not self.api_key:
            print("[WebResearchAgent] Error: API key not set")
            return []

        print(f"[WebResearchAgent] Searching web for: {query}")
        params = {
            "q": query,
            "api_key": self.api_key,
            "engine": "google",
            "num": self.max_results
        }

        try:
            res = requests.get("https://serpapi.com/search", params=params)
            res.raise_for_status()  # Raises exception for 4XX/5XX responses
            results = res.json()

            articles = []
            for result in results.get("organic_results", [])[:self.max_results]:
                articles.append({
                    "type": "web",
                    "title": result.get("title", "No title available"),
                    "summary": result.get("snippet", "No summary available"),
                    "link": result.get("link", "")
                })

            return articles

        except requests.exceptions.RequestException as e:
            print(f"[WebResearchAgent] API request failed: {e}")
            return []
        except ValueError as e:
            print(f"[WebResearchAgent] JSON decode error: {e}")
            return []
        except Exception as e:
            print(f"[WebResearchAgent] Unexpected error: {e}")
            return []