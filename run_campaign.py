import json

from crm.crm_manager import (
    hs_upsert_contact,
    send_newsletter,
    log_campaign
)

# Mock CRM contacts — used for simulation
CONTACTS = [
    {"email": "cdirector@example.com", "persona": "creative_director"},
    {"email": "opslead@example.com", "persona": "ops_lead"},
    {"email": "freelancer@example.com", "persona": "freelancer"}
]


def run_campaign(generated, hubspot_logging=False):
    """
    Complete campaign workflow:
    1. Upsert contact (HubSpot)
    2. Send newsletter (simulated)
    3. Log locally
    4. Optional logging to HubSpot
    """

    topic = generated["topic"]
    newsletters = generated["personas"]

    results = []

    for entry in CONTACTS:
        email = entry["email"]
        persona = entry["persona"]
        newsletter = newsletters[persona]

        print(f"\n=== Running Campaign for → {email} ({persona}) ===")

        # STEP 1 — Upsert HubSpot contact
        contact_res = hs_upsert_contact(email, persona)

        # STEP 2 — Simulated send
        send_res = send_newsletter(email, persona, newsletter)

        # STEP 3 — Logging (local + optional HubSpot)
        log_res = log_campaign(
            blog_title=topic,
            persona=persona,
            subject=newsletter["subject"],
            perf=send_res,
            hubspot_logging=hubspot_logging
        )

        # Save output for dashboard
        results.append({
            "contact": contact_res,
            "sent": send_res,
            "log": log_res
        })

    print("\n🚀 CAMPAIGN EXECUTED SUCCESSFULLY")
    return results