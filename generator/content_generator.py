import json
import os
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =====================================================
# PERSONA DEFINITIONS
# =====================================================
PERSONAS = {
    "creative_director": {
        "pain_points": "Repetitive design tasks, slow revision cycles, not enough time for creative direction.",
        "goals": "More time for ideas, smoother workflows, faster reviews."
    },
    "ops_lead": {
        "pain_points": "Inefficient workflows, inconsistency, bottlenecks in delivery.",
        "goals": "Predictable operations, scalable processes, automation."
    },
    "freelancer": {
        "pain_points": "Balancing admin work with creative work, long turnaround times.",
        "goals": "Save time, simple workflow, keep clients happy."
    }
}


# =====================================================
# GPT HELPER
# =====================================================
def ai(prompt):
    """Return clean GPT output with zero markdown/backticks."""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Return plain text only. "
                    "Do NOT include backticks, no markdown fences, "
                    "no code blocks, no commentary unless asked."
                )
            },
            {"role": "user", "content": prompt},
        ]
    )
    return res.choices[0].message.content.strip()


# =====================================================
# GENERATE BLOG + NEWSLETTERS
# =====================================================
def generate_content(topic):

    # 1 — Create outline
    outline = ai(
        f"""
Create a clean, structured outline for a blog titled '{topic}'.
Use sections and bullets. Do NOT use markdown code blocks or backticks.
Return plain text only.
        """
    )

    # 2 — Blog draft
    draft = ai(
        f"""
Write a complete and well-structured 400–600 word blog using this outline.

Topic: {topic}

Outline:
{outline}

Return plain flowing text. No markdown, no backticks, no JSON.
        """
    )

    # 3 — Persona newsletters
    newsletters = {}
    for persona, meta in PERSONAS.items():

        prompt = f"""
Convert this blog into a 130–180 word email-style newsletter
targeted for persona '{persona}'.

Blog text:
{draft}

Persona pain points: {meta['pain_points']}
Persona goals: {meta['goals']}

You MUST return valid JSON only:

{{
  "subject": "string",
  "body": "string"
}}
        """

        raw = ai(prompt)

        try:
            newsletters[persona] = json.loads(raw)
        except:
            newsletters[persona] = {
                "subject": f"{topic} — Newsletter",
                "body": raw.strip()
            }

    # 4 — Save everything
    result = {
        "topic": topic,
        "blog": {
            "outline": outline,
            "draft": draft
        },
        "personas": newsletters,
        "generated_at": datetime.now().isoformat()
    }

    os.makedirs("content", exist_ok=True)
    with open("content/generated_content.json", "w") as f:
        json.dump(result, f, indent=2)

    return result


# =====================================================
# REVISION MODE
# =====================================================
def revise_newsletter(persona, original_body, request):
    """Return a revised newsletter body only — plain text."""

    prompt = f"""
Revise the following newsletter for persona '{persona}'.
User request: {request}

Newsletter body:
{original_body}

Return ONLY the revised newsletter body.
Plain text only. No JSON. No backticks.
    """

    revised = ai(prompt)
    return revised.strip()