# =============================================================================
# pages/7_💬_AI_Assistant.py
# =============================================================================
import streamlit as st
from utils.constants import APP_CSS
from utils.assistant import generate_bot_reply

st.set_page_config(page_title="AI Assistant", page_icon="💬", layout="wide")
st.markdown(APP_CSS, unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

pred_data = st.session_state.last_prediction

# ── Header ────────────────────────────────────────────────────────────────────
st.title("💬 Social Media Impact Assistant")
st.markdown("Ask me anything about your prediction — in **English or Hindi**.")
st.caption("⚠️ Educational and digital-wellbeing information only. Not a medical diagnosis.")
st.divider()

# ── Prediction context banner ─────────────────────────────────────────────────
if pred_data:
    emoji = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(
        pred_data["label"], "🔵")
    st.info(f"{emoji} **Prediction in context: {pred_data['label']}** — from your last submission on the Prediction page.")
else:
    st.warning("⚠️ No prediction yet. Go to **🔮 Prediction**, fill in your details, and run a prediction first.")

# ── Welcome message (injected once) ──────────────────────────────────────────
if not st.session_state.chat_history:
    if pred_data:
        emoji = {"Beneficial": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(
            pred_data["label"], "🔵")
        welcome = (
            f"Hi! 👋 I've loaded your prediction: {emoji} **{pred_data['label']}**.\n\n"
            "You can ask me:\n"
            "• Why did I get this result?\n"
            "• What should I improve?\n"
            "• What if I reduce my social media usage?\n"
            "• Sleep tips · Study focus tips · Mood tips\n"
            "• Or ask in Hindi — main Hindi mein bhi samjha sakta hoon! 🙂\n\n"
            "⚠️ *Model-based educational prediction — not a medical diagnosis.*"
        )
    else:
        welcome = (
            "Hi! 👋 I'm your **Social Media Impact Assistant**.\n\n"
            "Please go to **🔮 Prediction** first, fill in your details, and run a prediction. "
            "I'll then give you personalised explanations and suggestions in English or Hindi!"
        )
    st.session_state.chat_history.append({"role": "bot", "text": welcome})

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="chat-wrapper"><div class="chat-user">{msg["text"]}</div></div>',
            unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["text"])

# ── Quick-action chips ────────────────────────────────────────────────────────
st.markdown("**Quick questions:**")
cols = st.columns(6)
chips = [
    ("Why this result?",      "Why did I get this result?"),
    ("What to improve?",      "What should I improve?"),
    ("Reduce usage scenario", "What if I reduce my social media usage?"),
    ("मेरा रिजल्ट समझाओ",      "मेरा रिजल्ट समझाओ"),
    ("Sleep tips",            "How can I sleep better?"),
    ("Study focus tips",      "How to focus on studies?"),
]
for idx, (label, prompt) in enumerate(chips):
    if cols[idx].button(label, key=f"chip_{idx}", use_container_width=True):
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        reply = generate_bot_reply(
            prompt,
            pred_data["label"] if pred_data else "",
            pred_data["input_dict"] if pred_data else {},
            predicted=bool(pred_data),
        )
        st.session_state.chat_history.append({"role": "bot", "text": reply})
        st.rerun()

st.divider()

# ── Text input ────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your message",
        placeholder="Ask anything… (English or Hindi)",
        label_visibility="collapsed",
    )
    send = st.form_submit_button("Send ➤")

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "text": user_input.strip()})
    reply = generate_bot_reply(
        user_input.strip(),
        pred_data["label"] if pred_data else "",
        pred_data["input_dict"] if pred_data else {},
        predicted=bool(pred_data),
    )
    st.session_state.chat_history.append({"role": "bot", "text": reply})
    st.rerun()

# ── Clear button ──────────────────────────────────────────────────────────────
if st.button("🗑️ Clear chat history", key="clear_chat"):
    st.session_state.chat_history = []
    st.rerun()
