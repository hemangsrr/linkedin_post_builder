from langchain_openai import ChatOpenAI
import matplotlib.pyplot as plt
from io import BytesIO
import json
from typing import List, Optional

class GraphAgent:
    def __init__(self, model: str = "gpt-4", temperature: float = 0.5):
        self.model = model
        self.temperature = temperature
        self.llm: Optional[ChatOpenAI] = None  # Will be initialized with API key

    def set_api_key(self, api_key: str):
        """Initialize the LLM with the provided API key"""
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            openai_api_key=api_key
        )

    def generate_graphs(self, summary: str) -> List[BytesIO]:
        """Generate graphs based on the summary using LangChain and matplotlib.
        
        Args:
            summary: Text summary to base graphs on
            
        Returns:
            List containing BytesIO objects with graph images
            
        Raises:
            RuntimeError: If API key is not set
        """
        if not self.llm:
            raise RuntimeError("OpenAI API key not set. Call set_api_key() first.")

        print("[GraphAgent] Generating graphs...")

        try:
            # Use LangChain to generate graph descriptions
            messages = [
                {"role": "system", "content": "You are a data visualization expert. Generate graph data in JSON format that can be directly used to create matplotlib graphs. The JSON should include the following fields: 'title', 'x_label', 'y_label', 'x_data', 'y_data', and optionally 'type' (e.g., 'line', 'bar')."},
                {"role": "user", "content": f"Generate a graph description based on this summary: {summary}"}
            ]
            response = self.llm.invoke(messages)
            graph_description = response.content
            print(f"[GraphAgent] Graph description: {graph_description}")

            # Parse the JSON response
            graph_data = json.loads(graph_description)

            # Create the graph dynamically
            fig, ax = plt.subplots()
            graph_type = graph_data.get("type", "line")  # Default to line graph

            if graph_type == "line":
                ax.plot(graph_data["x_data"], graph_data["y_data"])
            elif graph_type == "bar":
                ax.bar(graph_data["x_data"], graph_data["y_data"])
            elif graph_type == "scatter":
                ax.scatter(graph_data["x_data"], graph_data["y_data"])
            else:
                raise ValueError(f"Unsupported graph type: {graph_type}")

            # Set graph labels and title
            ax.set_title(graph_data.get("title", "Generated Graph"))
            ax.set_xlabel(graph_data.get("x_label", "X-axis"))
            ax.set_ylabel(graph_data.get("y_label", "Y-axis"))

            # Save the graph to a BytesIO object
            buf = BytesIO()
            plt.savefig(buf, format="png", dpi=300, bbox_inches='tight')
            buf.seek(0)
            plt.close(fig)

            return [buf]

        except json.JSONDecodeError as e:
            print(f"[GraphAgent] Error parsing graph description JSON: {e}")
            return []
        except Exception as e:
            print(f"[GraphAgent] Error generating graphs: {e}")
            return []