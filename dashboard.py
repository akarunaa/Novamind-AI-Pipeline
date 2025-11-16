import streamlit as st
import textstat
from generator.content_generator import generate_content, revise_newsletter
from run_campaign import run_campaign
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# THEME
# -------------------------
custom_css = """
<style>
:root {
    --bg: #f6f3ff;
    --section: #ffffff;
    --purple: #6c4bc1;
    --purple-light: #9273e0;
    --text: #1d1c22;
    --border: #e7defa;
}

.section {
    background: var(--section);
    padding: 28px;
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-top: 25px;
}

h1, h2, h3 {
    color: var(--purple);
    font-weight: 600;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)



# -------------------------
# STATE
# -------------------------
if "generated" not in st.session_state:
    st.session_state.generated = None

if "campaign_results" not in st.session_state:
    st.session_state.campaign_results = None



# -------------------------
# TITLE
# -------------------------
st.title("AI Content Generator + CRM Campaign Pipeline")
st.markdown(
    "<p style='color:#6c4bc1; font-size:16px; margin-top:-15px;'>by Aksha Karunaagaran</p>",
    unsafe_allow_html=True
)


# ============================================================================
# 1 — GENERATE CONTENT
# ============================================================================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.header("1. Generate Blog + Persona Newsletters")

topic = st.text_input("Blog topic", "AI in Creative Automation")

if st.button("Generate Content Now"):
    with st.spinner("Generating content…"):
        st.session_state.generated = generate_content(topic)
    st.success("Content generated!")

st.markdown('</div>', unsafe_allow_html=True)



# ============================================================================
# 2 — BLOG PREVIEW
# ============================================================================
if st.session_state.generated:

    blog = st.session_state.generated["blog"]

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("2. Blog Preview")

    st.subheader("Blog Outline")
    st.write(blog["outline"])

    st.subheader("Full Draft")
    st.write(blog["draft"])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Reading Grade", f"{textstat.flesch_kincaid_grade(blog['draft']):.1f}")
    with c2:
        st.metric("Reading Ease", f"{textstat.flesch_reading_ease(blog['draft']):.1f}")

    st.markdown('</div>', unsafe_allow_html=True)



# ============================================================================
# 3 — PERSONA NEWSLETTERS + REVISION
# ============================================================================
if st.session_state.generated:

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("3. Persona Newsletters")

    personas = st.session_state.generated["personas"]

    selected = st.selectbox("Persona", list(personas.keys()))
    newsletter = personas[selected]

    st.subheader("Subject")
    new_subj = st.text_input("Subject", newsletter["subject"])

    st.subheader("Body")
    new_body = st.text_area("Body", newsletter["body"], height=250)

    rev_prompt = st.text_area("Revision Instructions",
                              "Make tone clearer and more engaging.")

    if st.button("Apply Revision"):
        with st.spinner("Revising…"):
            revised = revise_newsletter(selected, new_body, rev_prompt)
            st.session_state.generated["personas"][selected]["body"] = revised

        st.success("Revision applied!")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)



# ============================================================================
# 4 — SEND CAMPAIGN
# ============================================================================
if st.session_state.generated:

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("4. Run CRM Campaign")

    if st.button("Send Campaign to CRM"):
        with st.spinner("Running…"):
            results = run_campaign(st.session_state.generated, hubspot_logging=True)

        st.success("Campaign sent!")

        st.subheader("Engagement Summary")

        st.session_state.campaign_results = results

        for r in results:
            persona = r["sent"]["persona"].replace("_", " ").title()

            st.markdown(f"### {persona}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Open Rate", f"{r['sent']['open_rate']*100:.0f}%")
            with col2:
                st.metric("Click Rate", f"{r['sent']['click_rate']*100:.0f}%")
            with col3:
                st.metric("Unsub Rate", f"{r['sent']['unsubscribe_rate']*100:.0f}%")

    st.markdown('</div>', unsafe_allow_html=True)



# ============================================================================
# 5 — AI CONTENT OPTIMIZER (NEW)
# ============================================================================
if st.session_state.campaign_results:

    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.header("5. AI Content Optimizer")

    # Generate improvement suggestions
    def ai_optimize(results, blog_topic):
        prompt = f"""
You are an AI content strategist.

Here are newsletter engagement metrics for a blog campaign about "{blog_topic}":

{results}

Provide:
1. 3 improved subject lines
2. 3 next blog topic ideas
3. 3 ways to improve newsletter copywriting
4. Persona-specific suggestions (creative director, ops lead, freelancer)

Return plain text. No lists inside lists.
"""
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content

    if st.button("Generate Optimization Insights"):
        with st.spinner("Optimizing content…"):
            blog_topic = st.session_state.generated["topic"]
            insights = ai_optimize(st.session_state.campaign_results, blog_topic)
        st.subheader("Optimization Report")
        st.write(insights)

    st.markdown('</div>', unsafe_allow_html=True)