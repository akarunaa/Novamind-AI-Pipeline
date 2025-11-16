from datetime import datetime
import random

def create_campaign_record(campaign_name):
    """Simulate creation of a HubSpot campaign record."""
    print(f"[CRM] Creating campaign → {campaign_name}")

    return {
        "id": f"campaign_{random.randint(10000,99999)}",
        "name": campaign_name,
        "created_at": datetime.now().isoformat()
    }
