from agents.web_agent import WebResearchAgent
from agents.paper_agent import PaperResearchAgent
from agents.summary_agent import SummaryAgent
from agents.image_agent import ImageAgent
from agents.graph_agent import GraphAgent

class ResearchCoordinator:
    def __init__(self):
        # Initialize all the specialized agents
        self.web_agent = WebResearchAgent()
        self.paper_agent = PaperResearchAgent()
        self.summary_agent = SummaryAgent()
        self.image_agent = ImageAgent()
        self.graph_agent = GraphAgent()

    def run(self, topic: str, openai_api_key: str, serp_api_key: str, 
            generate_images: bool, generate_graphs: bool) -> dict:
        """Orchestrate the entire research process.
        
        Args:
            topic: Research topic
            openai_api_key: API key for OpenAI services
            serp_api_key: API key for SERP (web search)
            generate_images: Whether to generate images
            generate_graphs: Whether to generate graphs
            
        Returns:
            Dictionary containing research results
        """
        print(f"[ResearchCoordinator] Starting research for topic: {topic}")

        # Set API keys for agents that need them
        self.web_agent.set_api_key(serp_api_key)  # Web agent uses SERP
        self.summary_agent.set_api_key(openai_api_key)
        self.image_agent.set_api_key(openai_api_key)
        self.graph_agent.set_api_key(openai_api_key)

        # Step 1: Run Web Research
        web_results = self.web_agent.run(topic)
        print(f"[ResearchCoordinator] Fetched {len(web_results)} web results.")

        # Step 2: Run Paper Research
        paper_results = self.paper_agent.run(topic)
        print(f"[ResearchCoordinator] Fetched {len(paper_results)} paper results.")

        # Combine results from both sources
        combined_results = web_results + paper_results
        if not combined_results:
            return {"summary": "No results found.", "posts": []}

        # Step 3: Summarize the combined results
        summary = self.summary_agent.summarize(combined_results)

        # Step 4: Generate LinkedIn Posts
        posts = self.summary_agent.generate_posts(summary)

        # Step 5: Generate Images (if enabled)
        images = []
        if generate_images:
            images = self.image_agent.generate_images(summary)

        # Step 6: Generate Graphs (if enabled)
        graphs = []
        if generate_graphs:
            graphs = self.graph_agent.generate_graphs(summary)

        return {
            "summary": summary,
            "posts": posts,
            "images": images,
            "graphs": graphs
        }