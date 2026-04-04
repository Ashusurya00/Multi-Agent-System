from crewai import Agent

reviewer = Agent(
    role="Quality Reviewer",
    goal="Improve clarity and correctness of report",
    backstory="Expert in reviewing and refining content",
    verbose=True
)