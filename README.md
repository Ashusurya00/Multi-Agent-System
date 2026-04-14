# ⬡ NEXUS · Multi-Agent Intelligence Platform

> **Enterprise-grade multi-agent research & report generation system**
> powered by CrewAI, OpenAI, and a premium Streamlit UI.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![CrewAI](https://img.shields.io/badge/CrewAI-0.80%2B-purple?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

NEXUS orchestrates a **4-agent autonomous pipeline** that transforms any research topic into a polished, executive-grade intelligence report — in minutes.

```
🔭 Researcher  →  📊 Analyst  →  ✍️ Writer  →  ⚖️ Reviewer
```

Each agent is purpose-built with deep role context, specialized tools, and hand-off prompting for maximum output quality.

---

## Architecture

```
enterprise-multi-agent/
├── app.py                    # Premium Streamlit UI (main entry)
├── main.py                   # CLI runner with rich output
├── requirements.txt
├── .env.example
│
├── agents/
│   ├── researcher.py         # Senior Research Specialist (search + calculator)
│   ├── analyst.py            # Strategic Intelligence Analyst (calculator)
│   ├── writer.py             # Principal Technical Writer
│   └── reviewer.py           # Senior Editorial Director
│
├── tools/
│   ├── search_tool.py        # DuckDuckGo web search (retry, dedup, structured)
│   └── calculator_tool.py    # Safe math expression evaluator
│
├── config/
│   └── settings.py           # Pydantic settings with .env support
│
├── utils/
│   ├── helpers.py            # Export (MD/JSON/TXT), metrics, formatting
│   └── logger.py             # Structured logging
│
└── outputs/                  # Auto-generated reports (MD + JSON)
```

---

## Agent Pipeline

| Agent | Role | Tools | Responsibility |
|-------|------|-------|----------------|
| 🔭 **Researcher** | Senior Research Specialist | Web Search, Calculator | Multi-source research, data gathering, context building |
| 📊 **Analyst** | Strategic Intelligence Analyst | Calculator | SWOT analysis, trend identification, risk assessment |
| ✍️ **Writer** | Principal Technical Writer | — | Structured 7-section report creation |
| ⚖️ **Reviewer** | Senior Editorial Director | — | Quality assurance, strengthening recommendations, final polish |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/yourname/nexus-multi-agent.git
cd nexus-multi-agent
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run the web UI

```bash
streamlit run app.py
```

### 4. Or use the CLI

```bash
# Basic
python main.py --topic "AI trends in 2025"

# With GPT-4o
python main.py --topic "Quantum computing" --model gpt-4o

# Without memory, no file save
python main.py --topic "Climate tech" --no-memory --no-save
```

---

## Features

### Premium UI
- 🎨 Dark luxury aesthetic with animated agent pipeline visualization
- ⚡ Live agent status (idle → running → done) with glow effects
- 📊 Report metrics dashboard (word count, reading time, sections, gen. time)
- 💾 Multi-format export: Markdown, JSON, Plain Text
- 📂 Session history with quick-access sidebar
- 💡 Topic presets for one-click research
- 🔧 Runtime configuration: model, temperature, memory toggle

### Enterprise Backend
- 🔁 Retry logic with exponential back-off on search failures
- 🧹 Search result deduplication by URL
- 🛡️ Safe math evaluator (no `eval()` exploits)
- 📝 Structured logging across all modules
- ⚙️ Pydantic settings validation with `.env` support
- 📁 Auto-save reports as Markdown + JSON to `outputs/`
- 🏷️ Full metadata in JSON exports (topic, timestamp, metrics, agent trace)

### Report Quality
- Executive summary with 5-bullet key takeaways
- 7-section structured format (Background → Findings → Strategy → Risks → Recommendations → Outlook)
- SWOT analysis framework
- Specific, measurable recommendations
- Future Outlook subsection

---

## Configuration

All settings configurable via `.env` or environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | **Required.** OpenAI API key |
| `MODEL_NAME` | `gpt-4o-mini` | LLM model to use |
| `TEMPERATURE` | `0.3` | Generation temperature (0–1) |
| `MAX_TOKENS` | `4000` | Max tokens per LLM call |
| `AGENT_VERBOSE` | `false` | Enable CrewAI verbose logging |
| `MAX_ITERATIONS` | `10` | Max agent iteration loops |
| `ENABLE_MEMORY` | `true` | Enable CrewAI shared memory |
| `MAX_SEARCH_RESULTS` | `6` | Search results per query |
| `OUTPUT_DIR` | `outputs` | Directory for saved reports |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Technologies

- **[CrewAI](https://crewai.com/)** — Multi-agent orchestration framework
- **[OpenAI](https://openai.com/)** — LLM backbone (GPT-4o / GPT-4o-mini)
- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)** — Privacy-first web search
- **[Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)** — Configuration management
- **Google Fonts** — Syne, DM Sans, JetBrains Mono

---

## License

MIT © 2025 NEXUS Intelligence Platform
