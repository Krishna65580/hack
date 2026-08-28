a=1
while a<=10:
    a=a+a
print(a)
"""
Rural Health Assistant — HackSprint 2.0
Problem Statement #2: Healthcare Accessibility and Rural Health Assistant

A non-diagnostic digital healthcare assistance platform that helps users
understand general health information, locate nearby healthcare resources,
and manage basic healthcare activities (reminders). This system does NOT
diagnose or prescribe — every response is templated from a curated
knowledge base and routes serious concerns to real medical professionals.
"""

import streamlit as st
from datetime import datetime, date
from engine import build_response
from locator import search_facilities
from knowledge_base import EMERGENCY_CONTACTS, DISCLAIMER
from speech import transcribe

st.set_page_config(
    page_title="Rural Health Assistant",
    page_icon="⚕️",
    layout="wide",
)

# ---------- session state ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "records" not in st.session_state:
    st.session_state.records = []

# ---------- sidebar: emergency + navigation ----------
with st.sidebar:
    st.markdown("## ⚕️ Rural Health Assistant")
    st.caption("Non-diagnostic healthcare accessibility platform")

    st.markdown("### 🚨 Emergency Contacts")
    for name, number in EMERGENCY_CONTACTS.items():
        st.markdown(f"**{name}:** `{number}`")

    st.divider()
    page = st.radio(
        "Navigate",
        ["💬 Health Info Chat", "🏥 Find Healthcare", "⏰ Reminders", "📋 My Health Notes"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Built for HackSprint 2.0 — Dept. of CSE, AITAM")

# ---------- header disclaimer (always visible) ----------
st.info(DISCLAIMER, icon="⚕️")

# ================= PAGE 1: CHAT =================
if page == "💬 Health Info Chat":
    st.title("Health Information Assistant")
    st.caption(
        "Ask about common symptoms or health topics in your own words. "
        "Voice input available where supported by your browser/device."
    )

    if "pending_query" not in st.session_state:
        st.session_state.pending_query = ""

    def ask(text: str):
        result = build_response(text)
        st.session_state.chat_history.append({"role": "user", "text": text})
        st.session_state.chat_history.append({
            "role": "assistant",
            "text": result["text"],
            "urgent": result["urgent"],
            "lang": result["language_name"],
        })

    # Welcome message shown only before the first question is asked
    if not st.session_state.chat_history:
        st.success(
            "👋 **Welcome!** I'm here to give you general health information, "
            "help you find nearby care, and flag anything that needs urgent "
            "attention. Type a question below, or tap a topic to try it out."
        )
        st.caption("Quick topics")
        suggestions = ["Fever", "Cough and cold", "Loose motions", "Headache",
                        "Skin rash", "Feeling stressed", "Child health", "Pregnancy care"]
        cols = st.columns(4)
        for i, s in enumerate(suggestions):
            with cols[i % 4]:
                if st.button(s, use_container_width=True, key=f"sugg_{i}"):
                    ask(s)
                    st.rerun()

    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""

    col_input, col_voice = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "Type your question",
            value=st.session_state.voice_text,
            placeholder="e.g. I have had a fever and cough for two days...",
            label_visibility="collapsed",
        )
    with col_voice:
        audio = mic_recorder(
            start_prompt="🎤 Speak",
            stop_prompt="⏹ Stop",
            just_once=True,
            use_container_width=True,
            key="voice_recorder",
        )

    if audio and audio.get("bytes"):
        with st.spinner("Transcribing..."):
            text = transcribe(audio["bytes"])
        if text:
            st.session_state.voice_text = text
            st.rerun()
        else:
            st.warning("Couldn't catch that — please try again or type your question.")

    send = st.button("Ask", type="primary")

    if send and query.strip():
        ask(query)
        st.session_state.voice_text = ""
        st.rerun()

    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['text']}")
        else:
            box = st.error if msg.get("urgent") else st.success
            box(msg["text"])
        st.markdown("---")

# ================= PAGE 2: LOCATOR =================
elif page == "🏥 Find Healthcare":
    st.title("Find Nearby Healthcare")
    st.caption("Showing facilities near Tekkali, Andhra Pradesh (demo data — swap for live Places API in production)")

    search_q = st.text_input("Search by need (e.g. 'emergency', 'maternity', 'pediatric')", "")
    results = search_facilities(search_q)

    for f in results:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"### {f['name']}")
                st.markdown(f"**Type:** {f['type']}  |  **Services:** {f['services']}")
                st.markdown(f"📞 {f['phone']}")
            with c2:
                st.metric("Distance", f"{f['distance_km']} km")

# ================= PAGE 3: REMINDERS =================
elif page == "⏰ Reminders":
    st.title("Medicine & Appointment Reminders")

    with st.form("add_reminder", clear_on_submit=True):
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            r_title = st.text_input("What (medicine / appointment)")
        with c2:
            r_date = st.date_input("Date", min_value=date.today())
        with c3:
            r_time = st.time_input("Time")
        submitted = st.form_submit_button("Add Reminder", type="primary")
        if submitted and r_title.strip():
            st.session_state.reminders.append({
                "title": r_title, "date": str(r_date), "time": str(r_time),
                "added": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            st.success(f"Reminder added: {r_title} on {r_date} at {r_time}")

    st.divider()
    if not st.session_state.reminders:
        st.caption("No reminders yet.")
    else:
        sorted_reminders = sorted(st.session_state.reminders, key=lambda r: (r["date"], r["time"]))
        for i, r in enumerate(sorted_reminders):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"**{r['title']}** — {r['date']} at {r['time']}")
            with c2:
                if st.button("✕", key=f"del_{i}"):
                    st.session_state.reminders.remove(r)
                    st.rerun()

# ================= PAGE 4: HEALTH NOTES =================
elif page == "📋 My Health Notes":
    st.title("My Health Notes")
    st.caption(
        "A private, local space to jot down symptoms, visit summaries, or "
        "questions to ask your doctor. This is organizational only — not a "
        "medical record and not shared with anyone."
    )

    with st.form("add_note", clear_on_submit=True):
        note = st.text_area("New note")
        submitted = st.form_submit_button("Save Note", type="primary")
        if submitted and note.strip():
            st.session_state.records.append({
                "text": note, "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            st.success("Note saved.")

    st.divider()
    if not st.session_state.records:
        st.caption("No notes yet.")
    else:
        for i, rec in enumerate(reversed(st.session_state.records)):
            with st.container(border=True):
                st.caption(rec["date"])
                st.write(rec["text"])
