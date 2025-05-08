from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from typing import List, Optional

class SummaryAgent:
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
        
    def _prepare_sources_text(self, sources: List[dict]) -> tuple[str, List[str]]:
        """Helper method to format sources text and collect references"""
        combined_text = ""
        reference_links = []
        
        for i, source in enumerate(sources):
            label = "[Web Article]" if source.get("type") == "web" else "[Research Paper]"
            combined_text += f"{label} {source.get('title', 'Untitled')}\n{source.get('summary', '')}\n\n"

            if "link" in source and len(reference_links) < 5:  # Limit to 5 references
                reference_links.append(f"{i+1}. [{source['title']}]({source['link']})")
                
        return combined_text, reference_links

    def summarize(self, sources: List[dict]) -> str:
        """Generate a readable summary from mixed research results with references.
        
        Args:
            sources: List of research sources (web articles and papers)
            
        Returns:
            Formatted summary with references if available
            
        Raises:
            RuntimeError: If LLM is not initialized with API key
        """
        if not self.llm:
            raise RuntimeError("OpenAI API key not set. Call set_api_key() first.")

        print("[SummaryAgent] Summarizing combined research...")
        combined_text, reference_links = self._prepare_sources_text(sources)

        prompt = (
            "Summarize the following research content into a clear, concise explanation "
            "for a general audience:\n\n" + combined_text
        )

        messages = [
            SystemMessage(content="You are a helpful research assistant."),
            HumanMessage(content=prompt)
        ]

        response = self.llm.invoke(messages)
        summary = response.content

        if reference_links:
            summary += "\n\n**References:**\n" + "\n".join(reference_links)

        return summary

    def generate_posts(self, summary: str, tone: str = "professional", num_posts: int = 3) -> List[str]:
        """Generate LinkedIn-style posts from the summary.
        
        Args:
            summary: Research summary to base posts on
            tone: Desired tone ('professional', 'casual', 'enthusiastic')
            num_posts: Number of post variations to generate
            
        Returns:
            List of generated post strings
            
        Raises:
            RuntimeError: If LLM is not initialized with API key
        """
        if not self.llm:
            raise RuntimeError("OpenAI API key not set. Call set_api_key() first.")

        print(f"[SummaryAgent] Generating {num_posts} LinkedIn posts...")

        system_prompt = f"""You are a professional content writer for LinkedIn.
            Using the research summary below, write {num_posts} LinkedIn posts that are:
            - Insightful and informative
            - Use a {tone.lower()} tone
            - Avoid jargon
            - Each post should stand on its own
            - Include relevant hashtags (3-5)
            - Format with clear paragraphs and line breaks
            - Length: 3-5 paragraphs each
            ---
            Return ONLY the posts, numbered as:
            1. [First post content]
            2. [Second post content]
            etc."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Research Summary:\n{summary}")
        ]

        response = self.llm.invoke(messages)
        return self._parse_post_response(response.content)
        
    def _parse_post_response(self, response_text: str) -> List[str]:
        """Helper to parse the LLM response into separate posts"""
        posts = []
        current_post = []
        
        for line in response_text.split('\n'):
            if line.startswith(('1.', '2.', '3.', '4.', '5.')) and current_post:
                posts.append('\n'.join(current_post).strip())
                current_post = []
            current_post.append(line)
            
        if current_post:
            posts.append('\n'.join(current_post).strip())
            
        return posts or [response_text.strip()]  # Fallback if parsing fails