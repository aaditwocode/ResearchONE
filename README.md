# ResearchONE
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/aaditwocode/ResearchONE)

ResearchONE is a multi-agent research assistant that transforms any topic into a clean, polished research brief. Instead of just a list of links, it uses a chain of specialized agents to search, read, write, and critique, delivering a structured and sourced report directly in an interactive web interface.

## How It Works

The application uses a four-step agent pipeline to process a research request. The entire process is visualized live in the Streamlit UI.

1.  **🔍 Search Agent**: Queries the web for the user's topic to find relevant, up-to-date sources. It uses the Tavily API for high-quality results and gracefully falls back to DuckDuckGo if an API key is not provided.

2.  **📖 Reader Agent**: Scrapes the full text content from the top-ranked URL returned by the Search Agent. This provides deep context for the report, ensuring it is grounded in real content, not just search snippets.

3.  **✍️ Writer Agent**: Synthesizes the search results and the scraped article content into a structured report. The output is formatted in Markdown and includes an introduction, key findings, supporting evidence, and a conclusion.

4.  **🧠 Critic Agent**: Reviews the generated report for quality and coherence. It provides a score (out of 10), lists the report's strengths, and suggests areas for improvement.

## Getting Started

### Using GitHub Codespaces (Recommended)

The easiest way to run ResearchONE is with GitHub Codespaces, which will configure the development environment for you automatically.

1.  Click the **Code** button on the repository page.
2.  Select the **Codespaces** tab.
3.  Click **Create a codespace on main**.

The environment will build, install all dependencies, and automatically launch the Streamlit application. A new tab will open in your browser with the running app.

### Local Installation

If you prefer to run the application on your local machine, follow these steps.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/aaditwocode/ResearchONE.git
    cd ResearchONE
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **(Optional) Configure API Key:**
    For the best search performance, create a `.env` file in the root directory and add your Tavily API key:
    ```
    TAVILY_API_KEY="your_tavily_api_key_here"
    ```
    If this file is not present, the application will use DuckDuckGo for web searches.

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    Open your web browser and navigate to `http://localhost:8501`.

## Project Structure

The repository is organized as follows:

```
/
├── app.py              # Main Streamlit application file (UI and front-end logic)
├── project_pipeline.py # Defines the core multi-agent research workflow
├── agents.py           # Builder functions for the search and reader agents
├── tools.py            # Implements web search (Tavily, DuckDuckGo) and URL scraping
├── requirements.txt    # Python dependencies
└── .devcontainer/      # Configuration for GitHub Codespaces & VS Code Dev Containers
