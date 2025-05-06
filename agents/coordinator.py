from agents.web_agent import WebResearchAgent
from agents.paper_agent import PaperResearchAgent
from agents.summary_agent import SummaryAgent

class ResearchCoordinator:
    def __init__(self):
        # Initialize all the specialized agents
        self.web_agent = WebResearchAgent()
        self.paper_agent = PaperResearchAgent()
        self.summary_agent = SummaryAgent()

    def run(self, topic: str) -> dict:
        """Orchestrate the entire research process."""
        print(f"[ResearchCoordinator] Starting research for topic: {topic}")

        # Step 1: Run Web Research
        web_results = self.web_agent.run(topic)
        print(f"[ResearchCoordinator] Fetched {len(web_results)} web results.")

        # Step 2: Run Paper Research
        paper_results = self.paper_agent.run(topic)
        print(f"[ResearchCoordinator] Fetched {len(paper_results)} paper results.")

        # Combine results from both sources
        combined_results = web_results + paper_results
        if not combined_results:
            return {"summary": "No results found.", "posts": ""}

        # Step 3: Summarize the combined results
        summary = self.summary_agent.summarize(combined_results)

        # Step 4: Generate LinkedIn Posts
        posts = self.summary_agent.generate_posts(summary)

        return {"summary": summary, "posts": posts}
