# purchase_agreement/section23_30_overview.py

import streamlit as st

# Try to import the shared AI helper; fall back gracefully if not available
try:
    from purchase_agreement.ai_helpers import call_purchase_agreement_ai
except Exception:
    def call_purchase_agreement_ai(prompt, section=None):
        """
        Fallback stub so this module still imports even if ai_helpers is missing.
        """
        return (
            "AI helper backend is not available right now. "
            "Please check your configuration or try again later."
        )


def render_section23_30_overview():
    """
    Combined view for Sections 23–30 of the CAR Residential Purchase Agreement.

    These are mostly 'general terms' and knowledge sections:
    - Assignment / who can step into the contract
    - Equal housing / fair housing language
    - Attorney’s fees, governing law, and notices
    - Additional terms, addenda, and counter-offers
    - Broker compensation, agency relationships, and other confirmations
    - Miscellaneous boilerplate that matters but usually isn’t edited by buyers
    """

    st.markdown("## Sections 23–30 – General Terms, Brokers & Other Legal Details")

    # --------------------------------------------------
    # 💬 GPT / AI Realtor + Human Realtor – Top Helper
    # --------------------------------------------------
    with st.expander("💬 Need help with Sections 23–30? Ask AI Realtor", expanded=True):
        st.markdown(
            "These sections cover **general legal terms, broker relationships, and other fine print** "
            "that support the rest of the contract.\n\n"
            "**Reminder:** This is information only and not legal advice. Always confirm with your own "
            "broker or attorney if you have questions about these clauses."
        )

        default_prompt_2330 = (
            "You are an experienced California residential real estate agent. "
            "Explain, in simple language, the typical topics covered in Sections 23–30 of the CAR "
            "Residential Purchase Agreement. At a high level, cover:\n"
            "- General terms like assignment, successors, and notices.\n"
            "- Equal housing / fair housing language.\n"
            "- Attorney’s fees and governing law.\n"
            "- Additional terms and addenda.\n"
            "- Broker compensation and confirmation of agency relationships.\n"
            "- Why these sections matter even though buyers usually don't edit them directly.\n"
            "Do not give legal advice. Stay neutral and remind the user to consult their own attorney "
            "for legal interpretation or custom changes."
        )

        with st.form("pa23_30_ai_form"):
            user_prompt_2330 = st.text_input(
                "What do you want help with in Sections 23–30?",
                key="pa23_30_ai_prompt",
                placeholder=(
                    "Examples:\n"
                    "• What does it mean if the contract says it can be assigned?\n"
                    "• What are 'additional terms' vs. counter-offers and addenda?\n"
                    "• How are brokers paid and what is their role in this contract?\n"
                    "• What is the attorney’s fees clause really saying?"
                ),
            )

            col_ai1, col_ai2 = st.columns([3, 2])

            with col_ai1:
                use_context_2330 = st.checkbox(
                    "Include default Sections 23–30 context in my question",
                    value=True,
                    key="pa23_30_ai_use_context",
                )

            with col_ai2:
                ask_clicked_2330 = st.form_submit_button(
                    "Ask AI Realtor",
                    use_container_width=True,
                )
                connect_clicked_2330 = st.form_submit_button(
                    "Connect with a Human Realtor",
                    use_container_width=True,
                )

        # Handle Ask AI
        if ask_clicked_2330:
            if not user_prompt_2330.strip():
                st.warning("Please enter a question or description first.")
            else:
                full_prompt_2330 = user_prompt_2330.strip()
                if use_context_2330:
                    full_prompt_2330 = (
                        default_prompt_2330
                        + "\n\nUser question:\n"
                        + user_prompt_2330.strip()
                    )

                with st.spinner("Thinking like a California Realtor..."):
                    answer_2330 = call_purchase_agreement_ai(
                        full_prompt_2330,
                        section="23-30",
                    )
                    st.session_state["pa23_30_ai_answer"] = answer_2330

        # Show AI answer
        if "pa23_30_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa23_30_ai_answer"])

        # Handle Connect with Human Realtor
        if connect_clicked_2330:
            st.session_state["pa23_30_show_human_realtor_form"] = True

        if st.session_state.get("pa23_30_show_human_realtor_form", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info_2330 = st.text_input(
                "Your preferred phone or email",
                key="pa23_30_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )

            human_question_2330 = st.text_area(
                "What would you like to ask a human?",
                key="pa23_30_human_question",
                height=100,
                placeholder=(
                    "Example: Can you explain how broker compensation and agency confirmation work "
                    "for my specific situation?"
                ),
            )

            send_clicked_2330 = st.button(
                "Send my question to a Human Realtor",
                key="pa23_30_human_send_btn",
                use_container_width=True,
            )

            if send_clicked_2330:
                if not contact_info_2330.strip() or not human_question_2330.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    st.session_state["pa23_30_human_realtor_request"] = {
                        "contact": contact_info_2330.strip(),
                        "question": human_question_2330.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )

    st.markdown("---")

    # --------------------------------------------------
    # Quick overview text
    # --------------------------------------------------
    st.markdown("### Quick overview of Sections 23–30")

    st.markdown(
        "These sections act like the **fine print that supports everything else** in your offer:\n"
        "- They describe how the contract can be assigned, who is bound by it, and how notices must be given.\n"
        "- They confirm fair housing principles and other legal protections.\n"
        "- They explain what happens with **attorney’s fees** if there is a dispute.\n"
        "- They confirm the role and compensation of brokers, and agency relationships.\n"
        "- They provide space for **additional terms** and cross-reference addenda or counter-offers.\n\n"
        "Most buyers do **not** rewrite these sections, but it’s still important to understand what they say."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Clustered summaries with expanders / placeholders
    # --------------------------------------------------

    # 23–24: Assignment / Successors / Notices / Equal Housing
    st.markdown("#### Sections 23–24 – Assignment, Successors & Equal Housing")

    st.markdown(
        "- Explain **who can step into the buyer or seller’s shoes** (assignment), "
        "and that the contract is binding on **heirs, successors, and assigns**.\n"
        "- Describe how **formal notices** (like cancellation or important communications) "
        "should be delivered (for example, in writing, to certain addresses or emails).\n"
        "- Include **fair housing / equal opportunity language**, confirming compliance with "
        "federal and state anti-discrimination laws."
    )

    with st.expander("📄 Click to view more about Sections 23–24 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for the actual RPA wording or a more detailed explanation of "
            "assignment, successors, notices, and equal housing. You can paste or link content here later._"
        )

    st.markdown("---")

    # 25–26: Attorney’s Fees, Governing Law, Additional Terms
    st.markdown("#### Sections 25–26 – Attorney’s Fees, Governing Law & Additional Terms")

    st.markdown(
        "- Explain **attorney’s fees**: typically, the prevailing party in certain disputes may "
        "be entitled to recover reasonable attorney’s fees and costs, subject to mediation rules.\n"
        "- Identify the **governing law** (usually California) for interpreting the contract.\n"
        "- Provide a space for **additional terms** that do not fit neatly into other sections—"
        "for example, custom agreements or clarifications negotiated between buyer and seller."
    )

    with st.expander("📄 Click to view more about Sections 25–26 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for full or partial contract text about attorney’s fees, governing law, "
            "and additional terms. You can replace this with more precise language or links later._"
        )

    st.markdown("---")

    # 27–28: Addenda, Counter-Offers, Integrated Agreement
    st.markdown("#### Sections 27–28 – Addenda, Counter-Offers & Entire Agreement")

    st.markdown(
        "- Clarify how **addenda, counter-offers, and other attached forms** become part of the contract.\n"
        "- Often include an **“entire agreement”** clause stating that the written contract (plus listed "
        "addenda) is the full agreement between the parties, superseding prior verbal discussions.\n"
        "- This means side conversations that are **not written into the contract** may not be enforceable."
    )

    with st.expander("📄 Click to view more about Sections 27–28 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for the full wording about addenda, counter-offers, and entire agreement. "
            "You can paste exact RPA language or a more detailed breakdown here in the future._"
        )

    st.markdown("---")

    # 29–30: Brokers, Agency Confirmation, Misc. Broker Terms
    st.markdown("#### Sections 29–30 – Brokers, Agency & Compensation")

    st.markdown(
        "- Confirm the identity of the **buyer’s broker** and the **seller’s broker**.\n"
        "- Confirm **agency relationships** (for example, whether a broker represents only one side "
        "or is acting as a dual agent, if allowed).\n"
        "- Reference how **broker compensation** is handled (usually via separate listing or compensation "
        "agreements) and clarify that brokers are not parties to certain promises in the contract.\n"
        "- These sections are important for transparency about **who represents whom**."
    )

    with st.expander("📄 Click to view more about Sections 29–30 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for the detailed broker / agency / compensation language from the contract. "
            "You can later embed specific RPA snippets or custom brokerage explanations here._"
        )

    st.markdown("---")

    # --------------------------------------------------
    # Optional user notes
    # --------------------------------------------------
    st.markdown("### Your notes about these general terms (optional)")

    st.text_area(
        "Any notes or questions you want to remember about general terms, brokers, or addenda?",
        key="pa23_30_user_notes",
        height=140,
        placeholder=(
            "Examples:\n"
            "- Confirm with my agent if there are any important addenda I should review in detail.\n"
            "- Ask how dual agency works if the same brokerage represents both sides.\n"
            "- Make sure any verbal promises are actually written into 'additional terms' or an addendum."
        ),
    )

    st.info(
        "These notes are just for your clarity or for discussion with your agent. "
        "They do **not** change the legal contract language by themselves."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Bottom navigation – Save / Next
    # --------------------------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Sections 23–30", key="pa23_30_save"):
            # Hook this into your persistence logic (DB, file, etc.)
            st.success("Sections 23–30 notes saved (connect this button to your actual save logic).")

    with col_right:
        if st.button("Next: Section 31 – Expiration of Offer", key="pa23_30_next"):
            # If you are using an active_pa_tab index, set it here (adjust to your nav)
            # Example:
            # st.session_state['active_pa_tab'] = 14  # whatever index corresponds to Section 31 tab
            st.info("Moving to Section 31 – Expiration of Offer…")
