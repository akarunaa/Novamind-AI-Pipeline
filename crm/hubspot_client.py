import os
import requests

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE = "https://api.hubapi.com"

HEADERS = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------------------------------------
# CONFIG — YOUR CUSTOM OBJECT + ASSOCIATION TYPE
# ------------------------------------------------
CUSTOM_OBJECT = "p342697823_campaign_logs"   # Your custom object API name
ASSOCIATION_TYPE_ID = 279                    # Generic “related to” association
CONTACT_OBJECT = "contacts"


# =================================================
# 1. UPSERT CONTACT (CORRECTED)
# =================================================
def hs_upsert_contact(email, persona):
    """
    Create or update a HubSpot contact.
    Contacts live under the contacts object, NOT your custom object.
    """

    url = f"{BASE}/crm/v3/objects/contacts"

    payload = {
        "properties": {
            "email": email,

            # IMPORTANT:
            # CHANGE THIS to your actual HubSpot contact property API name.
            # Example: "persona", "persona_segment", "project_persona"
            "persona": persona
        }
    }

    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


# =================================================
# 2. FIND CONTACT ID BY EMAIL
# =================================================
def hs_get_contact_id(email):
    url = f"{BASE}/crm/v3/objects/contacts/search"

    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": email
            }]
        }]
    }

    r = requests.post(url, headers=HEADERS, json=payload)
    res = r.json()

    if res.get("results"):
        return res["results"][0]["id"]

    return None


# =================================================
# 3. CREATE CAMPAIGN LOG RECORD (CUSTOM OBJECT)
# =================================================
def hs_create_campaign_log(properties):
    url = f"{BASE}/crm/v3/objects/{CUSTOM_OBJECT}"

    payload = {
        "properties": properties
    }

    r = requests.post(url, headers=HEADERS, json=payload)
    return r.json()


# =================================================
# 4. ASSOCIATE CAMPAIGN LOG → CONTACT
# =================================================
def hs_associate_log_to_contact(log_id, contact_id):

    url = (
        f"{BASE}/crm/v4/objects/{CUSTOM_OBJECT}/"
        f"{log_id}/associations/contacts/{contact_id}"
    )

    payload = {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": ASSOCIATION_TYPE_ID
    }

    r = requests.put(url, headers=HEADERS, json=payload)
    return r.json()