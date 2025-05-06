from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI  # Use this import for the latest version

class SummaryAgent:
    def __init__(self, model="gpt-4o", temperature=0.5):
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def summarize(self, sources: list) -> str:
        """Generate a readable summary from mixed research results, with references if available."""
        print("[SummaryAgent] Summarizing combined research...")

        combined_text = ""
        reference_links = []

        for i, s in enumerate(sources):
            label = "[Web Article]" if s.get("type") == "web" else "[Research Paper]"
            combined_text += f"{label} {s.get('title', 'Untitled')}\n{s.get('summary', '')}\n\n"

            # Attempt to include link if available
            try:
                if "link" in s and len(reference_links) < 5:
                    reference_links.append(f"{i+1}. [{s['title']}]({s['link']})")
            except Exception as e:
                # Log or ignore bad links, but don't crash
                print(f"[SummaryAgent] Skipped invalid link for source {i}: {e}")

        prompt = (
            "Summarize the following research content into a clear, concise explanation "
            "for a general audience:\n\n" + combined_text
        )

        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=prompt)
        ]

        response = self.llm(messages=messages)
        summary = response.content

        if reference_links:
            summary += "\n\n**References:**\n" + "\n".join(reference_links)

        return summary

    def generate_posts(self, summary: str, tone: str = "Professional") -> str:
        """Generate LinkedIn-style posts from the summary."""
        print("[SummaryAgent] Generating LinkedIn posts...")

        prompt = f'''
                Summary:
                \"\"\"
                {summary}
                \"\"\"
                '''
        
        system_prompt = f'''
                You are a professional content writer for LinkedIn.
                Using the research summary below, write 3 LinkedIn posts that are:
                - Insightful and informative
                - Use a {tone.lower()} tone
                - Avoid jargon
                - Each post should stand on its own
                '''
        
        # Create BaseMessage instances
        system_message = SystemMessage(content=system_prompt)
        user_message = HumanMessage(content=prompt)

        # Correctly format the prompt inside the messages using BaseMessage
        messages = [system_message, user_message]
        
        # Call the model with the properly formatted message
        response = self.llm(messages=messages)  # Use `messages=messages` to pass the correctly formatted list
        
        # Access the content correctly from the response (use .content instead of ['text'])
        return response.content  # Correctly access the content of the AIMessage
