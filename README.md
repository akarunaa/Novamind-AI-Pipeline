AI-Powered Marketing Content Pipeline

This project is something I built to show how an end-to-end marketing workflow can be automated with AI — from generating content to delivering it, logging performance, and learning from the results. The goal was to make something that feels like a real internal tool: fast, simple to use, and actually helpful.

Everything runs in Streamlit, so the reviewer can open the link and test the whole flow without installing anything.

⸻

How to Use the App
	1.	Open the Streamlit link.
	2.	Pick a topic.
	3.	Generate a full blog + tailored persona newsletters.
	4.	Review or revise the content.
	5.	Run a simulated CRM campaign and see performance metrics update in real time.
	6.	View optimization suggestions (AI-powered).

I designed it so the entire workflow can be tested in under a minute.

⸻

What the System Does

1. Blog Generation

The app takes a topic and builds:
	•	a clean outline
	•	a 400–600 word blog draft
	•	readability metrics
I wanted the content to feel structured and easy to evaluate, not just “AI rambling.”

2. Persona-Based Newsletters

Each newsletter is adjusted based on persona pain points and goals:
	•	Creative Director
	•	Ops Lead
	•	Freelancer

They all stay consistent with the blog topic.

3. Revision Mode

You can tell the AI: “shorter,” “more formal,” “more energetic,” etc.
It rewrites instantly — like a mini editorial assistant.

4. CRM-Style Campaign Simulation

Running a campaign performs:
	•	contact upsert
	•	a simulated “send”
	•	generation of open/click/unsubscribe rates
	•	local logging
	•	optional HubSpot custom object logging (if API key is added)

I kept the CRM part realistic but not overly complex.

5. Optimization Suggestions

After a campaign, the system recommends:
	•	what topic to write about next
	•	stronger email subject lines
	•	which persona is performing best
	•	how to adjust tone or structure

This gives the assignment a “continuous improvement” cycle instead of a one-off output.

6. Architecture Overview
Streamlit Frontend
        │
        ▼
Content Generator (OpenAI)
        │
        ▼
Persona Newsletters
        │
        ▼
CRM Campaign Engine
   • contact mgmt
   • simulated email send
   • engagement metrics
   • logs (local + optional HubSpot)
        │
        ▼
AI Optimization Insights

I tried to keep the architecture clean so it's easy to understand and test.
7. Tools & APIs
    •    Streamlit for the interface
    •    OpenAI GPT-4o-mini for all content generation
    •    HubSpot API (optional) for logging and associations
    •    Python (requests, json, uuid, textstat)


8. Assumptions I Made
    •    CRM sending is simulated (no real emails are sent).
    •    HubSpot is optional — if a key isn’t provided, the pipeline still orks normally.
    •    Contacts are mock examples (cdirector@example.com, etc.).
    •    Metrics are probabilistic to reflect realistic campaign behavior.
    •    The UI is designed to be simple, accessible, and easy to test.

9. Why I Built It This Way

I wanted to show a few things clearly:
    •    I can design complete systems, not just isolated scripts.
    •    I understand how real marketing pipelines work (content → persona targeting → delivery → logs → learning).
    •    I can connect AI models with external APIs + UX in a way that feels like a real internal tool.
    •    Most importantly: I wanted the reviewer to be able to open it and immediately use it.

If you want, I can also make:

10. Why I Built It This Way

I wanted to show a few things clearly:
    •    I can design complete systems, not just isolated scripts.
    •    I understand how real marketing pipelines work (content → persona targeting → delivery → logs → learning).
    •    I can connect AI models with external APIs + UX in a way that feels like a real internal tool.
    •    Most importantly: I wanted the reviewer to be able to open it and immediately use it.

If you want, I can also make: