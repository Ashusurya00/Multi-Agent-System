"""
Enterprise Web Search Tool
DuckDuckGo-powered search with structured results, deduplication, and retries.
"""

import time
import random
from crewai.tools import BaseTool
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# Support both old (duckduckgo_search) and new (ddgs) package names gracefully
try:
    from ddgs import DDGS
    logger.info("[SearchTool] Using 'ddgs' package")
except ImportError:
    try:
        from duckduckgo_search import DDGS
        logger.info("[SearchTool] Using 'duckduckgo_search' package")
    except ImportError:
        DDGS = None
        logger.error("[SearchTool] Neither 'ddgs' nor 'duckduckgo_search' is installed.")


class SearchTool(BaseTool):
    """
    Enterprise-grade web search using DuckDuckGo.

    Features:
    - Auto-detects ddgs vs duckduckgo_search package
    - Retry with exponential back-off on rate limits / empty results
    - Random jitter between retries to avoid hammering the API
    - Result deduplication by URL
    - Structured output with source attribution
    """

    name: str = "Web Search"
    description: str = (
        "Search the web for current, accurate information on any topic. "
        "Returns structured results with titles, snippets, and sources. "
        "Use this to gather factual, up-to-date data before forming conclusions."
    )

    def _run(self, query: str) -> str:
        if DDGS is None:
            return (
                "Search tool unavailable: install the search package with "
                "'pip install ddgs' then restart."
            )

        max_results = settings.max_search_results
        retries = 4
        base_delay = 3.0

        logger.info(f"[SearchTool] Query: '{query}' | Max results: {max_results}")

        for attempt in range(retries):
            # Progressive delay with jitter to avoid rate-limits
            if attempt > 0:
                wait = base_delay * attempt + random.uniform(0.5, 1.5)
                logger.info(f"[SearchTool] Waiting {wait:.1f}s before attempt {attempt+1}…")
                time.sleep(wait)

            try:
                seen_urls: set[str] = set()
                results: list[str] = []

                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=max_results):
                        url = r.get("href", "")
                        if url in seen_urls:
                            continue
                        seen_urls.add(url)
                        title = r.get("title", "Untitled")
                        body = r.get("body", "").strip()
                        if body:
                            results.append(f"[{title}] {body}\nSource: {url}")

                if results:
                    logger.info(f"[SearchTool] Returned {len(results)} results")
                    return "\n\n".join(results)

                logger.warning(
                    f"[SearchTool] Empty result on attempt {attempt+1} for: '{query}'"
                )

            except Exception as exc:
                logger.warning(f"[SearchTool] Attempt {attempt+1} error: {exc}")

        # All retries exhausted — tell the agent to reason from its own knowledge
        logger.warning(f"[SearchTool] All retries exhausted for: '{query}'")
        return (
            f"Web search returned no results for '{query}' after {retries} attempts "
            "(likely DuckDuckGo rate-limiting). "
            "Please answer using your own up-to-date training knowledge."
        )
