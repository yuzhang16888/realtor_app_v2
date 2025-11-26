# purchase_agreement/section10_13_overview.py

import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai  # adjust path if needed


def render_section10_13_overview():
    """
    Overview hub for Sections 10–13:
    - Short summaries
    - AI helper for questions
    - Expanders to read full section content later
    """

    st.markdown("## Other Disclosures, Rules & Rights")

    # ---------------------------
    # 🔹 GPT / AI Realtor – overview for 10–13
    # ---------------------------
    with st.expander("💬 Need help? Ask AI Realtor", expanded=True):
        st.markdown(
            "Use this assistant to understand the big picture for disclosures, inspections, "
            "access, and what happens if someone breaches the agreement.\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        default_prompt_1013 = (
            "You are an experienced California residential real estate agent. "
            "Explain to a buyer how Sections 10–13 of the CAR Residential Purchase Agreement work:\n"
            "- Section 10: Statutory and contractual disclosures, including condo/HOA and planned development disclosures.\n"
            "- Section 11: Buyer investigation, inspections, and due diligence.\n"
            "- Section 12: Seller and agent access to the property during escrow.\n"
            "- Section 13: Remedies if buyer or seller breaches, including liquidated damages and specific performance.\n"
            "Give clear, practical explanations in plain language and remind them that timelines and practices can vary by area."
        )

        # Use a form so pressing Enter submits
        with st.form("pa_10_13_ai_form"):
            user_prompt_1013 = st.text_input(
                "What do you want help with ?",
                key="pa_10_13_ai_prompt",
                placeholder=(
                    "Example: What disclosures do I get if I'm buying a condo?\n"
                    "Example: What happens if I find something bad during inspections?\n"
                    "Example: When can the seller still come into the property before closing?\n"
                    "Example: Could I really lose my deposit if I back out?"
                ),
            )

            col_ai1, col_ai2 = st.columns([3, 2])
            with col_ai1:
                use_context_1013 = st.checkbox(
                    "Include default Sections 10–13 context in my question",
                    value=True,
                    key="pa_10_13_ai_use_context",
                )
            with col_ai2:
                ask_clicked_1013 = st.form_submit_button(
                    "Ask AI Realtor about Sections 10–13",
                    use_container_width=True,
                )
                connect_clicked_1013 = st.form_submit_button(
                    "Connect with a Human Realtor",
                    use_container_width=True,
                )

        # Handle Ask AI
        if ask_clicked_1013:
            if not user_prompt_1013.strip():
                st.warning("Please enter a question or description first.")
            else:
                full_prompt_1013 = user_prompt_1013.strip()
                if use_context_1013:
                    full_prompt_1013 = (
                        default_prompt_1013
                        + "\n\nUser question:\n"
                        + user_prompt_1013.strip()
                    )

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer_1013 = call_purchase_agreement_ai(
                            full_prompt_1013, section="10-13"
                        )
                    except Exception as e:
                        answer_1013 = (
                            "There was an error calling the AI backend for Sections 10–13.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa_10_13_ai_answer"] = answer_1013

        # Handle Connect with Human Realtor
        if connect_clicked_1013:
            st.session_state["pa_10_13_show_human_realtor_form"] = True

        # Show AI answer if we have one
        if "pa_10_13_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion (Sections 10–13)")
            st.info(st.session_state["pa_10_13_ai_answer"])

        # Show human-realtor contact form if toggled on
        if st.session_state.get("pa_10_13_show_human_realtor_form", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info_1013 = st.text_input(
                "Your preferred phone or email",
                key="pa_10_13_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )
            human_question_1013 = st.text_area(
                "What would you like to ask a human?",
                key="pa_10_13_human_question",
                height=100,
                placeholder="Share your questions or situation so a human realtor can follow up.",
            )

            send_clicked_1013 = st.button(
                "Send my question to a Human Realtor",
                key="pa_10_13_human_send_btn",
                use_container_width=True,
            )

            if send_clicked_1013:
                if not contact_info_1013.strip() or not human_question_1013.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    st.session_state["pa_10_13_human_realtor_request"] = {
                        "contact": contact_info_1013.strip(),
                        "question": human_question_1013.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )

    st.markdown("---")

    # ---------------------------
    # Section summaries + expanders
    # ---------------------------

    # Section 10
    st.markdown("### Statutory & Contractual Disclosures")

    st.markdown(
        "- This section covers **all the disclosures the seller must give you**.\n"
        "- Includes TDS, SPQ, NHD, safety items (smoke/CO detectors, water heater bracing), "
        "and various hazard, environmental, and local disclosures.\n"
        "- **If you are buying a condo or a home in an HOA/planned development**: "
        "Section 10 also covers the extra **HOA/condo disclosures** – CC&Rs, budget, "
        "reserves, meeting minutes, rules, etc.\n"
        "- It also explains your **right to review** disclosures and, in some cases, "
        "your **right to cancel** if they’re late or incomplete."
    )

    with st.expander("📄 Click to view full content", expanded=False):
        st.info(
            "Full Section 10 UI will go here.\n\n"
            "You can either:\n"
            "- Render the detailed Section 10 form in this expander, or\n"
            "- Call a separate function like `render_section10_disclosures()` once it's built."
        )
        # Example (later, once you have it):
        # render_section10_disclosures()

    st.markdown("---")

    # Section 11
    st.markdown("### Buyer Investigation, Inspections & Due Diligence")

    st.markdown(
        "- Confirms your **right to investigate the property**: condition, permits, "
        "systems, neighborhood, and more.\n"
        "- Covers typical inspections (home, pest, roof, sewer, etc.) and clarifies "
        "that you usually **pay for your own inspections** unless negotiated otherwise.\n"
        "- Reminds you that you must use care during inspections and repair any damage caused."
    )

    with st.expander("📄 Click to view full content", expanded=False):
        st.info(
            "Full Section 11 UI will go here.\n\n"
            "Later you can plug in a detailed inspections/due-diligence section here."
        )
        # Example later:
        # render_section11_investigations()

    st.markdown("---")

    # Section 12
    st.markdown("###  Seller Access to the Property")

    st.markdown(
        "- Explains when the **seller and their contractors can access the property** "
        "during escrow.\n"
        "- Typical reasons: appraisal, repairs, termite work, lender requirements, "
        "and other agreed work.\n"
        "- You must allow **reasonable access**, but the seller should give notice and "
        "use professional vendors."
    )

    with st.expander("📄 Click to view full content", expanded=False):
        st.info(
            "Full Section 12 UI will go here.\n\n"
            "You can later render your full Section 12 form or logic inside this expander."
        )
        # Example later:
        # render_section12_access()

    st.markdown("---")

    # Section 13
    st.markdown("###  Remedies for Breach (Buyer or Seller)")

    st.markdown(
        "- Covers **what happens if either side breaches** the contract.\n"
        "- For buyers, this often relates to **loss of the deposit** if liquidated damages "
        "are initialed and the buyer defaults.\n"
        "- For sellers, this may involve **specific performance** (being forced to sell) "
        "or damages if they refuse to perform.\n"
        "- Ties into mediation, arbitration, and attorney’s fees later in the RPA."
    )

    with st.expander("📄 Click to view full content", expanded=False):
        st.info(
            "Full Section 13 UI will go here.\n\n"
            "Later you can plug in a more detailed explanation of remedies, liquidated damages, "
            "and default scenarios."
        )
        # Example later:
        # render_section13_remedies()
