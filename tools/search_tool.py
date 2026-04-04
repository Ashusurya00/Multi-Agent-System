from crewai.tools import BaseTool
from duckduckgo_search import DDGS

class SearchTool(BaseTool):
    name: str = "Search Tool"
    description: str = "Search the web for latest information"

    def _run(self, query: str) -> str:
        results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r["body"])

        return "\n".join(results)