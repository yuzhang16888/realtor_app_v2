import streamlit as st

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
    st.session_state.current_mode = None      # which task the user selected

if "messages" not in st.session_state:
    st.session_state.messages = []            # this will store the chat messages

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False     # placeholder for now


# ==========================================================
# 🎛️ SIDEBAR (placeholder, will add real logic later)
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
# 🏡 HEADER — your brand
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
# 🧭 ACTION BUTTONS — small, clean, smart
# ==========================================================
st.markdown("### What do you want help with today?")

# 5 quick-action buttons
col1, col2, col3 = st.columns(3)
col4, col5, _ = st.columns(3)

with col1:
    if st.button("Draft an Offer Letter", use_container_width=True):
        st.session_state.current_mode = "offer_letter"
        st.session_state.messages = []   # reset chat

with col2:
    if st.button("Should I Buy This Property?", use_container_width=True):
        st.session_state.current_mode = "eval_property"
        st.session_state.messages = []

with col3:
    if st.button("Purchase Agreement", use_container_width=True):
        st.session_state.current_mode = "purchase_agreement"
        st.session_state.messages = []

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
# 💬 CHAT UI (placeholder version)
# ==========================================================
mode = st.session_state.current_mode

def show_chat_container():
    """Small helper to show chat messages."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message…")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Placeholder response (we will replace with GPT later)
        ai_response = "Thanks! I’ll help you shortly. (AI logic coming soon)"
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        with st.chat_message("assistant"):
            st.write(ai_response)



# ==========================================================
# 🧩 SHOW CONTENT BASED ON THE MODE
# ==========================================================
if mode is None:
    st.info("Select one of the options above to begin.")

elif mode == "offer_letter":
    st.subheader("Draft an Offer Letter")
    st.caption("We’ll guide you step-by-step. This screen will soon become a real chat flow.")
    show_chat_container()

elif mode == "eval_property":
    st.subheader("Should I Buy This Property?")
    st.caption("Paste a listing link and we’ll guide you through it.")
    show_chat_container()

elif mode == "purchase_agreement":
    st.subheader("Purchase Agreement")
    st.caption("This will eventually draft a formal agreement.")
    show_chat_container()

elif mode == "education":
    st.subheader("Homebuying Education")
    st.caption("We’ll explain the process in plain English.")
    show_chat_container()

elif mode == "free_chat":
    st.subheader("Ask Anything")
    st.caption("A free-form chat about buying a home.")
    show_chat_container()
