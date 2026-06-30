import os
import json
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool


load_dotenv()

t = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def web_searching(query: str) -> str:
    """
    Perform a web search and give recent and reliable information.
    Returns title, URL and snippet.
    """

    try:
        response = t.search(
            query=query,
            max_results=2
        )

        out = []

        for r in response["results"]:
            out.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content")
            })

        return json.dumps(
            out,
            indent=4
        )

    except Exception as e:
        return f"Search error: {e}"



@tool
def url_scrape(url: str) -> str:
    """
    Scrape the content of a given URL.
    Returns cleaned text content.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # remove unwanted sections
        for tag in soup(
            ["script", "style", "nav",
             "footer", "header", "aside"]
        ):
            tag.decompose()


        text = soup.get_text(
            separator="\n"
        )

        cleaned = "\n".join(
            line.strip()
            for line in text.splitlines()
            if line.strip()
        )

        return cleaned[:5000]


    except Exception as e:
        return f"Error scraping URL: {e}"
