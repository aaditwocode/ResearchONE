import streamlit as st

from project_pipeline import run_research_pipeline

st.set_page_config(page_title="ResearchONE", page_icon="🔎", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 10% 0%, #1b2b4a 0%, #0b1220 45%, #070c16 100%);
        color: #f2f4fb;
    }

    /* ---------- Hero ---------- */
    .hero-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(20,184,166,0.14));
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 28px;
        padding: 32px 34px;
        box-shadow: 0 25px 60px rgba(0,0,0,0.35);
        backdrop-filter: blur(12px);
    }
    .hero-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.75rem;
        color: #8fe9ff;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
        background: linear-gradient(90deg, #ffffff, #b7c8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #cbd6f5;
        margin-bottom: 1.1rem;
        max-width: 640px;
    }
    .tag {
        display: inline-block;
        background: rgba(103, 232, 249, 0.14);
        color: #8fe9ff;
        border: 1px solid rgba(103,232,249,0.25);
        border-radius: 999px;
        padding: 6px 12px;
        margin: 4px 6px 0 0;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* ---------- Generic cards ---------- */
    .info-card, .report-card, .timeline-card, .pipeline-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 20px;
        margin-top: 14px;
    }
    .info-card h3, .report-card h3, .timeline-card h3, .pipeline-card h3 {
        margin-top: 0;
        color: #ffffff;
    }

    /* ---------- Agent pipeline strip ---------- */
    .agent-row {
        display: flex;
        align-items: stretch;
        gap: 6px;
        margin-top: 10px;
    }
    .agent-step {
        flex: 1;
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        padding: 16px 14px;
        position: relative;
        transition: all 0.2s ease;
    }
    .agent-step .agent-icon { font-size: 1.5rem; margin-bottom: 6px; display: block; }
    .agent-step .agent-name { font-weight: 700; color: #fff; font-size: 0.95rem; }
    .agent-step .agent-role { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; color: #8fe9ff; margin-bottom: 6px; display: block; }
    .agent-step .agent-desc { font-size: 0.8rem; color: #c3cde6; line-height: 1.35; }
    .agent-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #4d5b82;
        font-size: 1.3rem;
        padding: 0 2px;
    }

    /* ---------- Buttons ---------- */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #22c55e, #14b8a6);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        transition: all 0.15s ease;
    }
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(20,184,166,0.3);
    }

    /* ---------- Timeline (how it works) ---------- */
    .timeline-item {
        display: flex;
        gap: 10px;
        margin-bottom: 14px;
        align-items: flex-start;
    }
    .timeline-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #22c55e;
        margin-top: 6px;
        flex-shrink: 0;
        box-shadow: 0 0 0 4px rgba(34,197,94,0.15);
    }

    /* ---------- Source result cards ---------- */
    .result-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 10px;
    }
    .result-card a { color: #8fe9ff; text-decoration: none; font-size: 0.85rem; }
    .result-card span { color: #c3cde6; font-size: 0.88rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-card">
        <div class="hero-eyebrow">Multi-agent research assistant</div>
        <div class="hero-title">ResearchONE</div>
        <div class="hero-subtitle">Turn any topic into a clean, polished research brief. A small team of
        purpose-built agents searches, reads, writes, and critiques the result — so you get a sourced
        report, not just a wall of links.</div>
        <div>
            <span class="tag">🔍 Search Agent</span>
            <span class="tag">📖 Reader Agent</span>
            <span class="tag">✍️ Writer Agent</span>
            <span class="tag">🧠 Critic Agent</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pipeline-card">
        <h3>How the agent chain works</h3>
        <div class="agent-row">
            <div class="agent-step">
                <span class="agent-icon">🔍</span>
                <span class="agent-role">Stage 1</span>
                <div class="agent-name">Search Agent</div>
                <div class="agent-desc">Queries the web for your topic and returns a ranked list of
                candidate sources (title, URL, snippet).</div>
            </div>
            <div class="agent-arrow">➜</div>
            <div class="agent-step">
                <span class="agent-icon">📖</span>
                <span class="agent-role">Stage 2</span>
                <div class="agent-name">Reader Agent</div>
                <div class="agent-desc">Opens the top-ranked source and scrapes its article text so the
                report is grounded in real content, not just snippets.</div>
            </div>
            <div class="agent-arrow">➜</div>
            <div class="agent-step">
                <span class="agent-icon">✍️</span>
                <span class="agent-role">Stage 3</span>
                <div class="agent-name">Writer Agent</div>
                <div class="agent-desc">Synthesizes the search results and scraped article into a
                structured brief: intro, key findings, evidence, conclusion.</div>
            </div>
            <div class="agent-arrow">➜</div>
            <div class="agent-step">
                <span class="agent-icon">🧠</span>
                <span class="agent-role">Stage 4</span>
                <div class="agent-name">Critic Agent</div>
                <div class="agent-desc">Reviews the draft, scores it out of 10, and lists strengths and
                gaps — a quality check before you read it.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
left_col, right_col = st.columns([1.25, 0.75], gap="large")

# ----------------------------------------------------------------------------
# Left column: input + run + results
# ----------------------------------------------------------------------------
with left_col:
    st.markdown("<div class='info-card'><h3>Start your research</h3></div>", unsafe_allow_html=True)

    if "topic" not in st.session_state:
        st.session_state.topic = ""

    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic,
        placeholder="Try: AI startups, climate tech, football tactics",
        key="topic_input",
    )

    example_topics = ["Formula 1 in 2026", "AI in healthcare", "Latest climate tech trends"]
    cols = st.columns(len(example_topics))
    for col, example in zip(cols, example_topics):
        if col.button(example, use_container_width=True, key=f"topic_{example}"):
            st.session_state.topic = example
            st.rerun()

    run_clicked = st.button("Run research", use_container_width=True)

    if run_clicked:
        active_topic = topic or st.session_state.topic
        if not active_topic.strip():
            st.warning("Enter a topic first, or pick one of the examples above.")
        else:
            status = st.status("Running the agent chain...", expanded=True)

            def on_step(event, data=None):
                data = data or {}
                if event == "search_start":
                    status.write("🔍 **Search Agent** — querying the web...")
                elif event == "search_done":
                    status.write(f"✅ Search Agent found **{data.get('count', 0)}** candidate sources.")
                elif event == "read_start":
                    url = data.get("url") or "no source found"
                    status.write(f"📖 **Reader Agent** — reading top source: `{url}`")
                elif event == "read_done":
                    status.write(f"✅ Reader Agent collected **{data.get('chars', 0)}** characters of context.")
                elif event == "write_start":
                    status.write("✍️ **Writer Agent** — drafting the structured report...")
                elif event == "write_done":
                    status.write("✅ Writer Agent finished the draft.")
                elif event == "critique_start":
                    status.write("🧠 **Critic Agent** — reviewing the report...")
                elif event == "critique_done":
                    status.write("✅ Critic Agent finished scoring the report.")

            try:
                result = run_research_pipeline(active_topic, on_step=on_step)
            except TypeError as exc:
                if "unexpected keyword argument 'on_step'" in str(exc):
                    result = run_research_pipeline(active_topic)
                else:
                    raise

            try:
                status.update(label="Agent chain complete", state="complete", expanded=False)
                if result.get("error"):
                    st.warning("The workflow completed with a fallback message. See the report panel for details.")
                st.session_state.result = result
                st.session_state.topic = active_topic
            except Exception as exc:
                status.update(label="Agent chain failed", state="error", expanded=False)
                st.error(f"The research workflow hit an error: {exc}")
                st.session_state.result = {
                    "report": f"# Research Report: {active_topic}\n\n## Error\nThe workflow failed unexpectedly.\n\n**Error:** {exc}",
                    "feedback": "Score: 4/10\nStrengths:\n- The UI captured the issue clearly.\nAreas to Improve:\n- Retry the request after checking connectivity.",
                    "search_results": [],
                }
                st.session_state.topic = active_topic

    if "result" in st.session_state:
        result = st.session_state.result
        st.success("Research completed")

        report_tab, feedback_tab, sources_tab = st.tabs(["📄 Report", "🧠 Critic Feedback", "🔗 Sources"])

        with report_tab:
            st.markdown("<div class='report-card'>", unsafe_allow_html=True)
            st.markdown(result["report"])
            st.markdown("</div>", unsafe_allow_html=True)

        with feedback_tab:
            st.markdown("<div class='report-card'><h3>Review Feedback</h3></div>", unsafe_allow_html=True)
            st.text_area("Feedback", result["feedback"], height=220, label_visibility="collapsed")

        with sources_tab:
            st.markdown("<div class='report-card'><h3>Source highlights</h3></div>", unsafe_allow_html=True)
            search_results = result.get("search_results", [])
            if not search_results:
                st.info("No search results were returned for this topic.")
            for item in search_results:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <strong>{item.get('title', '')}</strong><br/>
                        <a href="{item.get('url', '')}" target="_blank">{item.get('url', '')}</a><br/>
                        <span>{item.get('snippet', '')}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

# ----------------------------------------------------------------------------
# Right column: workflow + benefits
# ----------------------------------------------------------------------------
with right_col:
    st.markdown(
        """
        <div class="timeline-card">
            <h3>What happens when you click "Run research"</h3>
            <div class="timeline-item"><div class="timeline-dot"></div><div><strong>1. Enter your topic</strong><br/>Choose anything you want to understand better.</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div><strong>2. Search Agent gathers evidence</strong><br/>Searches the web and collects a ranked list of sources.</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div><strong>3. Reader Agent reads the top source</strong><br/>Scrapes the best-matching page for real article content.</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div><strong>4. Writer Agent builds a report</strong><br/>Organizes findings into a readable, structured brief.</div></div>
            <div class="timeline-item"><div class="timeline-dot"></div><div><strong>5. Critic Agent reviews it</strong><br/>Scores the draft and lists strengths and gaps.</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="timeline-card">
            <h3>Why users like it</h3>
            <ul>
                <li>Fast and simple for research tasks</li>
                <li>Readable report layout, not raw text</li>
                <li>Transparent — you see every agent's step live</li>
                <li>Good for studying a topic quickly</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )