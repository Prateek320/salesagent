"""
agents/analyst.py — The Analyst Agent
────────────────────────────────────────
Job: Read the Researcher's company profile and identify:
     - The sharpest pain points to target
     - The best sales angle / hook
     - Personalization details for the outreach

PM Insight: Notice this agent gets HIGHER temperature (0.5) than the
Researcher (0.2). That's intentional — research needs accuracy,
analysis benefits from some creative thinking. Tuning temperature
is a real product decision in AI systems.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def run_analyst(company_profile: str, your_product: str) -> str:
    """
    Analyze a company profile and identify the best sales angle.

    Args:
        company_profile : The structured profile from run_researcher()
        your_product    : What you're selling e.g. "an AI-powered onboarding tool"

    Returns:
        A sales brief with pain points, hooks, and personalization notes.
    """

    print("\n🧠 [Analyst] Identifying pain points and sales angles...")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Groq's sharpest model — best for strategic reasoning
        messages=[
            {
                "role": "system",
                "content": """You are a sharp B2B sales strategist.
You read company profiles and identify exactly how to position a product to resonate with that company.

Output EXACTLY this format:

PRIMARY PAIN POINT: [The single most pressing challenge this company faces that your product solves]
SECONDARY PAIN POINT: [A supporting challenge that reinforces the case]
SALES HOOK: [One punchy sentence that frames the value proposition for THIS specific company]
PERSONALIZATION DETAIL: [A specific recent fact about the company that should be referenced in outreach to show you did your homework]
TONE RECOMMENDATION: [How the email should feel — e.g. "executive-level, data-driven" or "friendly and startup-casual"]
SUBJECT LINE IDEAS:
- [Option 1]
- [Option 2]
- [Option 3]

Be specific and tactical. No generic advice."""
            },
            {
                "role": "user",
                "content": f"""Company profile:
{company_profile}

Product being sold:
{your_product}

Produce the sales brief."""
            }
        ],
        temperature=0.5,   # Slightly higher = more creative angles, still grounded
        max_tokens=500
    )

    analysis = response.choices[0].message.content

    print("✅ [Analyst] Sales brief ready.")
    return analysis
