import json
import random
import uuid
from datetime import datetime

from crm.hubspot_client import (
    hs_get_contact_id,
    hs_upsert_contact,
    hs_create_campaign_log,
    hs_associate_log_to_contact
)


# ============================================================
# 1. CONTACT UPSERT (used by run_campaign)
# ============================================================
def create_or_update_contact(email, persona):
    """
    Wrapper for HubSpot contact creation + update.
    Kept for backwards compatibility.
    """
    return hs_upsert_contact(email, persona)


# ============================================================
# 2. SEND NEWSLETTER (simulated)
# ============================================================
def send_newsletter(email, persona, newsletter):
    """
    Generates simulated engagement metrics.
    """
    return {
        "email": email,
        "persona": persona,
        "subject": newsletter["subject"],
        "open_rate": round(random.uniform(0.30, 0.70), 2),
        "click_rate": round(random.uniform(0.05, 0.20), 2),
        "unsubscribe_rate": round(random.uniform(0.00, 0.05), 2),
        "campaign_id": f"cmp_{uuid.uuid4().hex[:8]}",
        "sent_at": datetime.now().isoformat()
    }


# ============================================================
# 3. LOCAL LOGGING (jsonl)
# ============================================================
def log_campaign_local(entry):
    """
    Save campaign logs locally in a .jsonl file.
    """
    with open("campaign_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


# ============================================================
# 4. HUBSPOT CAMPAIGN LOGGING
# ============================================================
def log_campaign_hubspot(perf, blog_title, persona, subject):
    """
    Push newsletter performance record → HubSpot custom object
    and associate record with contact.
    """

    properties = {
        "blog_title": blog_title,
        "persona": persona,
        "subject": subject,
        "open_rate": perf["open_rate"],
        "click_rate": perf["click_rate"],
        "unsubscribe_rate": perf["unsubscribe_rate"],
        "campaign_id": perf["campaign_id"],
        "sent_at": perf["sent_at"]
    }

    # Step 1: create custom object record
    created = hs_create_campaign_log(properties)
    log_id = created.get("id")

    # Step 2: associate with contact
    contact_id = hs_get_contact_id(perf["email"])
    if log_id and contact_id:
        hs_associate_log_to_contact(log_id, contact_id)

    return created


# ============================================================
# 5. MASTER LOG WRAPPER
# ============================================================
def log_campaign(blog_title, persona, subject, perf, hubspot_logging=False):
    """
    Central logging function:
      - Always writes local log
      - Optionally logs to HubSpot
    """

    entry = {
        "blog_title": blog_title,
        "persona": persona,
        "subject": subject,
        "open_rate": perf["open_rate"],
        "click_rate": perf["click_rate"],
        "unsubscribe_rate": perf["unsubscribe_rate"],
        "campaign_id": perf["campaign_id"],
        "sent_at": perf["sent_at"]
    }

    # always store locally
    log_campaign_local(entry)

    # optional: remote (HubSpot)
    if hubspot_logging:
        log_campaign_hubspot(
            perf=perf,
            blog_title=blog_title,
            persona=persona,
            subject=subject
        )

    return entry