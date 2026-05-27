"""
main.py — The Orchestrator
────────────────────────────
This is the conductor. It doesn't do the work itself —
it coordinates who does what, in what order, and passes
outputs between agents.

This is the core of "agent orchestration":
  Input → [Researcher] → [Analyst] → [Writer] → Output

To run:
  python main.py

Make sure you've:
  1. Created a .env file (copy from .env.example)
  2. Added your OPENAI_API_KEY and TAVILY_API_KEY
  3. Installed dependencies:  pip install -r requirements.txt
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Import our three agents — each is a module we built
from agents.researcher import run_researcher
from agents.analyst    import run_analyst
from agents.writer     import run_writer

load_dotenv()


# ── Guard: make sure API keys exist before we start ────────────────────
# It's good engineering to fail fast with a clear message,
# rather than getting a confusing error deep inside the pipeline.
def check_env():
    missing = []
    if not os.getenv("GROQ_API_KEY"):    missing.append("GROQ_API_KEY")
    if not os.getenv("TAVILY_API_KEY"):  missing.append("TAVILY_API_KEY")
    if missing:
        print(f"\n❌ Missing API keys in your .env file: {', '.join(missing)}")
        print("   Copy .env.example → .env and fill in your keys.")
        sys.exit(1)


def save_output(content: str, company: str):
    """Save the final email to a timestamped text file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"output_{company.lower().replace(' ', '_')}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(content)

    print(f"\n💾 Output saved to: {filename}")


def run_pipeline(company_name: str, your_product: str, sender_name: str, sender_role: str):
    """
    The main pipeline — runs all 3 agents in sequence.

    This function is the "orchestration logic":
    - It decides the ORDER agents run in
    - It passes each agent's OUTPUT as the next agent's INPUT
    - It handles the overall flow and final output

    Args:
        company_name  : Target company to research e.g. "Notion"
        your_product  : What you're pitching  e.g. "an AI onboarding tool for SaaS"
        sender_name   : Your name
        sender_role   : Your title / role
    """

    print("\n" + "═" * 55)
    print(f"  🚀  Sales Intelligence Pipeline")
    print(f"  Target: {company_name}")
    print("═" * 55)

    # ── STEP 1: Researcher ──────────────────────────────────────────────
    # Researcher searches the web and returns a structured company profile.
    # We store this in `company_profile` — it becomes Analyst's input.
    company_profile = run_researcher(company_name)

    # ── STEP 2: Analyst ─────────────────────────────────────────────────
    # Analyst reads the profile and identifies the best sales angles.
    # Notice: we pass company_profile directly into this function.
    # This is "output chaining" — each agent builds on the last.
    sales_analysis = run_analyst(company_profile, your_product)

    # ── STEP 3: Writer ──────────────────────────────────────────────────
    # Writer gets BOTH the profile AND the analysis — the richest context.
    # Its job is purely to turn that into a compelling email.
    email = run_writer(
        company_profile=company_profile,
        sales_analysis=sales_analysis,
        sender_name=sender_name,
        sender_role=sender_role,
        your_product=your_product
    )

    # ── FINAL OUTPUT ────────────────────────────────────────────────────
    print("\n" + "═" * 55)
    print("  📬  FINAL OUTREACH EMAIL")
    print("═" * 55)
    print(email)
    print("═" * 55)

    # Optionally show the intermediate steps (useful for learning/debugging)
    show_steps = input("\nShow intermediate steps (research + analysis)? [y/N]: ").strip().lower()
    if show_steps == "y":
        print("\n── RESEARCHER OUTPUT ──────────────────────────────────")
        print(company_profile)
        print("\n── ANALYST OUTPUT ─────────────────────────────────────")
        print(sales_analysis)

    # Save to file
    full_output = f"""SALES INTELLIGENCE PIPELINE OUTPUT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Target Company: {company_name}
{'═' * 50}

COMPANY PROFILE (Researcher Agent)
{company_profile}

SALES ANALYSIS (Analyst Agent)
{sales_analysis}

FINAL EMAIL (Writer Agent)
{email}
"""
    save_output(full_output, company_name)


# ── Entry point ─────────────────────────────────────────────────────────
# This block only runs when you execute "python main.py" directly.
# It won't run if another file imports from main.py.
if __name__ == "__main__":
    check_env()

    print("\n🤖 Sales Intelligence Agent")
    print("─" * 35)

    # Collect inputs from the user interactively
    company_name  = input("Company to research: ").strip()
    your_product  = input("What are you selling? (e.g. 'an AI onboarding tool for SaaS'): ").strip()
    sender_name   = input("Your name: ").strip()
    sender_role   = input("Your role: ").strip()

    if not company_name or not your_product:
        print("❌ Company name and product description are required.")
        sys.exit(1)

    run_pipeline(company_name, your_product, sender_name, sender_role)
