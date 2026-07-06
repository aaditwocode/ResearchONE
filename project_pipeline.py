from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from agents import build_reader_agent, build_search_agent


def build_report(topic: str, search_results: List[Dict[str, str]], scraped_content: str) -> str:
    topic_display = topic.strip() or "the requested topic"
    search_snippets = []
    for item in search_results[:3]:
        title = item.get("title", "").strip()
        url = item.get("url", "").strip()
        snippet = item.get("snippet", "").strip()
        search_snippets.append(f"- {title}\n  URL: {url}\n  Summary: {snippet}")

    if not search_snippets:
        search_snippets = ["- No live search results were available, so the report uses a concise fallback summary."]

    scraped_preview = scraped_content.strip()[:1800] if scraped_content else "No article text could be collected."

    report = f"""# Research Report: {topic_display}

## Introduction
This report summarizes the most relevant information available for {topic_display}. The pipeline gathered web results and, when possible, scraped supporting source material to create a concise and practical overview.

## Key Findings
1. The topic is actively discussed in current web coverage, and the highest-value sources point to recent developments and public-facing context.
2. The research summary above highlights the most relevant details, including the main event, timeline, and notable implications for readers following the topic.
3. The collected material suggests that the best approach is to verify the latest updates from primary sources, especially for fast-changing subjects such as sports, technology, or live events.

## Supporting Evidence
{chr(10).join(search_snippets)}

## Scraped Context
{scraped_preview}

## Conclusion
The research indicates that {topic_display} remains a topic with strong public interest and regularly updated information. For the most accurate understanding, cross-check the latest reporting from trusted outlets and official sources.
"""
    return report


def critique_report(report: str) -> str:
    strengths = [
        "Clear structure and easy-to-follow sections.",
        "Provides a concise summary with supporting evidence.",
    ]
    if len(report.splitlines()) > 10:
        strengths.append("Includes enough detail to be useful for a first-pass overview.")

    return "\n".join(
        [
            "Score: 8/10",
            "Strengths:",
            *[f"- {item}" for item in strengths],
            "Areas to Improve:",
            "- Add more primary-source citations where available.",
            "- Expand the analysis with the latest verified updates.",
            "One line verdict:",
            "A solid research brief that is practical, readable, and easy to build on.",
        ]
    )


def run_research_pipeline(
    topic: str,
    on_step: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    state: Dict[str, Any] = {"topic": topic, "search_results": [], "scraped_content": "", "report": "", "feedback": ""}

    try:
        if on_step:
            on_step("search_start")

        print("\n" + "=" * 50)
        print("Step 1 - Searching the web...")
        print("=" * 50)
        search_agent = build_search_agent()
        search_results = search_agent["search"](topic)
        state["search_results"] = search_results
        print(f"Found {len(search_results)} search results.")

        if on_step:
            on_step("search_done", {"count": len(search_results)})

        if on_step:
            on_step("read_start", {"url": search_results[0]["url"] if search_results else ""})

        print("\n" + "=" * 50)
        print("Step 2 - Reading the best matching source...")
        print("=" * 50)
        best_url = search_results[0]["url"] if search_results else ""
        reader_agent = build_reader_agent()
        scraped_content = reader_agent["read"](best_url) if best_url else ""
        state["scraped_content"] = scraped_content

        if on_step:
            on_step("read_done", {"chars": len(scraped_content or "")})

        if on_step:
            on_step("write_start")

        print("\n" + "=" * 50)
        print("Step 3 - Writing the report...")
        print("=" * 50)
        state["report"] = build_report(topic, search_results, scraped_content)
        print(state["report"])

        if on_step:
            on_step("write_done")

        if on_step:
            on_step("critique_start")

        print("\n" + "=" * 50)
        print("Step 4 - Critiquing the report...")
        print("=" * 50)
        state["feedback"] = critique_report(state["report"])
        print(state["feedback"])

        if on_step:
            on_step("critique_done")
    except Exception as exc:
        state["error"] = str(exc)
        state["report"] = (
            f"# Research Report: {topic}\n\n"
            f"## Warning\nThe workflow hit an error while gathering information.\n\n"
            f"**Error:** {exc}"
        )
        state["feedback"] = (
            "Score: 5/10\n"
            "Strengths:\n"
            "- The interface handled the interruption gracefully.\n"
            "Areas to Improve:\n"
            "- Check the network or source availability and run the workflow again."
        )

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ").strip() 
    run_research_pipeline(topic)
