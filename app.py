import streamlit as st
from crewai import Task, Crew

from agents.researcher import researcher
from agents.analyst import analyst
from agents.writer import writer
from agents.reviewer import reviewer

# ---------------- UI CONFIG ---------------- #
st.set_page_config(
    page_title="Multi-Agent AI System",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #4CAF50;
        }
        .sub-text {
            color: gray;
            font-size: 1rem;
        }
        .result-box {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown('<p class="main-title">🤖 Multi-Agent AI System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Generate intelligent reports using AI agents (Research → Analyze → Write → Review)</p>', unsafe_allow_html=True)

st.divider()

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.header("⚙️ Settings")
    show_steps = st.toggle("Show Agent Workflow", value=False)
    use_memory = st.toggle("Enable Memory", value=True)

    st.markdown("---")
    st.markdown("### 💡 Example Topics")
    st.write("• AI job trends")
    st.write("• Future of startups")
    st.write("• Blockchain in finance")

# ---------------- INPUT ---------------- #
user_input = st.text_input("💬 Enter your topic:")

col1, col2 = st.columns([1,1])

with col1:
    generate_btn = st.button("🚀 Generate Report", use_container_width=True)

with col2:
    clear_btn = st.button("🧹 Clear", use_container_width=True)

# ---------------- CLEAR ---------------- #
if clear_btn:
    st.rerun()

# ---------------- PROCESS ---------------- #
if generate_btn:

    if not user_input:
        st.warning("⚠️ Please enter a topic")
    else:
        with st.spinner("🤖 Agents are working..."):

            # Tasks
            research_task = Task(
                description=f"Research about {user_input}",
                agent=researcher,
                expected_output="Detailed research"
            )

            analysis_task = Task(
                description="Analyze research and extract insights",
                agent=analyst,
                context=[research_task],
                expected_output="Insights"
            )

            writing_task = Task(
                description="Write structured report",
                agent=writer,
                context=[analysis_task],
                expected_output="Report"
            )

            review_task = Task(
                description="Improve and finalize report",
                agent=reviewer,
                context=[writing_task],
                expected_output="Final report"
            )

            crew = Crew(
                agents=[researcher, analyst, writer, reviewer],
                tasks=[research_task, analysis_task, writing_task, review_task],
                verbose=False,
                memory=use_memory
            )

            result = crew.kickoff()

        st.success("✅ Report Generated!")

        # ---------------- OUTPUT ---------------- #
        st.subheader("📄 Final Report")
        st.markdown(f'<div class="result-box">{result.raw}</div>', unsafe_allow_html=True)

        # ---------------- WORKFLOW ---------------- #
        if show_steps:
            st.subheader("🔍 Agent Workflow")

            for i, task in enumerate(result.tasks_output):
                with st.expander(f"Step {i+1}: {task.description}"):
                    st.write(task.raw)