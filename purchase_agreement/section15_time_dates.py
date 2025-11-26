# purchase_agreement/section15_time_dates.py

import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai  # adjust path if needed


def render_section15_time_dates():
    """
    Render Section 15 – Time Periods; Dates; Time of Essence.

    UX design:
    - Top expander: Ask AI Realtor + Connect with Human Realtor.
    - Plain-English explanation of what 'time is of the essence' means.
    - Light user inputs: notes about flexibility/preferences on dates.
    """

    st.markdown("## 15. Time Periods; Dates; Time of Essence")

    # ---------------------------
    # 💬 GPT / AI Realtor + Human Realtor — Top Helper for Section 15
    # ---------------------------
    with st.expander("💬 Need help with Section 15 – Time & Dates?", expanded=True):

        st.markdown(
            "Use this assistant to understand how time periods and dates work in the contract, "
            "and what it means that **time is of the essence**.\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        default_prompt_15 = (
            "You are an experienced California residential real estate agent. "
            "Explain Section 15 of the CAR Residential Purchase Agreement in simple terms. "
            "Cover how time periods are counted (calendar vs business days), how deadlines "
            "relate to acceptance, when they can be extended, and what it means that "
            "'time is of the essence' in the contract. Provide practical, plain-language advice."
        )

        # --- FORM: Ask AI + Connect Human ---
        with st.form("pa15_ai_form_top"):
            user_prompt_15 = st.text_input(
                "Ask a question about time periods and dates (Section 15):",
                key="pa15_ai_prompt_top",
                placeholder=(
                    "Examples:\n"
                    "• Are these deadlines calendar days or business days?\n"
                    "• What does 'time is of the essence' really mean for me?\n"
                    "• How strict are closing and contingency dates?"
                ),
            )

            col_ai_top1, col_ai_top2 = st.columns([3, 2])

            with col_ai_top1:
                use_context_15 = st.checkbox(
                    "Include default context in my question",
                    key="pa15_ai_use_context_top",
                    value=True,
                )

            with col_ai_top2:
                ask_clicked_15_top = st.form_submit_button(
                    "Ask AI Realtor",
                    use_container_width=True,
                )
                connect_clicked_15_top = st.form_submit_button(
                    "Connect with a Human Realtor",
                    use_container_width=True,
                )

        # --- Handle Ask AI ---
        if ask_clicked_15_top:
            if not user_prompt_15.strip():
                st.warning("Please type something to ask the AI Realtor.")
            else:
                full_prompt_15 = user_prompt_15.strip()
                if use_context_15:
                    full_prompt_15 = (
                        default_prompt_15
                        + "\n\nUser question:\n"
                        + user_prompt_15.strip()
                    )

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer_15 = call_purchase_agreement_ai(
                            full_prompt_15,
                            section="15",
                        )
                    except Exception as e:
                        answer_15 = (
                            "There was an error calling the AI backend for Section 15.\n\n"
                            f"Details: {e}"
                        )
                    st.session_state["pa15_ai_answer_top"] = answer_15

        # --- Show AI Answer ---
        if "pa15_ai_answer_top" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa15_ai_answer_top"])

        # --- Handle Connect with Human Realtor ---
        if connect_clicked_15_top:
            st.session_state["pa15_show_human_realtor_form_top"] = True

        if st.session_state.get("pa15_show_human_realtor_form_top", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info_15_top = st.text_input(
                "Your preferred phone or email",
                key="pa15_human_contact_top",
                placeholder="Example: 415-555-1234 or you@example.com",
            )

            human_question_15_top = st.text_area(
                "What would you like to ask a human?",
                key="pa15_human_question_top",
                height=100,
                placeholder=(
                    "Example: I’m worried about hitting my loan and appraisal deadlines; "
                    "can you help me set realistic dates?\n"
                    "Example: How flexible is the closing date in my market?"
                ),
            )

            send_clicked_15_top = st.button(
                "Send my question to a Human Realtor",
                key="pa15_human_send_btn_top",
                use_container_width=True,
            )

            if send_clicked_15_top:
                if not contact_info_15_top.strip() or not human_question_15_top.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    st.session_state["pa15_human_realtor_request_top"] = {
                        "contact": contact_info_15_top.strip(),
                        "question": human_question_15_top.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )

    st.markdown("---")

    # ---------------------------
    # Plain-English summary of Section 15
    # ---------------------------
    st.markdown("### What Section 15 is about (plain English)")

    st.markdown(
        "- Section 15 explains **how all contract time periods and dates are counted**.\n"
        "- It typically uses **calendar days** (not business days), unless your contract "
        "is modified.\n"
        "- It confirms that **time is of the essence**, which means deadlines in the "
        "contract are important and can be enforced.\n"
        "- Changing key dates (like closing or contingency deadlines) usually requires "
        "a **written agreement** between buyer and seller (for example, an addendum)."
    )

    st.markdown("---")

    # ---------------------------
    # Light user inputs: notes about timing preferences
    # ---------------------------
    st.markdown("### Your preferences around timing (optional)")

    st.markdown(
        "You generally do **not** change the legal wording of Section 15 in the standard form, "
        "but it can help your agent (and future you) if you share your **timing preferences**."
    )

    col_timing1, col_timing2 = st.columns(2)

    with col_timing1:
        timing_flexibility = st.selectbox(
            "How flexible are you on closing date?",
            options=[
                "I need a very specific closing date",
                "I can be a little flexible (± 3–5 days)",
                "I am flexible within about 1–2 weeks",
            ],
            key="pa15_timing_flexibility",
        )

    with col_timing2:
        morning_evening_pref = st.selectbox(
            "Do you have a preference for signings / key handoff?",
            options=[
                "No strong preference",
                "Prefer earlier in the day",
                "Prefer later in the day",
            ],
            key="pa15_signing_pref",
        )

    timing_notes = st.text_area(
        "Any notes about dates, travel, or scheduling that might affect your timing?",
        key="pa15_timing_notes",
        placeholder=(
            "Example: I’m traveling during the last week of the month; prefer to avoid closing then.\n"
            "Example: My lease ends on the 30th, so I need to close before then or arrange a short-term overlap."
        ),
    )

    st.info(
        "These notes don’t automatically change the legal contract, but they can guide your agent "
        "when negotiating or adjusting dates (for example, through addenda)."
    )

    st.markdown("---")

    # ---------------------------
    # Quick reference: Time periods & 'time is of the essence'
    # ---------------------------
    st.markdown("### Quick reference: Time periods & 'time is of the essence'")

    with st.expander("📄 How time periods usually work", expanded=False):
        st.markdown(
            "- Most deadlines in the CAR RPA are **counted from the date of acceptance**.\n"
            "- Time periods are usually **calendar days**, including weekends and holidays.\n"
            "- If a deadline falls on a weekend or holiday, many agents still aim to perform on "
            "the prior business day, but the technical rule can depend on the specific form and any addenda.\n"
        )

    with st.expander("📄 What 'time is of the essence' means", expanded=False):
        st.markdown(
            "- When a contract says **time is of the essence**, it means **deadlines matter**.\n"
            "- Missing a deadline can give the other party certain rights, including issuing a "
            "Notice to Perform or, in some cases, cancelling the contract.\n"
            "- This is why your contingency periods, closing date, and delivery of disclosures "
            "are treated seriously by both sides."
        )

    st.markdown("---")

    # ---------------------------
    # Bottom navigation – Save / Next
    # ---------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Section 15", key="pa15_save"):
            # Hook this into your persistence logic (e.g., save to DB or session)
            st.success("Section 15 responses saved (connect this button to your save logic).")

    with col_right:
        if st.button("Next: Section 16", key="pa15_next"):
            # If you are using an active_pa_tab index, set it here (adjust index as needed)
            # Example:
            # st.session_state['active_pa_tab'] = 11  # whatever index corresponds to Section 16
            st.info("Moving to Section 16… (make sure this updates your main app navigation).")
