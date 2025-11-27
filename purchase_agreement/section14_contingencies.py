# purchase_agreement/section14_contingencies.py

import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai  # adjust path if needed


def render_section14_contingencies():
    """
    Render Section 4 – Contingencies; Removal of Contingencies; Cancellation Rights.

    UX design:
    - Top expander: Ask AI Realtor + Connect with Human Realtor.
    - User only edits 14B(1) (number of days for buyer contingencies + notes).
    - 14B(2), 14B(3), 14B(4) shown as plain-English explanations and tables.
    """

    st.markdown("## 4. Contingencies, Removal of Contingencies, and Cancellation Rights")

       # ---------------------------
    # 💬 GPT / AI Realtor + Human Realtor — Top Helper for Section 14
    # ---------------------------
    with st.expander("💬 Need help with contingencies?", expanded=True):

        st.markdown(
            "Use this assistant to understand contingency periods, deadlines, Notices to Perform, "
            "and cancellation rights.\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        # --- FORM for Ask AI + Connect Human ---
        with st.form("pa14_ai_form_top"):
            user_prompt_14 = st.text_input(
                "Ask a question about contingencies (Section 14):",
                key="pa14_ai_prompt_top",
                placeholder=(
                    "Examples:\n"
                    "• What happens if I miss my contingency deadline?\n"
                    "• What is a 'Notice to Perform'?\n"
                    "• Can I cancel if the seller is late with disclosures?"
                ),
            )

            ask_clicked_14_top = st.form_submit_button(
                "Ask AI Realtor",
                use_container_width=True,
            )
            connect_clicked_14_top = st.form_submit_button(
                "Connect with a Human Realtor",
                use_container_width=True,
            )

        # --- Handle Ask AI ---
        if ask_clicked_14_top:
            if not user_prompt_14.strip():
                st.warning("Please type something to ask the AI Realtor.")
            else:
                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer_14 = call_purchase_agreement_ai(
                            user_prompt_14.strip(),
                            section="14",
                            # If you have a Section 14 state dict, you can pass it here:
                            # section_state=st.session_state[SECTION14_KEY],
                        )
                    except Exception as e:
                        answer_14 = (
                            "There was an error calling the AI backend for Section 14.\n\n"
                            f"Details: {e}"
                        )
                    st.session_state["pa14_ai_answer_top"] = answer_14

        # --- Show AI Answer ---
        if "pa14_ai_answer_top" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa14_ai_answer_top"])

        # --- Handle Connect with Human Realtor ---
        if connect_clicked_14_top:
            st.session_state["pa14_show_human_realtor_form_top"] = True

        if st.session_state.get("pa14_show_human_realtor_form_top", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info_14_top = st.text_input(
                "Your preferred phone or email",
                key="pa14_human_contact_top",
                placeholder="Example: 415-555-1234 or you@example.com",
            )

            human_question_14_top = st.text_area(
                "What would you like to ask a human?",
                key="pa14_human_question_top",
                height=100,
                placeholder=(
                    "Example: Can you help me select a safe but competitive contingency period?\n"
                    "Example: Should I shorten my inspection contingency for a competitive offer?\n"
                    "Example: What is typical in Bay Area contingencies?"
                ),
            )

            send_clicked_14_top = st.button(
                "Send my question to a Human Realtor",
                key="pa14_human_send_btn_top",
                use_container_width=True,
            )

            if send_clicked_14_top:
                if not contact_info_14_top.strip() or not human_question_14_top.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    st.session_state["pa14_human_realtor_request_top"] = {
                        "contact": contact_info_14_top.strip(),
                        "question": human_question_14_top.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )

    st.markdown("---")

    # ---------------------------
    # Short plain-English summary
    # ---------------------------
    st.markdown("### What Section 4 is about (plain English)")

    st.markdown(
        "- Section 4 explains your **buyer contingencies** — conditions that must be satisfied "
        "before you are fully locked into the purchase.\n"
        "- It sets the **time period** for your contingencies, and explains how and when they "
        "must be removed.\n"
        "- It also explains **what happens if either side fails to perform**, including when a "
        "Notice to Perform can be used and when someone may cancel the contract."
    )

    st.markdown("---")

    # ---------------------------
    # 14B(1) – Time to remove buyer contingencies (user input)
    # ---------------------------
    st.markdown("### 4B(1). Time to Remove Buyer Contingencies")

    st.markdown(
        "Here you choose **how many days after offer acceptance** you want to keep your "
        "buyer contingencies in place before you must either:\n"
        "- remove contingencies and move forward, or\n"
        "- cancel the contract.\n\n"
        "Shorter contingency periods can make your offer more competitive but give you less time "
        "to investigate and get comfortable. Longer periods give you more protection but can make "
        "your offer less attractive to the seller. Talk to your agent about what’s typical in your area."
    )

    col_days, col_notes = st.columns([1, 2])

    with col_days:
        contingency_days = st.number_input(
            "Total days after acceptance for buyer contingencies",
            min_value=0,
            max_value=60,
            value=17,
            step=1,
            key="pa14B1_contingency_days",
            help=(
                "Number of days after the seller accepts your offer "
                "for you to complete inspections, review disclosures, and "
                "decide whether to proceed."
            ),
        )

    with col_notes:
        st.text_area(
            "Notes or preferences about your contingency period (optional)",
            key="pa14B1_notes",
            placeholder=(
                "Example: I prefer 10 days because my inspections can be scheduled quickly.\n"
                "Example: I want 21 days because I need extra time for loan approval and HOA docs."
            ),
        )

    st.info(
        f"You've selected **{contingency_days} day(s)** after acceptance for your buyer contingencies."
    )

    st.markdown("---")

    # ---------------------------
    # 14B(2)–(4) – Plain-language explanations (read-only)
    # ---------------------------
    st.markdown("### 4B(2)–(4). What happens if someone doesn’t perform?")

    with st.expander("📄 4B(2) – Seller’s right to cancel if buyer does nothing", expanded=False):
        st.markdown(
            "- If your contingency period expires and you do **nothing** "
            "(you don’t remove contingencies and you don’t cancel), the seller can issue a "
            "**48-hour 'Notice to Buyer to Perform'.**\n"
            "- If you still don’t act within those 48 hours, the seller may have the right "
            "to **cancel the contract**.\n"
        )

        st.markdown("**Who must do what, and by when:**")
        st.markdown(
            "| Party | Responsibility | When |\n"
            "|-------|----------------|------|\n"
            "| **Buyer** | Remove contingencies or cancel | Before the contingency period expires |\n"
            "| **Seller** | May issue a *Notice to Buyer to Perform* | After buyer fails to act by the deadline |\n"
            "| **Buyer** | Must perform (remove or cancel) after notice | Within 48 hours after receiving the notice |\n"
            "| **Seller** | May cancel the contract | If buyer still does nothing after the 48 hours |\n"
        )

    with st.expander("📄 4B(3) – Seller delays that affect buyer’s deadlines", expanded=False):
        st.markdown(
            "- If the seller is late delivering required disclosures, reports, or access, "
            "your contingency deadlines can be **affected and may be extended**.\n"
            "- You are not expected to remove contingencies based on information that the "
            "seller has not yet provided.\n"
        )

        st.markdown("**Who must do what, and how it affects deadlines:**")
        st.markdown(
            "| Party | Responsibility | Effect on deadlines |\n"
            "|-------|----------------|---------------------|\n"
            "| **Seller** | Provide required disclosures, access, or repairs | Within the agreed time (e.g., 7 days) |\n"
            "| **Buyer** | May receive extended contingency periods if seller is late | Deadlines may be extended until seller has completed their part |\n"
            "| **Seller** | Must complete tasks before expecting buyer to remove contingencies | Buyer’s practical countdown starts after seller performs |\n"
        )

    with st.expander("📄 4B(4) – Buyer’s right to cancel if seller doesn’t perform", expanded=False):
        st.markdown(
            "- If the seller fails to perform their obligations (for example, providing "
            "disclosures, allowing access, completing agreed repairs, or signing required "
            "paperwork), you can issue a **'Notice to Seller to Perform'** giving them "
            "48 hours to comply.\n"
            "- If the seller still doesn’t perform after that 48-hour period, you may have "
            "the right to **cancel the contract**.\n"
        )

        st.markdown("**Who must do what, and by when:**")
        st.markdown(
            "| Party | Responsibility | When |\n"
            "|-------|----------------|------|\n"
            "| **Seller** | Deliver disclosures, allow access, complete agreed repairs, sign required papers | By the agreed timelines in the contract |\n"
            "| **Buyer** | May issue a *Notice to Seller to Perform* | If seller fails to perform on time |\n"
            "| **Seller** | Must perform after receiving the notice | Within 48 hours after receiving the notice |\n"
            "| **Buyer** | May cancel the contract | If seller still has not performed after the 48 hours |\n"
        )

    st.markdown("---")

    # ---------------------------
    # Bottom navigation – Save / Next
    # ---------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Section 4", key="pa14_save"):
            # Hook this into your persistence logic (e.g., save to DB or session)
            st.success("Section 4 responses saved (connect this button to your save logic).")

    with col_right:
        if st.button("Next: Section 5", key="pa14_next"):
            # If you are using an active_pa_tab index, set it here (adjust index as needed)
            # Example:
            # st.session_state['active_pa_tab'] = 10  # whatever index corresponds to Section 15
            st.info("Moving to Section 5… (make sure this updates your main app navigation).")
