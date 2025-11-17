import streamlit as st
from core.offer_letter_flow import show_offer_letter_flow
from purchase_agreement.section1_offer import render_section_1_offer


# ==========================================================
# 🚀 STREAMLIT APP CONFIG
# ==========================================================
st.set_page_config(
    page_title="Enchanted AI Realtor — with Human Expertise",
    page_icon="🏡",
    layout="wide",
)

# ==========================================================
# 🧠 SESSION STATE SETUP
# ==========================================================
if "current_mode" not in st.session_state:
    st.session_state.current_mode = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# Offer letter state (used inside the Offer Letter tab)
if "offer_step" not in st.session_state:
    st.session_state.offer_step = 0

if "offer_last_prompted_step" not in st.session_state:
    st.session_state.offer_last_prompted_step = -1

if "offer_data" not in st.session_state:
    st.session_state.offer_data = {}

if "offer_messages" not in st.session_state:
    st.session_state.offer_messages = []


def reset_offer_state():
    st.session_state.offer_step = 0
    st.session_state.offer_last_prompted_step = -1
    st.session_state.offer_data = {}
    st.session_state.offer_messages = []


# ==========================================================
# ⚠️ GLOBAL DISCLAIMER TEXT
# ==========================================================
DISCLAIMER_SHORT = """
> **Note (not part of the offer letter or agreement):** This tool does not provide legal advice or brokerage services. \
> Please review all terms carefully and consult a licensed real estate professional before using this in a real transaction.
"""


# ==========================================================
# 🎛️ SIDEBAR
# ==========================================================
with st.sidebar:
    st.title("Menu")

    if not st.session_state.is_logged_in:
        st.write("You’re using the free version.")
        if st.button("Log in"):
            st.info("Login screen coming soon.")
        if st.button("Sign up"):
            st.info("Sign-up screen coming soon.")
    else:
        st.subheader("Saved Requests")
        st.write("🔒 Coming soon")

        st.markdown("---")
        st.subheader("Profile")
        st.write("Your home-buying profile (coming soon)")

        st.markdown("---")
        st.subheader("Settings")
        st.write("Password, email, etc. (coming soon)")


# ==========================================================
# 🏡 HEADER — BRAND
# ==========================================================
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 1.5rem;">
        <h1 style="margin-bottom: 0;">Enchanted AI Realtor — with Human Expertise</h1>
        <p style="margin-top: 0.3rem; font-size: 1.05rem; color: gray;">
            only pay for what you need
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================================
# 🧭 ACTION BUTTONS
# ==========================================================
st.markdown("### What do you want help with today?")

col1, col2, col3 = st.columns(3)
col4, col5, _ = st.columns(3)

with col1:
    # 🔹 Combined entry: purchase agreement + offer letter
    if st.button("Purchase Agreement (Offer Letter)", use_container_width=True):
        st.session_state.current_mode = "purchase_agreement"
        reset_offer_state()
        st.session_state.messages = []

with col2:
    if st.button("Should I Buy This Property?", use_container_width=True):
        st.session_state.current_mode = "eval_property"
        st.session_state.messages = []

with col3:
    # (free slot for future feature)
    pass

with col4:
    if st.button("I’m New — Teach Me", use_container_width=True):
        st.session_state.current_mode = "education"
        st.session_state.messages = []

with col5:
    if st.button("Ask Something Else", use_container_width=True):
        st.session_state.current_mode = "free_chat"
        st.session_state.messages = []

st.markdown("---")


# ==========================================================
# 💬 GENERIC CHAT (for non-offer flows)
# ==========================================================
def show_generic_chat():
    # show history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # new message
    user_input = st.chat_input("Type your message…")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # placeholder AI response for now
        ai_response = "Thanks! I’ll help you shortly. (AI logic coming later)"
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.write(ai_response)


# ==========================================================
# 🧩 MODE ROUTER — Which flow to show?
# ==========================================================
mode = st.session_state.current_mode

if mode is None:
    st.info("Select one of the options above to begin.")

elif mode == "purchase_agreement":
    st.subheader("Purchase Agreement – CA RPA Walkthrough (Beta)")

    st.markdown(
        "We’ll guide you through a **California Residential Purchase Agreement (RPA)** "
        "and also help you draft a clear **Offer Letter** based on the same terms."
    )

    # 🔹 Two tabs: Agreement walkthrough + Offer Letter
    tab1, tab2 = st.tabs(
        ["Purchase Agreement – Section 1", "Offer Letter Draft"]
    )

    with tab1:
        render_section_1_offer()

    with tab2:
        st.markdown("### Offer Letter Draft")
        show_offer_letter_flow()

        # Disclaimer + paid review CTA
        st.markdown(DISCLAIMER_SHORT)
        if st.button("Request Professional Review – $75", key="offer_review_btn"):
            st.info(
                "Review service and payment integration are coming soon. "
                "For now, please contact us directly if you’d like a licensed realtor to review your draft."
            )

    # Global disclaimer under the whole mode
    st.markdown(DISCLAIMER_SHORT)

elif mode == "eval_property":
    st.subheader("Should I Buy This Property?")
    st.write("Property evaluation chat coming soon. For now, you can chat below.")
    show_generic_chat()

elif mode == "education":
    st.subheader("I’m New — Teach Me")
    st.write("Ask anything about homebuying, offers, or California forms. Chat below:")
    show_generic_chat()

elif mode == "free_chat":
    st.subheader("Ask Something Else")
    show_generic_chat()

else:
    st.warning("Unknown mode. Please pick an option above.")
