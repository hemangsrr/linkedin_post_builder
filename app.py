import streamlit as st
from agents.coordinator import ResearchCoordinator

# Initialize the ResearchCoordinator
coordinator = ResearchCoordinator()

def main():
    # Streamlit page title
    st.title("Research Assistant and LinkedIn Post Generator")
    st.write("Welcome! Provide a research topic and let the assistant find the latest articles and papers for you.")

    # Input for research topic
    topic = st.text_input("Enter the research topic", "")

    # If the user submits the topic
    if st.button("Search") and topic:
        st.write(f"🔎 Researching: {topic}...")

        # Run the research process through the coordinator
        result = coordinator.run(topic)

        # Display summary
        st.subheader("Summary of Findings:")
        st.write(result["summary"] if result["summary"] else "No research found.")

        # Display LinkedIn Posts
        st.subheader("LinkedIn Post Drafts:")
        posts = result.get("posts", "")
        if posts:
            st.write(posts)
        else:
            st.write("No posts generated.")

    elif topic == "":
        st.write("Please enter a topic to begin the search.")

if __name__ == "__main__":
    main()
