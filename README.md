# 🤖 Multi-Agent AI System for Automated Report Generation

## 🚀 Overview

This project is a **production-ready multi-agent AI system** that automates the process of research, analysis, report writing, and review using multiple collaborating AI agents.

Unlike traditional single LLM-based systems, this solution uses a **multi-agent architecture** where each agent performs a specialized role, resulting in more structured, accurate, and high-quality outputs.

---

## 🎯 Problem Statement

Generating structured insights from large or dynamic information sources is time-consuming and requires multiple steps:

* Researching data
* Analyzing insights
* Writing reports
* Reviewing content

Traditional LLMs provide generic responses but lack **structured reasoning and role-based processing**.

👉 This project solves that by automating the entire workflow using **AI agents**.

---

## 🧠 Solution

The system is designed as a **multi-agent pipeline** where agents collaborate sequentially:

Researcher → Analyst → Writer → Reviewer

Each agent:

* Has a defined role
* Receives context from previous agents
* Produces structured output

---

## 🏗️ Architecture

User Input
↓
Research Agent → Analysis Agent → Writer Agent → Reviewer Agent
↓
Final Report

---

## ⚙️ Tech Stack

### 🧠 Core AI

* CrewAI (Multi-agent orchestration)
* LangChain (LLM integration)

### 🤖 LLM

* OpenAI API

### 🌐 Tools

* DuckDuckGo Search (real-time data retrieval)

### 🖥️ Frontend

* Streamlit (interactive UI)

### 🧠 Memory

* CrewAI built-in memory
* Custom memory module

### 📦 Other

* Python
* dotenv
* Virtual environment

---

## 🔥 Features

### ✅ Multi-Agent Collaboration

Specialized agents handle different stages of the workflow.

### ✅ Context-Aware Processing

Agents communicate using context passing for better reasoning.

### ✅ Real-Time Web Search

Integrated search tool for up-to-date information.

### ✅ Memory Integration

Maintains context across tasks for improved output consistency.

### ✅ Interactive UI

Built using Streamlit for user-friendly interaction.

---

## 📂 Project Structure

multi-agent-system/
│
├── app.py
├── main.py
├── agents/
│   ├── researcher.py
│   ├── analyst.py
│   ├── writer.py
│   ├── reviewer.py
│
├── tools/
├── memory/
├── requirements.txt
├── README.md

---

## ▶️ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multi-agent-system.git
cd multi-agent-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```

---

## 🧪 Example Use Cases

* AI job market analysis
* Business trend reports
* Technology research
* Market insights generation

---

## ⚠️ Challenges & Solutions

### 🔴 Tool Compatibility Issue

* Problem: LangChain tools not compatible with CrewAI
* Solution: Implemented custom tool using BaseTool

### 🔴 API Key Errors

* Problem: Missing environment variables
* Solution: Used dotenv for secure configuration

### 🔴 Output Formatting

* Problem: Raw JSON output
* Solution: Extracted clean output using `result.raw`

### 🔴 Environment Issues

* Problem: Python version conflicts
* Solution: Used Python 3.10 for stability

---

## 🚀 Future Improvements

* Add LangGraph for advanced workflows
* Integrate vector database (FAISS/Pinecone)
* Add chat-based UI
* Enable PDF export
* Deploy on cloud platforms

---

## 🏆 Key Learnings

* Multi-agent system design
* Tool integration in AI workflows
* Context management and memory
* Real-world AI deployment

---

## 👨‍💻 Author

Ashutosh Suryawanshi

* GitHub: https://github.com/Ashusurya00
* LinkedIn: https://linkedin.com/in/ashutosh-suryawanshi-26aa46378

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and connect with me!
