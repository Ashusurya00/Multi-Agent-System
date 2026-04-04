from crewai import Agent

writer = Agent(
    role="Technical Writer",
    goal="Write a clear and structured report",
    backstory="Expert in creating professional reports",
    verbose=True
)