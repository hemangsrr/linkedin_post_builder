# LinkedIn Research Agent

This project is a LinkedIn Research Agent that performs research on specific topics, summarizes the research findings, and generates LinkedIn-style posts based on the summary. It leverages advanced Natural Language Processing (NLP) and Large Language Models (LLMs), such as OpenAI's GPT models, to automate the entire research and content creation process.

## Features

- **Research Agent**: Gathers research from multiple sources like web articles and research papers based on a topic.
- **Summarizer**: Summarizes the combined research into a concise, clear explanation.
- **Post Generator**: Generates LinkedIn-style posts based on the summarized content.
  
## Requirements

To run this project, you'll need to have Python and some dependencies installed.

### Python Version:
- Python 3.7 or higher

### Dependencies:
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [requests](https://requests.readthedocs.io/en/master/)

Install the dependencies using:

```bash
pip install -r requirements.txt
```

## Setup and Usage

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/LinkedInAgent.git
```

### 2. Set Up Environment
Create a virtual environment (optional, but recommended):

```bash
python -m venv linkenv
```

Activate the virtual environment:

On Windows:

```bash
linkenv\Scripts\activate
```

On macOS/Linux:

```bash
source linkenv/bin/activate
```

### 3. Install Dependencies
After activating the virtual environment, install the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 4. Running the App
To run the app, use Streamlit:

```bash
streamlit run app.py
```

This will start a local Streamlit server. You can access the app by visiting [http://localhost:8501](http://localhost:8501) in your browser.

### 5. Interacting with the App
Once the app is running, you can input a topic (e.g., "AI in LinkedIn marketing") in the search box. The app will:

- Perform a web search and fetch articles related to the topic.
- Search for relevant research papers.
- Summarize the collected content into a short, easy-to-understand explanation.
- Generate LinkedIn-style posts based on the summary.

## Structure

The project has the following structure:

```
LinkedInAgent/
│
├── agents/
│   ├── coordinator.py       # Coordinates the flow of the research process
│   ├── paper_research_agent.py  # Handles the research papers search
│   ├── summary_agent.py      # Summarizes the results and generates posts
│   └── web_research_agent.py  # Handles the web search for articles
│
├── app.py                  # The main entry point for running the app (Streamlit)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Code Explanation

### coordinator.py
**Purpose**: Coordinates the overall process: from fetching research articles and papers to summarizing and generating posts.

**Main Logic**: Initiates web and paper research, and then calls the summarizer to create a concise summary of the research.

### summary_agent.py
**Purpose**: Summarizes the research content and generates LinkedIn posts.

**Main Logic**: It first combines the research findings, then generates a summary and finally creates LinkedIn-style posts.

### app.py
**Purpose**: Starts the Streamlit app and runs the coordinator.

**Main Logic**: This file handles user input and displays the results in the Streamlit interface.

## Usage Example

When running the Streamlit app, you will be prompted to input a topic. For example:

**Topic**: AI in LinkedIn Marketing

The app will:

1. Fetch web articles related to the topic.
2. Search research papers on arXiv for the same topic.
3. Combine the research findings and generate a summary.
4. Create 3 LinkedIn posts based on the summary.

### Example of Generated Posts:

**Post 1**:  
"AI is revolutionizing how we approach marketing on LinkedIn. By leveraging machine learning algorithms, businesses can now automate their content creation and targeting strategies to enhance engagement..."

**Post 2**:  
"In recent studies, the role of AI in LinkedIn marketing has shown great potential. AI-driven personalization is one of the key drivers behind increased conversion rates..."

**Post 3**:  
"As LinkedIn continues to grow as a professional network, AI is helping businesses harness user data to refine their outreach strategies, ultimately boosting ROI for companies looking to target professionals in specific industries..."

## Contributing

If you'd like to contribute to this project, feel free to fork the repository, create a branch, and submit a pull request. All contributions are welcome!

## License

This project is open-source and available under the MIT License.