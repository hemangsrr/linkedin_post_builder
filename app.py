import streamlit as st
from agents.coordinator import ResearchCoordinator

# Initialize the ResearchCoordinator
coordinator = ResearchCoordinator()

def set_api_keys():
    with st.form("API Keys", clear_on_submit=False):
        openai_key = st.text_input("OpenAI API Key", 
                                 type="password", 
                                 value=st.session_state.get("openai_key", ""))
        serp_key = st.text_input("SERP API Key", 
                                type="password", 
                                value=st.session_state.get("serp_key", ""))
        submitted = st.form_submit_button("Save")
        if submitted:
            st.session_state["openai_key"] = openai_key
            st.session_state["serp_key"] = serp_key
            st.success("API keys saved!")

def main():
    st.title("Research Assistant and LinkedIn Post Generator")
    st.write("Welcome! Provide a research topic and let the assistant find the latest articles and papers for you.")

    # Button to open API key popup
    if st.button("Set API Keys"):
        st.session_state["show_api_popup"] = True

    if st.session_state.get("show_api_popup", False):
        st.markdown("### Set API Keys")
        set_api_keys()
        if st.button("Close"):
            st.session_state["show_api_popup"] = False
        st.stop()

    # Check for API keys
    openai_key = st.session_state.get("openai_key", "")
    serp_key = st.session_state.get("serp_key", "")
    
    if not openai_key:
        st.error("Please set your OpenAI API key using the 'Set API Keys' button above.")
        st.stop()
    if not serp_key:
        st.error("Please set your SERP API key using the 'Set API Keys' button above.")
        st.stop()

    # Toggles for images and graphs
    col1, col2 = st.columns(2)
    with col1:
        generate_images = st.toggle("Generate Images (DALL·E)", value=False)
    with col2:
        generate_graphs = st.toggle("Generate Graphs", value=False)

    topic = st.text_input("Enter the research topic", "")

    if st.button("Search") and topic:
        st.write(f"🔎 Researching: {topic}...")

        # Pass toggles and API keys to coordinator
        result = coordinator.run(
            topic,
            openai_api_key=openai_key,
            serp_api_key=serp_key,
            generate_images=generate_images,
            generate_graphs=generate_graphs
        )

        st.subheader("Summary of Findings:")
        st.write(result.get("summary", "No research found."))

        st.subheader("LinkedIn Post Drafts:")
        posts = result.get("posts", [])
        if posts:
            for i, post in enumerate(posts, 1):
                st.markdown(f"**Post Option {i}**")
                st.write(post)
        else:
            st.write("No posts generated.")

        if generate_images and result.get("images"):
            st.subheader("Generated Images:")
            for img_url in result["images"]:
                st.image(img_url)

        if generate_graphs and result.get("graphs"):
            st.subheader("Generated Graphs:")
            for fig in result["graphs"]:
                st.pyplot(fig)

    elif topic == "":
        st.write("Please enter a topic to begin the search.")

if __name__ == "__main__":
    main()