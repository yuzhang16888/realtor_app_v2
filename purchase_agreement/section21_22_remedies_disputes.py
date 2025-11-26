# purchase_agreement/section21_22_remedies_disputes.py

import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai  # adjust path if needed


def render_section21_22_remedies_disputes():
    """
    Combined view for Sections 21–22 of the CAR Residential Purchase Agreement.

    Focus:
    - Section 21: Remedies for buyer and seller if one party breaches.
    - Section 22: Mediation and arbitration (how disputes are resolved).

    UX:
    - Top helper with Ask AI Realtor + Connect with Human Realtor.
    - Clear, plain-English explanation of remedies and dispute resolution.
    - Expanders for more detail and simple tables.
    - User can add personal notes (e.g., how they feel about arbitration or risk).
    """

    st.markdown("## Sections 21–22 – Remedies & Dispute Resolution")

    # --------------------------------------------------
    # 💬 GPT / AI Realtor + Human Realtor – Top Helper
    # --------------------------------------------------
    with st.expander("💬 Need help with remedies & dispute resolution (Sections 21–22)?", expanded=True):
        st.markdown(
            "These sections explain **what can happen if someone breaches the contract** and "
            "how disputes are supposed to be handled (mediation, arbitration, court, attorney’s fees).\n\n"
            "**Reminder:** This is educational information only and not legal advice. "
            "You should talk to your own broker or attorney before making decisions about "
            "remedies, mediation, or arbitration."
        )

        default_prompt_21_22 = (
            "You are an experienced California residential real estate agent. "
            "Explain Sections 21 and 22 of the CAR Residential Purchase Agreement in simple, "
            "neutral terms. Cover:\n"
            "- What 'remedies' are available to a buyer or seller if the other party breaches.\n"
            "- What 'liquidated damages' generally means when both parties initial it.\n"
            "- The concept of specific performance (especially when a seller breaches).\n"
            "- How mediation works and why the contract requires attempting it before court.\n"
            "- What arbitration is, that it is optional and requires separate initials, and that "
            "it affects the right to a jury trial.\n"
            "Do not give legal advice or tell the user what they *should* choose; just explain "
            "the concepts and remind them to consult their own attorney."
        )

        with st.form("pa21_22_ai_form"):
            user_prompt_21_22 = st.text_input(
                "What do you want help with in Sections 21–22?",
                key="pa21_22_ai_prompt",
                placeholder=(
                    "Examples:\n"
                    "• What happens if I back out after removing contingencies?\n"
                    "• What is liquidated damages and does it always mean I lose my deposit?\n"
                    "• What is the difference between mediation and arbitration?\n"
                    "• What does it mean that I may give up my right to a jury trial?"
                ),
            )

            col_ai1, col_ai2 = st.columns([3, 2])

            with col_ai1:
                use_context_21_22 = st.checkbox(
                    "Include default Sections 21–22 context in my question",
                    value=True,
                    key="pa21_22_ai_use_context",
                )

            with col_ai2:
                ask_clicked_21_22 = st.form_submit_button(
                    "Ask AI Realtor",
                    use_container_width=True,
                )
                connect_clicked_21_22 = st.form_submit_button(
                    "Connect with a Human Realtor",
                    use_container_width=True,
                )

        # Handle Ask AI
        if ask_clicked_21_22:
            if not user_prompt_21_22.strip():
                st.warning("Please enter a question or description first.")
            else:
                full_prompt_21_22 = user_prompt_21_22.strip()
                if use_context_21_22:
                    full_prompt_21_22 = (
                        default_prompt_21_22
                        + "\n\nUser question:\n"
                        + user_prompt_21_22.strip()
                    )

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer_21_22 = call_purchase_agreement_ai(
                            full_prompt_21_22,
                            section="21-22",
                        )
                    except Exception as e:
                        answer_21_22 = (
                            "There was an error calling the AI backend for Sections 21–22.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa21_22_ai_answer"] = answer_21_22

        # Show AI answer
        if "pa21_22_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa21_22_ai_answer"])

        # Handle Connect with Human Realtor
        if connect_clicked_21_22:
            st.session_state["pa21_22_show_human_realtor_form"] = True

        if st.session_state.get("pa21_22_show_human_realtor_form", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info_21_22 = st.text_input(
                "Your preferred phone or email",
                key="pa21_22_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )

            human_question_21_22 = st.text_area(
                "What would you like to ask a human?",
                key="pa21_22_human_question",
                height=100,
                placeholder=(
                    "Example: Can you walk me through what liquidated damages means in my case?\n"
                    "Example: Can you help me understand pros/cons of initialing the arbitration clause?"
                ),
            )

            send_clicked_21_22 = st.button(
                "Send my question to a Human Realtor",
                key="pa21_22_human_send_btn",
                use_container_width=True,
            )

            if send_clicked_21_22:
                if not contact_info_21_22.strip() or not human_question_21_22.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    st.session_state["pa21_22_human_realtor_request"] = {
                        "contact": contact_info_21_22.strip(),
                        "question": human_question_21_22.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )

    st.markdown("---")

    # --------------------------------------------------
    # Section 21 – Remedies for Buyer & Seller
    # --------------------------------------------------
    st.markdown("### Section 21 – Remedies if Someone Breaches the Contract")

    st.markdown(
        "- This section is about **what can happen if the buyer or seller fails to perform** "
        "their obligations under the contract.\n"
        "- It usually references **liquidated damages** (often tied to the buyer’s deposit) and, "
        "for a seller breach, the possibility of **specific performance** (a court ordering the "
        "seller to complete the sale).\n"
        "- It does **not automatically decide every outcome**, but sets the framework for what "
        "types of remedies may be available."
    )

    with st.expander("📄 More about remedies & liquidated damages (Section 21)", expanded=False):
        st.markdown(
            "**1. Buyer breach:**\n"
            "- If a buyer **defaults** after removing contingencies (for example, refuses to close "
            "without a valid contractual excuse), the seller may be entitled to **damages**.\n"
            "- When both buyer and seller initial the **liquidated damages** clause (on the separate "
            "initial lines), they are generally agreeing that the buyer’s deposit (up to certain "
            "legal limits) may be the agreed amount of damages.\n"
            "- This is subject to state law and is something you should discuss with your own attorney.\n\n"
            "**2. Seller breach:**\n"
            "- If a seller refuses to complete the sale without a valid contractual reason, a buyer "
            "may seek **specific performance** (asking a court to order the seller to go through with "
            "the sale) or damages.\n\n"
            "**3. Important notes:**\n"
            "- This section does **not automatically mean** you will win or lose a specific amount; "
            "actual outcomes depend on facts, law, and often negotiation or legal action.\n"
            "- These clauses can have serious consequences. It’s wise to review them with your own attorney "
            "before signing."
        )

    st.markdown("---")

    # --------------------------------------------------
    # Section 22 – Mediation & Arbitration
    # --------------------------------------------------
    st.markdown("### Section 22 – Mediation & Arbitration (Dispute Resolution)")

    st.markdown(
        "- This section explains **how disputes are supposed to be handled** if there is a disagreement "
        "over the contract.\n"
        "- It emphasizes **mediation** (a structured negotiation with a neutral third party) and may also "
        "include an option for **binding arbitration** if both parties initial that part.\n"
        "- These choices affect **whether you can go to court and whether you have a right to a jury trial**."
    )

    with st.expander("📄 More about mediation (Section 22)", expanded=False):
        st.markdown(
            "- Mediation is a process where a neutral mediator helps the parties try to reach a **settlement**.\n"
            "- The contract typically requires parties to **attempt mediation before filing a lawsuit or "
            "arbitration**, except in limited situations.\n"
            "- If a party refuses to mediate when required, they may **lose certain rights to recover attorney’s "
            "fees**, even if they later win in court or arbitration.\n"
        )

    with st.expander("📄 More about arbitration (Section 22)", expanded=False):
        st.markdown(
            "- Arbitration is an **alternative to going to court**. A neutral arbitrator (or panel) hears the case "
            "and makes a **binding decision**.\n"
            "- If both buyer and seller initial the **arbitration** provision, they may be agreeing to **give up "
            "the right to a jury trial** for disputes covered by that clause.\n"
            "- Arbitration can sometimes be faster or more private than court, but it is also often **final** with "
            "limited rights to appeal.\n"
            "- Whether to initial the arbitration clause is a **serious legal decision**. You should discuss it "
            "with your own attorney; this app cannot tell you what choice is best for you."
        )

    st.markdown("---")

    # --------------------------------------------------
    # User notes & reflections (non-binding)
    # --------------------------------------------------
    st.markdown("### Your notes & questions about remedies and dispute resolution (optional)")

    st.markdown(
        "You usually **don’t rewrite** Sections 21–22 in a standard form contract. "
        "But it can be helpful to record how you feel about these provisions or what you want to "
        "ask a professional before signing."
    )

    col_notes_1, col_notes_2 = st.columns(2)

    with col_notes_1:
        comfort_level_liquidated = st.selectbox(
            "How do you feel about the idea that your deposit may be at risk if you breach?",
            options=[
                "I need to talk to an attorney before signing",
                "I understand the general idea but still have questions",
                "I feel reasonably comfortable with the concept",
            ],
            key="pa21_liquidated_comfort",
        )

    with col_notes_2:
        comfort_level_arbitration = st.selectbox(
            "How do you feel about arbitration instead of a court/jury trial?",
            options=[
                "I need to talk to an attorney before deciding",
                "I have mixed feelings / I'm not sure",
                "I feel generally comfortable with arbitration",
            ],
            key="pa22_arbitration_comfort",
        )

    user_notes_21_22 = st.text_area(
        "Any notes, concerns, or questions you want to remember about remedies or dispute resolution?",
        key="pa21_22_user_notes",
        height=140,
        placeholder=(
            "Examples:\n"
            "- Ask attorney to explain what happens to my deposit under liquidated damages.\n"
            "- Discuss with my agent whether mediation is commonly used in my area.\n"
            "- Get legal advice on pros/cons of signing the arbitration clause."
        ),
    )

    st.info(
        "These notes are **just for you and your agent** and do not change the legal language of the contract. "
        "For actual legal guidance, please consult your own attorney."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Bottom navigation – Save / Next
    # --------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Sections 21–22", key="pa21_22_save"):
            # Hook this into your persistence logic (DB or session)
            st.success(
                "Sections 21–22 notes saved (connect this button to your actual save logic)."
            )

    with col_right:
        if st.button("Next: Remaining General Terms / Signatures", key="pa21_22_next"):
            # If you are using an active_pa_tab index, set it here (adjust to your nav)
            # Example:
            # st.session_state['active_pa_tab'] = 13  # whatever index corresponds to next section
            st.info("Moving to the remaining general terms and signatures…")
