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
    st.session_state.current_mode = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# Offer letter state
if "offer_step" not in st.session_state:
    st.session_state.offer_step = 0

if "offer_last_prompted_step" not in st.session_state:
    st.session_state.offer_last_prompted_step = -1

if "offer_data" not in st.session_state:
    st.session_state.offer_data = {}

if "offer_messages" not in st.session_state:
    st.session_state.offer_messages = []
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

def reset_offer_state():
    st.session_state.offer_step = 0
    st.session_state.offer_last_prompted_step = -1
    st.session_state.offer_data = {}
    st.session_state.offer_messages = []

with col1:
    if st.button("Draft an Offer Letter", use_container_width=True):
        st.session_state.current_mode = "offer_letter"
        reset_offer_state()

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
# 💬 GENERIC CHAT (for non-offer flows)
# ==========================================================
def show_generic_chat():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message…")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        ai_response = "Thanks! I’ll help you shortly. (AI logic coming later)"
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.write(ai_response)


# ==========================================================
# ✉️ OFFER LETTER — GUIDED QUESTION PROMPTS
# ==========================================================
def get_offer_prompt_for_step(step: int) -> str:
    prompts = {
        0: (
            "Great, let’s draft your offer letter together.\n\n"
            "First, what is the **property address or listing link**?"
        ),
        1: (
            "Got it. What is the **buyer’s full legal name**, exactly as it should appear on the offer?\n\n"
            "If there are multiple buyers, list all full legal names."
        ),
        2: (
            "Thanks. What is your **offer price** (in dollars)?\n\n"
            "You can type a number like `1,250,000`."
        ),
        3: (
            "Great. How much **earnest money** would you like to offer?\n\n"
            "Earnest money is usually around **1%–3% of the purchase price**."
        ),
        4: (
            "Noted. What is your **preferred closing timeline**?\n\n"
            "For example: “30 days after offer acceptance.” Typical closings are around **21–30 days** after acceptance."
        ),
        5: (
            "Until **when** should this offer remain valid? (Offer expiration)\n\n"
            "For example: “This offer expires on Monday at 5:00 PM Pacific.”"
        ),
        6: (
            "Let’s choose your **contingencies**.\n\n"
            "A contingency is a protection for the buyer. Common ones:\n"
            "• **Inspection** – inspect the property and request repairs.\n"
            "• **Financing** – your loan must be approved.\n"
            "• **Appraisal** – the property must appraise at or above the purchase price.\n\n"
            "Which contingencies would you like to include?"
        ),
        7: (
            "Any **special terms** you want to include? (Optional)\n\n"
            "Examples:\n"
            "• Do you need to sell your current home first?\n"
            "• Buying on behalf of someone (child/parent/LLC)?\n"
            "• Want a rent-back period for the seller or to include certain items (appliances, furniture)?\n\n"
            "If nothing special, type “none”."
        ),
    }
    return prompts.get(step, "")

    


# ==========================================================
# 📄 OFFER LETTER GENERATOR
# ==========================================================
def generate_offer_letter_text(data: dict) -> str:
    property_address = data.get("property_address", "[Property Address]")
    buyer_name = data.get("buyer_name", "[Buyer Name]")
    offer_price = data.get("offer_price", "[Offer Price]")
    earnest_money = data.get("earnest_money", "[Earnest Money]")
    closing_timeline = data.get("closing_timeline", "[Closing Timeline]")
    offer_expiration = data.get("offer_expiration", "[Offer Expiration]")
    contingencies = data.get("contingencies", "Standard inspection, appraisal, and financing contingencies.")
    special_terms = data.get("special_terms", "None specified.")

    return f"""
**Offer Letter — {property_address}**

Dear Listing Agent / Seller,

On behalf of **{buyer_name}**, I am pleased to submit this offer to purchase the property located at **{property_address}**. We appreciate your consideration and have outlined the proposed terms below for your review.

---

### **📌 Key Offer Terms**

**1. Purchase Price:**  
${offer_price}

**2. Earnest Money Deposit:**  
${earnest_money}  
This deposit will be placed into escrow upon acceptance of the offer.

**3. Closing Timeline:**  
{closing_timeline}

**4. Offer Expiration:**  
This offer remains valid until **{offer_expiration}**, unless formally withdrawn or extended in writing.

**5. Contingencies:**  
{contingencies}

**6. Special Terms (if any):**  
{special_terms}

---

### **📄 Acknowledgment**

This letter serves as a summary of the buyer’s intentions and proposed terms. The full contractual obligations will be detailed in the formal Residential Purchase Agreement and related disclosures.

{buyer_name} is prepared to cooperate promptly and professionally throughout the process and looks forward to working together toward a successful transaction.

Thank you for your time and consideration.

Sincerely,  
**{buyer_name}**

---

*This draft was generated for convenience. Please review the formal Residential Purchase Agreement for binding terms.*
"""

# ==========================================================
# 🤖 OFFER LETTER FLOW (guided wizard)
# ==========================================================
def show_offer_letter_flow():
    """Guided chat for drafting an offer letter."""

    # 1) Show previous messages (Q&A history)
    for msg in st.session_state.offer_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    step = st.session_state.offer_step

    # 2) If we still have questions to ask, show the current one
    if step <= 6:
        prompt = get_offer_prompt_for_step(step)
        # Only add the prompt once per step
        if not st.session_state.offer_messages or st.session_state.offer_messages[-1]["content"] != prompt:
            st.session_state.offer_messages.append({"role": "assistant", "content": prompt})
            with st.chat_message("assistant"):
                st.write(prompt)

    # 3) Wait for user's answer
    user_input = st.chat_input("Answer here…")
    if not user_input:
        # Nothing typed yet → just show current prompt & history
        return

    # 4) Record and show user's answer
    st.session_state.offer_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 5) Save data depending on step
    if step == 0:
        st.session_state.offer_data["property_address"] = user_input.strip()
    elif step == 1:
        st.session_state.offer_data["buyer_name"] = user_input.strip()
    elif step == 2:
        st.session_state.offer_data["offer_price"] = user_input.strip()
    elif step == 3:
        st.session_state.offer_data["earnest_money"] = user_input.strip()
    elif step == 4:
        st.session_state.offer_data["closing_timeline"] = user_input.strip()
    elif step == 5:
        st.session_state.offer_data["offer_expiration"] = user_input.strip()
    elif step == 6:
        st.session_state.offer_data["contingencies"] = user_input.strip()
    elif step == 7:
        st.session_state.offer_data["special_terms"] = user_input.strip()

      
    # 6) Move to the next step
    st.session_state.offer_step += 1
    step = st.session_state.offer_step

    # 7) If we just finished the last step, generate the draft
    if step > 6:
        draft = generate_offer_letter_text(st.session_state.offer_data)
        st.session_state.offer_messages.append({"role": "assistant", "content": draft})
        with st.chat_message("assistant"):
            st.markdown(draft)

    # 8) Immediately rerun so the next question (or final draft) shows up fast
    st.rerun()



# ==========================================================
# 🧩 MODE ROUTER — Which flow to show?
# ==========================================================
mode = st.session_state.current_mode

if mode is None:
    st.info("Select one of the options above to begin.")

elif mode == "offer_letter":
    st.subheader("Draft an Offer Letter")
    st.caption("We’ll guide you step-by-step and generate a complete draft.")
    show_offer_letter_flow()

elif mode == "eval_property":
    st.subheader("Should I Buy This Property?")
    show_generic_chat()

elif mode == "purchase_agreement":
    st.subheader("Purchase Agreement")
    show_generic_chat()

elif mode == "education":
    st.subheader("Homebuying Education")
    show_generic_chat()

elif mode == "free_chat":
    st.subheader("Ask Anything")
    show_generic_chat()
