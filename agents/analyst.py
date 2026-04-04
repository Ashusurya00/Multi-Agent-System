from crewai import Agent

analyst = Agent(
    role="Data Analyst",
    goal="Analyze research data and extract insights",
    backstory="Expert in identifying patterns and trends",
    verbose=True
)