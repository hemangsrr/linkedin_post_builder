from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI  # Use this import for the latest version

class SummaryAgent:
    def __init__(self, model="gpt-4o", temperature=0.5):
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def summarize(self, sources: list) -> str:
        """Generate a readable summary from mixed research results."""
        print("[SummaryAgent] Summarizing combined research...")

        combined_text = ""
        for s in sources:
            label = "[Web Article]" if s["type"] == "web" else "[Research Paper]"
            combined_text += f"{label} {s['title']}\n{s['summary']}\n\n"

        # Format the prompt as a message for the chat model
        prompt = f"Summarize the following research content into a clear, concise explanation for a general audience:\n\n{combined_text}"

        # Correctly format the prompt inside the messages using BaseMessage
        system_message = SystemMessage(content="You are a helpful assistant.")
        user_message = HumanMessage(content=prompt)

        # Create a list of BaseMessage objects
        messages = [system_message, user_message]
        
        # Call the model with the properly formatted message
        response = self.llm(messages=messages)  # Use `messages=messages` to pass the correctly formatted list
        
        # Access the content correctly from the response (use .content instead of ['text'])
        return response.content  # Correctly access the content of the AIMessage

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
