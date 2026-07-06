from typing import Callable, Dict, Any

from tools import scrape_url, web_search


def build_search_agent() -> Dict[str, Callable[[str], Any]]:
    return {"search": lambda topic: web_search(topic, max_results=5)}


def build_reader_agent() -> Dict[str, Callable[[str], str]]:
    return {"read": lambda url: scrape_url(url)}
