import requests
import json
import os

API_KEY = os.getenv("HUBSPOT_API_KEY")

url = "https://api.hubapi.com/crm/v3/schemas"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

schema = {
    "name": "campaign_log",
    "labels": {
        "singular": "Campaign Log",
        "plural": "Campaign Logs"
    },
    "primaryDisplayProperty": "blog_title",
    "requiredProperties": ["blog_title"],
    "properties": [
        {"name": "blog_title", "label": "Blog Title", "type": "string", "fieldType": "text"},
        {"name": "persona", "label": "Persona", "type": "string", "fieldType": "text"},
        {"name": "subject", "label": "Subject Line", "type": "string", "fieldType": "text"},
        {"name": "open_rate", "label": "Open Rate", "type": "number", "fieldType": "number"},
        {"name": "click_rate", "label": "Click Rate", "type": "number", "fieldType": "number"},
        {"name": "unsubscribe_rate", "label": "Unsubscribe Rate", "type": "number", "fieldType": "number"},
        {"name": "sent_at", "label": "Sent At", "type": "datetime", "fieldType": "date"}
    ],
    "associations": [
        {
            "fromObjectTypeId": "contact",
            "toObjectTypeId": "campaign_log",
            "name": "campaign_log_to_contact",
            "cardinality": "ONE_TO_MANY"
        }
    ]
}

response = requests.post(url, headers=headers, data=json.dumps(schema))
print(response.status_code)
print(response.json())
