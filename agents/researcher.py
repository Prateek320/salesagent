"""
agents/researcher.py — The Researcher Agent
─────────────────────────────────────────────
Job: Given a company name, search the web and return a structured
     company profile (what they do, size, recent news, challenges).

PM Insight: This agent's system prompt is its "job description."
The more specific the prompt, the more focused the output.
Vague prompt → vague output. This is core prompt engineering.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from tools.search import web_search

load_dotenv()


def run_researcher(company_name: str) -> str:
    """
    Research a company and return a structured profile.

    Args:
        company_name: e.g. "Notion", "Stripe", "Figma"

    Returns:
        A structured text profile of the company.
    """

    print(f"\n🔍 [Researcher] Searching for info on: {company_name}...")

    # ── Step 1: Use our search TOOL to pull real web data ──────────────
    # We run two targeted searches to get richer data:
    # one for general overview, one for recent news/challenges
    overview_results = web_search(f"{company_name} company overview product 2024 2025")
    news_results     = web_search(f"{company_name} challenges growth news 2024 2025")

    # Combine both into one big context block for the LLM
    raw_research = f"""
=== OVERVIEW SEARCH RESULTS ===
{overview_results}

=== NEWS & CHALLENGES SEARCH RESULTS ===
{news_results}
"""

    # ── Step 2: Send raw research to the LLM to structure it ───────────
    # The LLM's job here is NOT to know about the company from memory —
    # it's to READ the search results and organize them cleanly.
    # This is called "grounding" — the LLM works from real data, not guesses.

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # Fast Groq model — perfect for structured extraction
        messages=[
            {
                # The SYSTEM message defines WHO the agent is and HOW it behaves.
                # This is the most important part of any agent — it's the "prompt engineering."
                "role": "system",
                "content": """You are a precise B2B research analyst.
Your job is to read raw search results and extract a clean, structured company profile.

Output EXACTLY this format — no extra commentary:

COMPANY: [name]
INDUSTRY: [industry / sector]
WHAT THEY DO: [1-2 sentences on their core product/service]
COMPANY SIZE: [employees / ARR / stage if known, else "Unknown"]
KEY CUSTOMERS: [types of customers they serve]
RECENT NEWS: [2-3 bullet points of notable recent developments]
KNOWN CHALLENGES: [2-3 bullet points of pain points, pressures, or struggles]

Only use information from the search results provided. If something is unknown, write "Unknown"."""
            },
            {
                # The USER message is the actual task + data for this specific run
                "role": "user",
                "content": f"Company to research: {company_name}\n\nSearch results:\n{raw_research}"
            }
        ],
        temperature=0.2,  # Low temperature = more factual, less creative. Good for research.
        max_tokens=600
    )

    # Extract the text from the response object
    profile = response.choices[0].message.content

    print("✅ [Researcher] Profile complete.")
    return profile
