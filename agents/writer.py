"""
agents/writer.py — The Writer Agent
──────────────────────────────────────
Job: Take the company profile + sales analysis and write a sharp,
     personalized cold outreach email that doesn't read like a template.

PM Insight: The system prompt here is the most detailed of the three.
That's intentional — writing quality is the hardest to constrain with AI.
Good negative instructions ("never write X") are as valuable as positive ones.
This is a key skill in AI product design.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def run_writer(
    company_profile: str,
    sales_analysis: str,
    sender_name: str,
    sender_role: str,
    your_product: str
) -> str:
    """
    Write a personalized outreach email using the research + analysis.

    Args:
        company_profile : Structured profile from Researcher
        sales_analysis  : Pain points + angles from Analyst
        sender_name     : Your name  e.g. "Prateek Bhoge"
        sender_role     : Your role  e.g. "Product Manager at XYZ"
        your_product    : What you're selling

    Returns:
        A complete, ready-to-send outreach email (subject + body).
    """

    print("\n✍️  [Writer] Drafting personalized outreach email...")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Groq's best model — great for nuanced writing
        messages=[
            {
                "role": "system",
                "content": """You are an expert B2B copywriter who specializes in cold outreach.
You write emails that get replies — because they feel personal, relevant, and brief.

Rules you NEVER break:
- Email body: 100-130 words maximum. Shorter is always better.
- Never start with "I hope this email finds you well" or any generic opener.
- Never list features. Focus only on outcomes and their specific situation.
- Always reference one specific, real detail about the company to prove you researched them.
- End with a single, low-friction CTA (e.g., "Worth a 20-min call?")
- Tone must match the "TONE RECOMMENDATION" from the sales analysis.
- No exclamation marks. No buzzwords like "synergy", "leverage", "unlock".

Output format:
SUBJECT: [subject line]

[email body]"""
            },
            {
                "role": "user",
                "content": f"""Write an outreach email using the information below.

--- COMPANY PROFILE ---
{company_profile}

--- SALES ANALYSIS ---
{sales_analysis}

--- SENDER INFO ---
Name: {sender_name}
Role: {sender_role}
Product: {your_product}"""
            }
        ],
        temperature=0.7,   # Higher = more natural, human-sounding writing
        max_tokens=400
    )

    email = response.choices[0].message.content

    print("✅ [Writer] Email drafted.")
    return email
