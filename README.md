# Sales Intelligence Agent 🤖

A multi-agent AI pipeline that turns a company name into a personalized outreach email in under 20 seconds.

Built with Python, Groq (LLaMA 3.3), and Tavily. Includes a clean web UI for live demos.

---

## How It Works

Three specialized AI agents run in sequence, each with a distinct role and tuned parameters:

```
Input: Company Name
       │
       ▼
┌─────────────────────┐
│   Researcher Agent  │  Searches the web → structured company profile
│   LLaMA 3.1 · 0.2t │  (low temp = factual accuracy)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Analyst Agent     │  Reads profile → pain points + sales angles
│   LLaMA 3.3 · 0.5t │  (mid temp = strategic reasoning)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Writer Agent      │  Reads analysis → personalized email
│   LLaMA 3.3 · 0.7t │  (high temp = natural writing)
└──────────┬──────────┘
           │
           ▼
Output: Ready-to-send outreach email
```

Each agent's output becomes the next agent's input — this is **output chaining**, the core pattern of multi-agent orchestration.

---

## Features

- **Real web search** via Tavily — agents work with live data, not training memory
- **Temperature tuning** — each agent has a deliberately chosen temperature based on its job
- **Web UI** with live agent progress via Server-Sent Events (SSE)
- **CLI mode** — run directly from terminal without the UI
- **Auto-saves** full pipeline output (profile + analysis + email) to a `.txt` file

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM inference | [Groq](https://groq.com) — LLaMA 3.3 70B + LLaMA 3.1 8B |
| Web search | [Tavily](https://tavily.com) — AI-optimized search API |
| Web framework | [Flask](https://flask.palletsprojects.com) |
| Streaming | Server-Sent Events (SSE) |
| Language | Python 3.10+ |

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/sales-agent.git
cd sales-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add API keys
```bash
cp .env.example .env
```
Open `.env` and add your keys:
- **Groq** (free): [console.groq.com](https://console.groq.com) → API Keys
- **Tavily** (free, 1000 searches/month): [app.tavily.com](https://app.tavily.com)

```env
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly-...
```

---

## Running

### Web UI (recommended for demos)
```bash
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser. Watch all three agents fire in real time.

### CLI mode
```bash
python main.py
```

---

## Project Structure

```
sales-agent/
├── app.py                 # Flask server + SSE streaming
├── main.py                # CLI orchestrator
├── requirements.txt
├── .env.example
├── agents/
│   ├── researcher.py      # Agent 1 — web research
│   ├── analyst.py         # Agent 2 — pain point analysis
│   └── writer.py          # Agent 3 — email drafting
├── tools/
│   └── search.py          # Tavily web search wrapper
└── templates/
    └── index.html         # Web UI
```

---

## What I Learned / Product Decisions

- **Why separate agents instead of one big prompt?** Separation of concerns. Each agent can be individually improved, swapped, or tested without breaking the others. This mirrors how real AI products like Clay and Apollo are built.

- **Why different temperatures per agent?** Research needs accuracy (0.2), analysis benefits from creative angles (0.5), writing sounds more human with higher variance (0.7). Temperature is a product decision, not just a technical one.

- **Why Tavily over the OpenAI web plugin?** Tavily returns clean, structured text optimized for LLM consumption. Raw web scraping returns HTML noise. For agent pipelines, input quality directly determines output quality.

- **Why SSE over WebSockets for the UI?** SSE is simpler (plain HTTP), one-directional (server → client), and perfect for this use case. WebSockets add complexity when you don't need bi-directional communication.

---

## Author

**Prateek Bhoge** — Product Manager · AI & Enterprise SaaS

[LinkedIn](https://linkedin.com/in/prateekbhoge) · prateekbhoge320@gmail.com
