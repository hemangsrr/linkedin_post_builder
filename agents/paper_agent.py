import requests
import xml.etree.ElementTree as ET

class PaperResearchAgent:
    def __init__(self, max_results=5):
        self.max_results = max_results

    def run(self, query: str) -> list:
        """Fetch academic papers from arXiv."""
        print(f"[PaperResearchAgent] Searching arXiv for: {query}")
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={self.max_results}"

        try:
            response = requests.get(url)
            root = ET.fromstring(response.content)

            ns = {"arxiv": "http://www.w3.org/2005/Atom"}
            papers = []

            for entry in root.findall("arxiv:entry", ns):
                papers.append({
                    "type": "paper",
                    "title": entry.find("arxiv:title", ns).text.strip(),
                    "summary": entry.find("arxiv:summary", ns).text.strip(),
                    "link": entry.find("arxiv:id", ns).text.strip()
                })

            return papers

        except Exception as e:
            print(f"[PaperResearchAgent] Error: {e}")
            return []
