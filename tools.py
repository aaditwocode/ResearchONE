import os
import re
from typing import List, Dict
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

try:
    from tavily import TavilyClient
except Exception:  # pragma: no cover - optional dependency
    TavilyClient = None


def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """Search the web and return recent results with title, URL, and snippet."""
    if TavilyClient and os.getenv("TAVILY_API_KEY"):
        try:
            client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
            response = client.search(query=query, max_results=max_results)
            results = []
            for item in response.get("results", []):
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("content", ""),
                    }
                )
            return results
        except Exception:
            pass

    return _duckduckgo_search(query, max_results=max_results)


def _duckduckgo_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results: List[Dict[str, str]] = []
    for item in soup.select(".result")[:max_results]:
        title_tag = item.select_one(".result__title a")
        snippet_tag = item.select_one(".result__snippet")
        if not title_tag:
            continue

        href = title_tag.get("href", "")
        url = href if href.startswith("http") else f"https://duckduckgo.com{href}"

        results.append(
            {
                "title": title_tag.get_text(" ", strip=True),
                "url": url,
                "snippet": snippet_tag.get_text(" ", strip=True) if snippet_tag else "",
            }
        )

    return results


def scrape_url(url: str, max_chars: int = 4000) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "noscript"]):
            tag.decompose()
        text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
        return text[:max_chars]
    except Exception as exc:
        return f"Could not scrape URL: {str(exc)}"