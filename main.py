from crewai import Task, Crew

from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer
from agents.reviewer import reviewer
from dotenv import load_dotenv
import os

load_dotenv()

# Step 1: Research
research_task = Task(
    description="Research AI job trends in 2025",
    agent=researcher,
    expected_output="Detailed research findings"
)

# Step 2: Analysis
analysis_task = Task(
    description="Analyze the research and extract key insights",
    agent=analyst,
    expected_output="Key insights and trends",
    context=[research_task]
)

# Step 3: Writing
writing_task = Task(
    description="Write a structured report based on insights",
    agent=writer,
    expected_output="Professional report",
    context=[analysis_task]
)

# Step 4: Review
review_task = Task(
    description="Review and improve the final report",
    agent=reviewer,
    expected_output="Polished final report",
    context=[writing_task]
)

crew = Crew(
    agents=[researcher, analyst, writer, reviewer],
    tasks=[research_task, analysis_task, writing_task, review_task],
    verbose=True,
    memory=True
)

result = crew.kickoff()

print("\nFINAL OUTPUT:\n")
print(result)