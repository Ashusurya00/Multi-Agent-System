from crewai import Agent
from tools.search_tool import SearchTool

search_tool = SearchTool()

researcher = Agent(
    role="AI Researcher",
    goal="Find accurate and up-to-date information using web search",
    backstory="Expert in researching AI trends using online sources",
    tools=[search_tool],   # ✅ NOW CORRECT
    verbose=True
)