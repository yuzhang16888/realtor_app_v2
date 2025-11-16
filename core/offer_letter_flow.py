import streamlit as st

# How many steps the wizard has (0..7)
MAX_OFFER_STEP = 7


def _init_offer_state():
    """
    Ensure all offer-letter-related state exists in st.session_state.
    This keeps app.py clean — it doesn't need to know the internal keys.
    """
    ss = st.session_state
    if "offer_step" not in ss:
        ss.offer_step = 0
    if "offer_data" not in ss:
        ss.offer_data = {}
    if "offer_messages" not in ss:
        ss.offer_messages = []


def _get_offer_prompt_for_step(step: int) -> str:
    """
    Return the assistant's question for the current step.
    This is where we control the UX wording of the wizard.
    """
    prompts = {
        0: (
            "Great, let’s draft your offer letter together.\n\n"
            "First, what is the **property address or listing link**?"
        ),
        1: (
            "Got it. What is the **buyer’s full legal name**, exactly as it should appear on the offer?\n\n"
            "If there are multiple buyers, please list all full legal names."
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


def _generate_offer_letter_text(data: dict) -> str:
    """
    Create a formal, professional offer-letter draft from collected data.
    """
    property_address = data.get("property_address", "[Property Address]")
    buyer_name = data.get("buyer_name", "[Buyer Name]")
    offer_price = data.get("offer_price", "[Offer Price]")
    earnest_money = data.get("earnest_money", "[Earnest Money]")
    closing_timeline = data.get("closing_timeline", "[Closing Timeline]")
    offer_expiration = data.get("offer_expiration", "[Offer Expiration]")
    contingencies = data.get(
        "contingencies",
        "Standard inspection, appraisal, and financing contingencies."
    )
    special_terms = data.get("special_terms", "None specified.")

    return f"""
**Offer Letter — {property_address}**

Dear Listing Agent / Seller,

On behalf of **{buyer_name}**, I am pleased to submit this offer to purchase the property located at **{property_address}**. We appreciate your consideration and have outlined the proposed terms below for your review.

---

### 📌 Key Offer Terms

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

### 📄 Acknowledgment

This letter serves as a summary of the buyer’s intentions and proposed terms. The full contractual obligations will be detailed in the formal Residential Purchase Agreement and related disclosures.

{buyer_name} is prepared to cooperate promptly and professionally throughout the process and looks forward to working together toward a successful transaction.

Thank you for your time and consideration.

Sincerely,  
**{buyer_name}**

---

"""


def show_offer_letter_flow():
    """
    Main entrypoint for the Offer Letter wizard.
    Called from app.py. Handles:
    - rendering previous messages
    - asking the next question
    - capturing the user's answer
    - generating the final letter
    """
    _init_offer_state()
    ss = st.session_state

    # 1) Show existing Q&A history
    for msg in ss.offer_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    step = ss.offer_step

    # 2) Ask the current question (if we still have steps left)
    if step <= MAX_OFFER_STEP:
        prompt = _get_offer_prompt_for_step(step)
        # Only append if it's not already the last assistant message
        if not ss.offer_messages or ss.offer_messages[-1]["content"] != prompt:
            ss.offer_messages.append({"role": "assistant", "content": prompt})
            with st.chat_message("assistant"):
                st.write(prompt)

    # 3) Wait for user answer
    user_input = st.chat_input("Answer here…")
    if not user_input:
        # Nothing typed yet → just show current prompt & history
        return

    # 4) Record user's message
    ss.offer_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # 5) Save structured data based on current step
    text = user_input.strip()
    if step == 0:
        ss.offer_data["property_address"] = text
    elif step == 1:
        ss.offer_data["buyer_name"] = text
    elif step == 2:
        ss.offer_data["offer_price"] = text
    elif step == 3:
        ss.offer_data["earnest_money"] = text
    elif step == 4:
        ss.offer_data["closing_timeline"] = text
    elif step == 5:
        ss.offer_data["offer_expiration"] = text
    elif step == 6:
        ss.offer_data["contingencies"] = text
    elif step == 7:
        ss.offer_data["special_terms"] = text

    # 6) Advance to next step
    ss.offer_step += 1
    step = ss.offer_step

    # 7) If all steps done → generate final letter
    if step > MAX_OFFER_STEP:
        draft = _generate_offer_letter_text(ss.offer_data)
        ss.offer_messages.append({"role": "assistant", "content": draft})
        with st.chat_message("assistant"):
            st.markdown(draft)

    # 8) Rerun so the next question (or final draft) appears immediately
    st.rerun()
