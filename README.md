# NovaMind AI Content Pipeline  
Built with care by **Aksha Karunaagaran** 💜
#### Acccess here: https://novamindaipipeline.streamlit.app

## Overview  
NovaMind is an AI-powered marketing content pipeline that lets you generate a blog, convert it into persona-specific newsletters, revise content live, and run a simulated CRM campaign on HubSpot all inside one clean Streamlit app.

The whole flow mirrors how real AI-driven marketing teams work:  
**Generate → Personalize → Send → Analyze → Optimize.**

---

## Features  

### AI Blog Generator  
- Auto-creates a structured outline  
- Produces a clean 400–600 word blog draft  
- No markdown fences or messy formatting  

### Persona Newsletters  
Each persona gets a unique angle based on their needs:  
- **Creative Director**  
- **Operations Lead**  
- **Freelancer**  

Content aligns with pain points and goals for each user type.

### Revision Engine  
- Add a natural-language instruction  
- GPT rewrites the newsletter instantly  
- Updated text feeds back into the pipeline  

### Campaign Runner  
- Creates or updates CRM contacts  
- Simulates newsletter send with engagement metrics  
- Logs all results locally  
- Supports optional HubSpot custom-object logging  

### Optimization Layer  
After the send, the system recommends:  
- Stronger subject lines  
- High-performing future blog topics  
- Content strategy adjustments  

---

## Tech Stack  
- **Python + Streamlit**  
- **OpenAI API (gpt-4o-mini)**  
- **HubSpot CRM API (optional)**  
- **textstat** for readability feedback  
- **JSONL** for lightweight local logging  

---

## Assumptions  
- Email sending is simulated (focus is on content + workflow).  
- HubSpot integration is included, but optional for review.  
- Contacts are mock personas used for demonstration.  
- The reviewer can run the entire app through Streamlit Cloud using secure secrets.  
- GPT responses are kept plain-text to ensure clean display.  

---

## Architecture Diagram
flowchart TD

    A[User Opens Streamlit App] --> B[Enter Blog Topic]
    B --> C[OpenAI API - Generate Outline & Blog]
    C --> D[OpenAI API - Generate Persona Newsletters]

    D --> E[Streamlit UI - Persona Review & Revision]
    E --> F[OpenAI API - Revision Mode]

    F --> G[Run Campaign]
    G --> H[Simulated Newsletter Send]

    H --> I[Local Logging (JSONL)]

    H --> J{HubSpot Logging Enabled?}
    J -->|Yes| K[HubSpot API - Upsert Contact]
    K --> L[HubSpot API - Create Campaign Log Entry]
    L --> M[HubSpot API - Associate Log → Contact]
    J -->|No| N[Skip HubSpot Logging]


## How to Run  

### Streamlit Cloud (Recommended)  
Just open the hosted link. https://novamindaipipeline.streamlit.app
All keys are stored in Streamlit Secrets, so everything works instantly.

## Next Steps
Replace simulated sends with a real provider (SendGrid or HubSpot Marketing Email API).

### Auto-Recurring Weekly Pipelines
Enable scheduled weekly runs that automatically:
- generate a topic
- write a blog
- create newsletters
- run the campaign
- log results


