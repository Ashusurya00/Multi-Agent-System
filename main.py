"""
NEXUS · Multi-Agent Intelligence Platform
CLI Entry Point — run the pipeline from the terminal with rich output.

Usage:
    python main.py --topic "AI trends in 2025"
    python main.py --topic "Quantum computing" --model gpt-4o --no-memory
"""

import argparse
import sys
import time
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from crewai import Task, Crew
from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer
from agents.reviewer import reviewer
from config.settings import settings
from utils.helpers import (
    export_markdown, export_txt, export_json,
    get_report_metrics, format_elapsed, sanitize_filename
)
from utils.logger import get_logger

logger = get_logger(__name__)

DIVIDER = "─" * 70


def banner():
    print(f"\n{'═'*70}")
    print("  ⬡  NEXUS · Multi-Agent Intelligence Platform  v" + settings.app_version)
    print(f"{'═'*70}\n")


def section(title: str):
    print(f"\n  ◈ {title}")
    print(f"  {DIVIDER}")


def run_pipeline(topic: str, memory: bool = True, save_output: bool = True) -> str | None:
    """Execute the full 4-agent pipeline and return the final report."""

    banner()
    print(f"  Topic   : {topic}")
    print(f"  Model   : {settings.model_name}")
    print(f"  Memory  : {'enabled' if memory else 'disabled'}")
    print(f"  Started : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start = time.time()

    # ── Task Definitions ─────────────────────────────────────────────────────
    research_task = Task(
        description=(
            f"Conduct comprehensive research on: '{topic}'. "
            "Search the web for current facts, statistics, expert opinions, "
            "key players, recent developments, market data, and context. "
            "Organize findings under clear subheadings. Cite sources where possible."
        ),
        agent=researcher,
        expected_output=(
            "A thorough research brief with sections covering: current state, "
            "key data/statistics, major players, recent developments, challenges, "
            "and opportunities. Minimum 400 words."
        ),
    )

    analysis_task = Task(
        description=(
            "Using the research findings provided, perform a deep analytical assessment. "
            "Identify: (1) top 5 key trends with supporting data, "
            "(2) SWOT analysis framework, "
            "(3) quantitative metrics and their significance, "
            "(4) risk factors and mitigation strategies, "
            "(5) strategic implications."
        ),
        agent=analyst,
        context=[research_task],
        expected_output=(
            "Structured analytical report with executive insights, trend analysis, "
            "SWOT framework, risk matrix, and 5–7 evidence-backed strategic findings."
        ),
    )

    writing_task = Task(
        description=(
            "Using the analytical insights, write a comprehensive professional report with: "
            "(1) Executive Summary, (2) Background & Context, "
            "(3) Key Findings & Analysis, (4) Strategic Implications, "
            "(5) Risks & Considerations, (6) Recommendations (5+ specific items), "
            "(7) Conclusion & Outlook. Tone: authoritative, objective, strategic."
        ),
        agent=writer,
        context=[analysis_task],
        expected_output=(
            "A fully structured intelligence report with all 7 sections, "
            "clear headings, data references, and actionable recommendations. "
            "Minimum 600 words."
        ),
    )

    review_task = Task(
        description=(
            "Critically review and elevate the draft report. Tasks: "
            "(1) Strengthen executive summary, "
            "(2) Verify all claims have supporting logic, "
            "(3) Sharpen recommendations to be specific and measurable, "
            "(4) Improve flow and clarity, "
            "(5) Add '⚡ Key Takeaways' section with 5 bullet points at the top, "
            "(6) Add 'Future Outlook' subsection in the conclusion."
        ),
        agent=reviewer,
        context=[writing_task],
        expected_output=(
            "The final polished intelligence report with: Key Takeaways section, "
            "all 7 body sections, verified recommendations, and Future Outlook. "
            "Executive-ready."
        ),
    )

    # ── Agent Execution Tracking ─────────────────────────────────────────────
    agent_labels = [
        ("🔭", "Senior Research Specialist"),
        ("📊", "Strategic Intelligence Analyst"),
        ("✍️", "Principal Technical Writer"),
        ("⚖️", "Senior Editorial Director"),
    ]

    section("Executing Pipeline")

    crew = Crew(
        agents=[researcher, analyst, writer, reviewer],
        tasks=[research_task, analysis_task, writing_task, review_task],
        verbose=settings.agent_verbose,
        memory=memory,
    )

    for icon, label in agent_labels:
        print(f"  {icon}  {label} ... ", end="", flush=True)

    print()  # newline after the agent list

    print(f"\n  ⏳ Running crew pipeline...\n")
    result = crew.kickoff()

    elapsed = time.time() - start
    metrics = get_report_metrics(result.raw)

    # ── Results ──────────────────────────────────────────────────────────────
    section("Pipeline Complete")
    print(f"  ✅ Completed in {format_elapsed(elapsed)}")
    print(f"  📄 Words       : {metrics['words']:,}")
    print(f"  ⏱  Reading time : ~{metrics['reading_time']} min")
    print(f"  📋 Sections    : {metrics['paragraphs']}")

    section("Final Intelligence Report")
    print()
    print(result.raw)

    # ── Save Output ───────────────────────────────────────────────────────────
    if save_output:
        safe_name = sanitize_filename(topic)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = Path(settings.output_dir)
        out_dir.mkdir(exist_ok=True)

        agent_data = []
        for (icon, role), task_out in zip(agent_labels, result.tasks_output):
            agent_data.append({"name": role, "icon": icon, "role": role, "output": task_out.raw})

        md_path = out_dir / f"{safe_name}_{ts}.md"
        json_path = out_dir / f"{safe_name}_{ts}.json"

        md_path.write_bytes(export_markdown(topic, result.raw, agent_data))
        json_path.write_bytes(export_json(topic, result.raw, agent_data))

        section("Outputs Saved")
        print(f"  📝 Markdown : {md_path}")
        print(f"  📦 JSON     : {json_path}")

    print(f"\n{'═'*70}\n")
    return result.raw


def main():
    parser = argparse.ArgumentParser(
        description="NEXUS · Multi-Agent Intelligence Platform CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "AI trends in 2025"
  python main.py --topic "Quantum computing" --model gpt-4o
  python main.py --topic "Climate tech" --no-memory --no-save
        """,
    )
    parser.add_argument("--topic", "-t", type=str, help="Research topic")
    parser.add_argument("--model", "-m", type=str, default=settings.model_name, help="OpenAI model name")
    parser.add_argument("--no-memory", action="store_true", help="Disable crew memory")
    parser.add_argument("--no-save", action="store_true", help="Don't save output files")

    args = parser.parse_args()

    if not args.topic:
        topic = input("  Enter research topic: ").strip()
        if not topic:
            print("  Error: topic is required.")
            sys.exit(1)
    else:
        topic = args.topic

    os.environ["MODEL_NAME"] = args.model
    settings.model_name = args.model

    run_pipeline(
        topic=topic,
        memory=not args.no_memory,
        save_output=not args.no_save,
    )


if __name__ == "__main__":
    main()
