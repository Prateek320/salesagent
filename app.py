"""
app.py — Flask Web Server
──────────────────────────
This turns our terminal pipeline into a browser-based app.

Key concept: Server-Sent Events (SSE)
Instead of waiting for ALL agents to finish then showing results,
SSE lets us push updates to the browser in real time — so the user
sees each agent fire live. Much more impressive to demo.

To run:
  python app.py
Then open: http://localhost:5000
"""

import json
import queue
import threading
import os
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv

# Import our agents (same ones we built — nothing changes)
from agents.researcher import run_researcher
from agents.analyst    import run_analyst
from agents.writer     import run_writer

load_dotenv()

app = Flask(__name__)


# ── SSE helper ─────────────────────────────────────────────────────────
# SSE (Server-Sent Events) works like this:
# - The browser opens a long-lived HTTP connection
# - The server pushes "events" down that connection whenever it wants
# - The browser's JavaScript listens and updates the UI instantly
# No page refresh needed. No websockets needed. Just HTTP.

def sse_message(event: str, data: dict) -> str:
    """Format a message in SSE protocol format."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# ── Routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main page."""
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_pipeline():
    """
    Receive form data and stream agent updates back via SSE.

    This is the core endpoint. It:
    1. Gets the user's inputs from the form
    2. Runs all 3 agents in sequence
    3. Streams progress events to the browser after each agent completes
    """
    company_name  = request.form.get("company_name", "").strip()
    your_product  = request.form.get("your_product", "").strip()
    sender_name   = request.form.get("sender_name", "").strip()
    sender_role   = request.form.get("sender_role", "").strip()

    if not company_name or not your_product:
        return {"error": "Company name and product are required"}, 400

    def generate():
        """
        Generator function — yields SSE messages as each agent finishes.
        We run this in the main thread (Flask handles streaming for us).
        """
        try:
            # ── Agent 1: Researcher ────────────────────────────────────
            yield sse_message("agent_start", {
                "agent": "researcher",
                "message": f"Searching the web for info on {company_name}..."
            })

            profile = run_researcher(company_name)

            yield sse_message("agent_done", {
                "agent": "researcher",
                "output": profile
            })

            # ── Agent 2: Analyst ───────────────────────────────────────
            yield sse_message("agent_start", {
                "agent": "analyst",
                "message": "Identifying pain points and sales angles..."
            })

            analysis = run_analyst(profile, your_product)

            yield sse_message("agent_done", {
                "agent": "analyst",
                "output": analysis
            })

            # ── Agent 3: Writer ────────────────────────────────────────
            yield sse_message("agent_start", {
                "agent": "writer",
                "message": "Drafting personalized outreach email..."
            })

            email = run_writer(
                company_profile=profile,
                sales_analysis=analysis,
                sender_name=sender_name,
                sender_role=sender_role,
                your_product=your_product
            )

            yield sse_message("agent_done", {
                "agent": "writer",
                "output": email
            })

            # ── Pipeline complete ──────────────────────────────────────
            yield sse_message("complete", {
                "email": email,
                "profile": profile,
                "analysis": analysis
            })

        except Exception as e:
            yield sse_message("error", {"message": str(e)})

    # stream_with_context keeps the Flask request context alive
    # while we stream — required for SSE to work correctly
    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"   # Prevents nginx from buffering SSE
        }
    )


if __name__ == "__main__":
    # debug=True auto-reloads when you save changes — great for development
    # threaded=True allows multiple requests at once
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, threaded=True, host="0.0.0.0", port=port)
