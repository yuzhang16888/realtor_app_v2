# purchase_agreement/section31_expiration.py

import streamlit as st
from datetime import datetime, timedelta
from purchase_agreement.ai_helpers import call_purchase_agreement_ai


def render_section31_expiration():
    """
    Section 4 – Expiration of Offer
    Buyer sets the exact date/time their offer expires.
    """

    #st.markdown("## 31. Expiration of Offer")

    # --------------------------------------------------
    # 💬 GPT + Human Realtor Helper (Top)
    # --------------------------------------------------
    with st.expander("💬 Need help with Offer Expiration (Section 31)?", expanded=True):
        st.markdown(
            "This section controls **when your offer automatically expires** if the seller does "
            "NOT accept it by a specific deadline.\n\n"
            "**Reminder:** Not legal advice. Always confirm with your agent or attorney."
        )

        default_prompt_31 = (
            "You are an experienced California residential real estate agent. "
            "Explain Section 31 – Expiration of Offer in the CAR Residential Purchase Agreement "
            "in clear, simple terms. Cover:\n"
            "- Why buyers set an expiration deadline.\n"
            "- Seller pressure vs flexibility.\n"
            "- Typical practices in competitive markets vs slow markets.\n"
            "- What happens if the seller signs after the deadline.\n"
            "- How expiration affects when the contract becomes binding.\n"
            "Do NOT give legal advice; keep explanations practical and buyer-oriented."
        )

        # Form
        with st.form("pa31_ai_form"):
            user_prompt_31 = st.text_input(
                "What do you want help with in Section 31?",
                key="pa31_ai_prompt",
                placeholder=(
                    "Examples:\n"
                    "• What is a reasonable expiration deadline in San Francisco?\n"
                    "• What happens if the seller signs after the expiration time?\n"
                    "• Should I set my expiration earlier to pressure the seller?"
                ),
            )

            col1, col2 = st.columns([3, 2])

            with col1:
                use_context_31 = st.checkbox(
                    "Include default Section 31 context",
                    value=True,
                    key="pa31_use_context",
                )
            with col2:
                ask_ai_clicked = st.form_submit_button(
                    "Ask AI Realtor",
                    use_container_width=True,
                )
                connect_clicked = st.form_submit_button(
                    "Connect with a Human Realtor",
                    use_container_width=True,
                )

        # Handle Ask AI
        if ask_ai_clicked:
            if not user_prompt_31.strip():
                st.warning("Please enter a question first.")
            else:
                full_prompt_31 = user_prompt_31.strip()
                if use_context_31:
                    full_prompt_31 = default_prompt_31 + "\n\nUser question:\n" + user_prompt_31.strip()

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer_31 = call_purchase_agreement_ai(full_prompt_31, section="31")
                    except Exception as e:
                        answer_31 = f"There was an error calling the AI backend.\n\nDetails: {e}"

                st.session_state["pa31_ai_answer"] = answer_31

        # Show AI answer
        if "pa31_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa31_ai_answer"])

        # Human Realtor Form
        if connect_clicked:
            st.session_state["pa31_show_human"] = True

        if st.session_state.get("pa31_show_human", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_31 = st.text_input(
                "Your preferred phone or email",
                key="pa31_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )

            question_31 = st.text_area(
                "What would you like to ask a human?",
                key="pa31_human_question",
                height=100,
                placeholder="Example: Can you help me choose the right expiration time for my offer?",
            )

            send_clicked = st.button("Send my question to a Human Realtor")

            if send_clicked:
                if not contact_31.strip() or not question_31.strip():
                    st.warning("Please provide both your contact info and your message.")
                else:
                    st.session_state["pa31_human_request"] = {
                        "contact": contact_31.strip(),
                        "question": question_31.strip(),
                    }
                    st.success("Your request has been sent. A human realtor will reach out to you.")

    st.markdown("---")

    # --------------------------------------------------
    # Plain-English Summary
    # --------------------------------------------------
    st.markdown("### What this means (plain English)")

    st.markdown(
        "- The offer automatically **expires** at the exact date and time you set.\n"
        "- The seller must **sign and return acceptance** by that deadline for it to become binding.\n"
        "- If the seller accepts **after the deadline**, it is NOT a valid acceptance unless the buyer re-approves.\n"
        "- A shorter expiration:\n"
        "  - increases pressure on the seller\n"
        "  - is common in competitive markets\n"
        "- A longer expiration:\n"
        "  - gives the seller more time\n"
        "  - can be helpful in slower markets or complex situations"
    )

    st.markdown("---")

    # --------------------------------------------------
    # 31 – User Input (Expiration Date and Time)
    # --------------------------------------------------

    st.markdown("### Set Your Offer Expiration")

    # Default expiration: 24 hours from now
    default_dt = datetime.now() + timedelta(hours=24)

    col_date, col_time = st.columns(2)

    with col_date:
        exp_date = st.date_input(
            "Expiration Date",
            value=default_dt.date(),
            key="pa31_date",
        )

    with col_time:
        exp_time = st.time_input(
            "Expiration Time",
            value=default_dt.time().replace(second=0, microsecond=0),
            key="pa31_time",
        )

    expiration_dt = datetime.combine(exp_date, exp_time)

    # Warning if expiration is unreasonable
    if expiration_dt < datetime.now():
        st.error("⚠️ The expiration date/time is in the past. Please choose a future time.")

    elif expiration_dt < datetime.now() + timedelta(hours=6):
        st.warning(
            "⚠️ This expiration is **very short**. Sellers may not have time to review. "
            "Use a short deadline only when intentional."
        )

    elif expiration_dt > datetime.now() + timedelta(days=7):
        st.warning(
            "⚠️ This expiration is **very long**. Most sellers expect 24–72 hours unless otherwise discussed."
        )

    st.info(f"Your offer will expire on **{expiration_dt.strftime('%B %d, %Y at %I:%M %p')}** unless accepted earlier.")

    st.markdown("---")

    # --------------------------------------------------
    # Optional User Notes
    # --------------------------------------------------
    st.markdown("### Notes (optional)")

    st.text_area(
        "Anything you want to remember or ask your agent about offer timing?",
        key="pa31_notes",
        height=100,
        placeholder=(
            "Examples:\n"
            "- Ask if a shorter expiration could strengthen my offer.\n"
            "- Confirm seller availability (travel, weekend, holiday timing).\n"
            "- Coordinate expiration with lender letter timing."
        ),
    )

    st.markdown("---")

    # --------------------------------------------------
    # Save / Next
    # --------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save "):
            st.success("saved (connect this to your persistence logic).")

    with col_right:
        if st.button("Next:Final Review"):
            # Example navigation (adjust index to your app)
            # st.session_state['active_pa_tab'] = your_next_tab_index
            st.info("Moving to Final Signatures…")
