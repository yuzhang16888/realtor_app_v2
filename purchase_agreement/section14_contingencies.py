# purchase_agreement/section14_contingencies.py

import streamlit as st

# IMPORTANT: adjust this import to match how you did it in Section 8 / Section 9
# Example (if this is what Section 8 uses):
# from purchase_agreement.ai_helpers import call_purchase_agreement_ai
from purchase_agreement.ai_helpers import call_purchase_agreement_ai


def render_section14_contingencies():
    """
    Render Section 14 – Contingencies; Removal of Contingencies; Cancellation Rights.

    UX decisions:
    - At the top: AI helper with quick default options + custom question.
    - User only fills 14B(1) (time to remove buyer contingencies).
    - 14B(2), 14B(3), 14B(4) are explained in layman's terms and shown in tables,
      instead of asking the user to tweak legal language.
    """

    st.markdown("## 14. Contingencies, Removal of Contingencies, and Cancellation Rights")

    # ---------------------------
    # 💬 GPT / AI Realtor – Section 14 Helper
    # ---------------------------
    with st.expander("💬 Ask AI Realtor about Section 14 – Contingencies & Cancellation", expanded=True):
        st.markdown(
            "Use this helper to understand how contingency deadlines, notices, and cancellation "
            "rights work in Section 14.\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        default_prompt_14 = (
            "You are an experienced California residential real estate agent. "
            "Help the buyer understand Section 14 of the CAR Residential Purchase Agreement, "
            "especially Section 14.B(1), 14.B(2), 14.B(3), and 14.B(4). Explain:\n"
            "- what each part means in plain language,\n"
            "- what happens if the buyer or seller does not perform,\n"
            "- how the 48-hour 'Notice to Perform' works, and\n"
            "- how contingency deadlines are affected when the seller is late delivering disclosures.\n"
            "Give clear, practical explanations and remind them that timelines and practices may vary by area."
        )

        # -------------------------
        # Quick choices
        # -------------------------
        st.markdown("**Quick options:**")

        col_q1, col_q2 = st.columns(2)
        with col_q1:
            show_contract_clicked = st.button(
                "📄 Show me the contract details",
                key="pa14_show_contract_details",
                use_container_width=True,
            )
        with col_q2:
            show_timeline_clicked = st.button(
                "📊 Who does what by when?",
                key="pa14_show_timeline",
                use_container_width=True,
            )

        # Handle "Show me the contract details" via AI
        if show_contract_clicked:
            full_prompt_14_contract = (
                default_prompt_14
                + "\n\nUser question:\n"
                "Please walk me through the meaning of Section 14.B(1), 14.B(2), 14.B(3), "
                "and 14.B(4) in plain English. Focus on what contingencies are, when they must "
                "be removed, when the seller can cancel, when the buyer can cancel, and how "
                "the 48-hour 'Notice to Perform' works."
            )
            with st.spinner("Thinking like a California Realtor..."):
                try:
                    answer_14_contract = call_purchase_agreement_ai(
                        full_prompt_14_contract,
                        section="14",
                    )
                except Exception as e:
                    answer_14_contract = (
                        "There was an error calling the AI backend for Section 14.\n\n"
                        f"Details: {e}"
                    )
                st.session_state["pa14_ai_answer"] = answer_14_contract

        # Handle "Who does what by when?" – show static tables
        if show_timeline_clicked:
            st.markdown("#### 📊 What needs to be done, by whom, and by when")

            st.markdown("**14.B(2) – Seller’s right to cancel if buyer does nothing**")
            st.markdown(
                "| Party | Responsibility | When |\n"
                "|-------|----------------|------|\n"
                "| **Buyer** | Remove contingencies or cancel | Before the contingency period expires |\n"
                "| **Seller** | May issue a *Notice to Buyer to Perform* | After buyer fails to act by the deadline |\n"
                "| **Buyer** | Must perform (remove or cancel) after notice | Within 48 hours after receiving the notice |\n"
                "| **Seller** | May cancel the contract | If buyer still does nothing after the 48 hours |\n"
            )

            st.markdown("**14.B(3) – Seller delays that affect buyer’s deadlines**")
            st.markdown(
                "| Party | Responsibility | Effect on deadlines |\n"
                "|-------|----------------|---------------------|\n"
                "| **Seller** | Provide required disclosures, access, or repairs | Within the agreed time (e.g., 7 days) |\n"
                "| **Buyer** | Gets extended contingency periods if seller is late | Deadlines may be extended until seller has completed their part |\n"
                "| **Seller** | Must complete their tasks before expecting buyer to remove contingencies | Buyer’s practical countdown starts after seller performs |\n"
            )

            st.markdown("**14.B(4) – Buyer’s right to cancel if seller doesn’t perform**")
            st.markdown(
                "| Party | Responsibility | When |\n"
                "|-------|----------------|------|\n"
                "| **Seller** | Deliver disclosures, allow access, complete agreed repairs, sign required papers | By the agreed timelines in the contract |\n"
                "| **Buyer** | May issue a *Notice to Seller to Perform* | If seller fails to perform on time |\n"
                "| **Seller** | Must perform after receiving the notice | Within 48 hours after receiving the notice |\n"
                "| **Buyer** | May cancel the contract | If seller still has not performed after the 48 hours |\n"
            )

        # -------------------------
        # Custom AI question
        # -------------------------
        st.markdown("---")
        st.markdown("**Or ask your own question about Section 14:**")

        with st.form("pa14_ai_form"):
            user_prompt_14 = st.text_input(
                "What do you want help with in Section 14?",
                key="pa14_ai_prompt",
                placeholder=(
                    "Example: What happens if I miss my contingency deadline?\n"
                    "Example: Can I still cancel if the seller is late with disclosures?\n"
                    "Example: What exactly is a 'Notice to Perform'?"
                ),
            )

            col_ai1, col_ai2 = st.columns([3, 2])
            with col_ai1:
                use_context_14 = st.checkbox(
                    "Include default Section 14 context in my question",
                    value=True,
                    key="pa14_ai_use_context",
                )
            with col_ai2:
                ask_clicked_14 = st.form_submit_button(
                    "Ask AI Realtor about Section 14",
                    use_container_width=True,
                )

        if ask_clicked_14:
            if not user_prompt_14.strip():
                st.warning("Please enter a question or description first.")
            else:
                full_prompt_14 = user_prompt_14.strip()
                if use_context_14:
                    full_prompt_14 = (
                        default_prompt_14
                        + "\n\nUser question:\n"
                        + user_prompt_14.strip()
                    )

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer_14 = call_purchase_agreement_ai(
                            full_prompt_14,
                            section="14",
                        )
                    except Exception as e:
                        answer_14 = (
                            "There was an error calling the AI backend for Section 14.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa14_ai_answer"] = answer_14

        # Show AI answer if we have one
        if "pa14_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion (Section 14)")
            st.info(st.session_state["pa14_ai_answer"])

    st.markdown("---")

    # ---------------------------
    # Short plain-English summary
    # ---------------------------
    st.markdown("### What Section 14 is about (plain English)")

    st.markdown(
        "- Section 14 is where the contract explains **contingencies** — "
        "things that must happen, or information you must approve, before you are fully locked in.\n"
        "- It also explains **how and when contingencies must be removed**, and "
        "**what happens if either side fails to perform**.\n"
        "- This app lets you set the time for your **buyer contingencies in 14.B(1)** "
        "and then explains 14.B(2), 14.B(3), and 14.B(4) in plain language so you "
        "understand your rights and risks."
    )

    st.markdown("---")

    # ---------------------------
    # 14B(1) – Time to remove buyer contingencies (user input)
    # ---------------------------
    st.markdown("### 14B(1). Time to Remove Buyer Contingencies")

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
    st.markdown("### 14B(2)–(4). What happens if someone doesn’t perform?")

    with st.expander("📄 14B(2) – Seller’s right to cancel if buyer does nothing", expanded=False):
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

    with st.expander("📄 14B(3) – Seller delays that affect buyer’s deadlines", expanded=False):
        st.markdown(
            "- If the seller is late delivering required disclosures, reports, or access, "
            "your contingency deadlines can be **extended**.\n"
            "- You are not expected to remove contingencies based on information that the "
            "seller has not yet provided.\n"
        )

        st.markdown("**Who must do what, and how it affects deadlines:**")
        st.markdown(
            "| Party | Responsibility | Effect on deadlines |\n"
            "|-------|----------------|---------------------|\n"
            "| **Seller** | Provide required disclosures, access, or repairs | Within the agreed time (e.g., 7 days) |\n"
            "| **Buyer** | Gets extended contingency periods if seller is late | Deadlines may be extended until seller has completed their part |\n"
            "| **Seller** | Must complete tasks before expecting buyer to remove contingencies | Buyer’s practical countdown starts after seller performs |\n"
        )

    with st.expander("📄 14B(4) – Buyer’s right to cancel if seller doesn’t perform", expanded=False):
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
        if st.button("💾 Save Section 14", key="pa14_save"):
            # Hook this into your persistence logic (e.g., save to DB or session)
            st.success("Section 14 responses saved (connect this button to your save logic).")

    with col_right:
        if st.button("Next: Section 15", key="pa14_next"):
            # If you are using an active_pa_tab index, set it here (adjust index as needed)
            # st.session_state["active_pa_tab"] = SOME_INDEX_FOR_SECTION_15
            st.info("Moving to Section 15… (make sure this updates your main app navigation).")
