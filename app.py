import streamlit as st
from core.offer_letter_flow import show_offer_letter_flow
from purchase_agreement.section1_offer import render_section_1_offer
from purchase_agreement.section2_agency import render_section_2_agency
from purchase_agreement.section3_finance import render_section3_finance
from purchase_agreement.section4_sale_of_buyer_property import render_section4_sale_of_buyer_property
from purchase_agreement.section6_other_terms import render_section6_other_terms
from purchase_agreement.section7_allocation_costs import render_section7_allocation_costs
from purchase_agreement.section8_property_condition import render_section8_property_condition
from purchase_agreement.section9_closing_possession import render_section9_closing_possession
from purchase_agreement.section10_13_overview import render_section10_13_overview
from purchase_agreement.section14_contingencies import render_section14_contingencies
from purchase_agreement.section15_time_dates import render_section15_time_dates
from purchase_agreement.section16_20_info import render_section16_20_info
from purchase_agreement.section21_22_remedies_disputes import render_section21_22_remedies_disputes
from purchase_agreement.section23_30_overview import render_section23_30_overview
from purchase_agreement.section31_expiration import render_section31_expiration
from purchase_agreement.section_final_review_signatures import render_final_review_signatures
from purchase_agreement.section_signatures_export import render_signatures_export


# ==========================================================
# 🚀 STREAMLIT APP CONFIG
# ==========================================================
st.set_page_config(
    page_title="Buyerside AI Realtor with human in loop",
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

# Offer letter state (used inside the Offer Letter flow)
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
> Please review all terms carefully before using this in a real transaction.
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
        <h1 style="margin-bottom: 0;">Buyerside AI Realtor with human in loop</h1>
        <p style="margin-top: 0.3rem; font-size: 1.05rem; color: gray;">
                only pay for what you need,
                  plan starting from $99
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
    # Combined entry: purchase agreement + (future) offer letter
    if st.button("Purchase Agreement (Offer Letter)", use_container_width=True):
        st.session_state.current_mode = "purchase_agreement"
        reset_offer_state()
        st.session_state.messages = []

with col2:
    if st.button("Should I Buy This Property?", use_container_width=True):
        st.session_state.current_mode = "eval_property"
        st.session_state.messages = []

with col3:
    # reserved for future feature
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
        "We’ll guide you through the **core deal terms first** (price, financing, sale of your current home, "
        "and when your offer expires), then walk through costs, condition, contingencies, and the remaining fine print."
    )

    # ======================================================
    # 🧱 TABS – COLLAPSED STRUCTURE
    # ======================================================
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Core Deal Terms (1, 3, 4–5, Expiration)",
            "Section 7 – Costs",
            "Section 8 – Condition & Repairs",
            "Section 14 – Contingencies",
            "Section 15 – Final Verification",
            "Other (Agency, Misc & Disclosures)",
            "Final Review & Export",
        ]
    )

    # 1️⃣ Core Deal Terms: Section 1 + Section 3 + Sections 4–5 + Expiration
    with tab1:
        st.markdown("### Section 1 – Offer")
        render_section_1_offer()

        st.markdown("---")
        # st.markdown("### Section 3 – Finance")
        render_section3_finance()

        st.markdown("---")
        st.markdown("### Subject to Sale of Buyer's Property")
        render_section4_sale_of_buyer_property()

        st.markdown("---")
        st.markdown("### Expiration of Offer")
        render_section31_expiration()

    # 2️⃣ Section 7 – Costs
    with tab2:
        render_section7_allocation_costs()

    # 3️⃣ Section 8 – Condition & Repairs
    with tab3:
        render_section8_property_condition()

    # 4️⃣ Section 14 – Contingencies
    with tab4:
        render_section14_contingencies()

    # 5️⃣ Section 15 – Final Verification / Time
    with tab5:
        render_section15_time_dates()

    # 6️⃣ Other: Agency, Misc, Disclosures, General Terms
    with tab6:
        st.markdown("### Section 2 – Agency / Representation")
        render_section_2_agency()

        st.markdown("---")
        st.markdown("### Section 6 – Other Terms (Optional)")
        render_section6_other_terms()

        st.markdown("---")
        st.markdown("### Sections 10–13 – Disclosures Overview")
        render_section10_13_overview()

        st.markdown("---")
        st.markdown("### Sections 16–20 – Repairs, Taxes & Other Details")
        render_section16_20_info()

        st.markdown("---")
        st.markdown("### Sections 21–22 – Remedies & Dispute Resolution")
        render_section21_22_remedies_disputes()

        st.markdown("---")
        st.markdown("### Sections 23–30 – General Terms & Brokers")
        render_section23_30_overview()

    # 7️⃣ Final Review + Export in one flow
    with tab7:
        st.markdown("### Step 1 – Final Review of Key Terms")
        render_final_review_signatures()

        st.markdown("---")
        st.markdown("### Step 2 – Signatures & Export")
        render_signatures_export()

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
