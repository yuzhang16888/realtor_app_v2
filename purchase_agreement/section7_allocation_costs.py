import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai


def render_section7_allocation_costs():
    """
    Render Section 7 – Allocation of Costs.
    All Streamlit calls stay inside this function.
    """

    st.markdown("## Section 2 – Allocation of Costs")

        # ---------------------------
    # 🔹 GPT / AI Realtor – at the top of Section 7
    # ---------------------------
    with st.expander("💬 Need help with Section 7? Ask AI Realtor", expanded=True):
        st.markdown(
            "Use this assistant to understand typical cost allocations in California "
            "(for example: who usually pays escrow fees, title insurance, HOA docs, etc.).\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        # Use a form so pressing Enter inside the text input will submit (Ask AI)
        with st.form("pa7_ai_form"):
            user_prompt = st.text_input(
                "What do you want help with in allocation of costs?",
                key="pa7_ai_prompt",
                placeholder=(
                    "Example: In San Francisco, who usually pays escrow fees and the "
                    "owner's title policy? How are county and city transfer taxes often split?"
                ),
            )

            ask_clicked = st.form_submit_button(
                "Ask AI Realtor about Section 7",
                use_container_width=True,
            )
            connect_clicked = st.form_submit_button(
                "Connect with a Human Realtor",
                use_container_width=True,
            )

        # Handle Ask AI (form submit or Enter)
        if ask_clicked:
            if not user_prompt.strip():
                st.warning("Please enter a question or description first.")
            else:
                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer = call_purchase_agreement_ai(
                            user_prompt.strip(),
                            section="7",
                            # if you have a Section 7 state dict and want to pass it:
                            # section_state=st.session_state[SECTION7_KEY],
                        )
                    except Exception as e:
                        answer = (
                            "There was an error calling the AI backend for Section 7.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa7_ai_answer"] = answer

        # Handle Connect with Human Realtor
        if connect_clicked:
            st.session_state["pa7_show_human_realtor_form"] = True

        # Show AI answer if we have one
        if "pa7_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa7_ai_answer"])

        # Show the human-realtor contact form if toggled on
        if st.session_state.get("pa7_show_human_realtor_form", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info = st.text_input(
                "Your preferred phone or email",
                key="pa7_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )
            human_question = st.text_area(
                "What would you like to ask a human?",
                key="pa7_human_question",
                height=100,
                placeholder="Share your questions or situation so a human realtor can follow up.",
            )

            send_clicked = st.button(
                "Send my question to a Human Realtor",
                key="pa7_human_send_btn",
                use_container_width=True,
            )

            if send_clicked:
                if not contact_info.strip() or not human_question.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    # Later you can integrate this with email, database, or CRM.
                    st.session_state["pa7_human_realtor_request"] = {
                        "contact": contact_info.strip(),
                        "question": human_question.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you "
                        "using the contact info you provided."
                    )

    st.markdown("---")

    # ---------------------------
    # 7A. Inspections, Reports and Certificates
    # ---------------------------
    st.markdown("### 2A. Inspections, Reports and Certificates")

    st.write(
        "Specify who will pay for general inspections, pest reports, and required "
        "local government reports/certificates (for example: water heater bracing, "
        "smoke/CO detector compliance, city point-of-sale inspections)."
    )

    col_7a_1, col_7a_2 = st.columns(2)

    with col_7a_1:
        st.markdown("**General Property Inspection**")
        st.radio(
            "Who pays?",
            options=["Buyer", "Seller", "Split", "Other"],
            key="pa7a_general_inspection_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7a_general_inspection_other",
            placeholder="e.g., 50/50 split; or Buyer up to $500, remainder Seller.",
        )

        st.markdown("**Wood Destroying Pest Inspection**")
        st.radio(
            "Who pays?",
            options=["Buyer", "Seller", "Split", "Other"],
            key="pa7a_pest_inspection_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7a_pest_inspection_other",
            placeholder="e.g., Seller up to $2,000, remainder Buyer.",
        )

    with col_7a_2:
        st.markdown("**Government-Required Reports/Certificates**")
        st.radio(
            "Who pays for required local reports/certificates?",
            options=["Buyer", "Seller", "Split", "Other"],
            key="pa7a_gov_reports_party",
            horizontal=True,
        )
        st.text_area(
            "Details / Notes",
            key="pa7a_gov_reports_notes",
            height=80,
            placeholder="e.g., Seller pays city sewer lateral inspection; Buyer pays re-inspection if repairs required.",
        )

    st.markdown("---")

    # ---------------------------
    # 7B. Escrow and Title
    # ---------------------------
    st.markdown("### 2B. Escrow and Title")

    st.write(
        "Allocate who pays escrow fees, owner’s title insurance policy, and lender’s "
        "title policy (if applicable). Practices vary by county."
    )

    col_7b_1, col_7b_2 = st.columns(2)

    with col_7b_1:
        st.markdown("**Escrow Fees**")
        st.radio(
            "Escrow fees paid by:",
            options=["Buyer", "Seller", "50/50", "Other"],
            key="pa7b_escrow_fees_party",
            horizontal=True,
        )
        st.text_input(
            "If Other, describe:",
            key="pa7b_escrow_fees_other",
            placeholder="e.g., Split 60/40 in favor of Buyer.",
        )

        st.markdown("**Owner’s Title Insurance Policy**")
        st.radio(
            "Owner’s title policy paid by:",
            options=["Buyer", "Seller", "Split", "Other"],
            key="pa7b_owner_title_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7b_owner_title_other",
            placeholder="e.g., Seller pays CLTA policy; Buyer pays extended coverage.",
        )

    with col_7b_2:
        st.markdown("**Lender’s Title Policy (if any)**")
        st.radio(
            "Lender’s title policy paid by:",
            options=["Buyer", "Seller", "Split", "Other", "N/A – no loan"],
            key="pa7b_lender_title_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7b_lender_title_other",
            placeholder="e.g., Buyer pays lender’s title policy in full.",
        )

        st.text_area(
            "Additional Title/Escrow Notes (optional)",
            key="pa7b_additional_notes",
            height=80,
            placeholder="Any special title endorsements, escrow fee caps, or prorations you want to note.",
        )

    st.markdown("---")

    # ---------------------------
    # 7C. HOA / Community Association Fees and Documents
    # ---------------------------
    st.markdown("### 2C. HOA / Community Association Fees and Documents")

    st.write(
        "If the property is in a common interest development, specify who pays "
        "for HOA transfer fees, document packages, and move-in/move-out fees."
    )

    col_7c_1, col_7c_2 = st.columns(2)

    with col_7c_1:
        st.markdown("**HOA Transfer Fee**")
        st.radio(
            "HOA transfer fee paid by:",
            options=["Buyer", "Seller", "Split", "Other", "N/A – no HOA"],
            key="pa7c_transfer_fee_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7c_transfer_fee_other",
            placeholder="e.g., Split 50/50 between Buyer and Seller.",
        )

        st.markdown("**HOA Move-In / Move-Out Fees**")
        st.radio(
            "Move-in / move-out fees paid by:",
            options=["Buyer", "Seller", "Split", "Other", "N/A"],
            key="pa7c_move_fees_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7c_move_fees_other",
            placeholder="e.g., Buyer pays move-in, Seller pays move-out.",
        )

    with col_7c_2:
        st.markdown("**HOA Document Package**")
        st.radio(
            "HOA docs (CC&Rs, bylaws, budget, etc.) paid by:",
            options=["Buyer", "Seller", "Split", "Other", "N/A – no HOA"],
            key="pa7c_docs_party",
            horizontal=True,
        )
        st.text_area(
            "HOA-related Notes (optional)",
            key="pa7c_notes",
            height=80,
            placeholder="e.g., Seller to order HOA docs within 5 days of acceptance.",
        )

    st.markdown("---")

    # ---------------------------
    # 7D–7N. Other Costs (Free-form notes)
    # ---------------------------
  
    st.markdown("### 2D. Other Costs – Transfer Taxes & Fees")

    st.write(
        "Allocate who pays county and city transfer taxes/fees and any private transfer fee "
        "(for example: HOA or community transfer fee). Practices can vary by county and city."
    )

    col_7d_1, col_7d_2 = st.columns(2)

    # Left column: county + city transfer tax/fee
    with col_7d_1:
        st.markdown("**County Transfer Tax / Fee**")
        st.radio(
            "County transfer tax / fee paid by:",
            options=["Buyer", "Seller", "Split", "Other", "Not applicable"],
            key="pa7d_county_transfer_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7d_county_transfer_other",
            placeholder="e.g., Seller pays first $5,000; remainder Buyer.",
        )

        st.markdown("**City Transfer Tax / Fee**")
        st.radio(
            "City transfer tax / fee paid by:",
            options=["Buyer", "Seller", "Split", "Other", "Not applicable"],
            key="pa7d_city_transfer_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7d_city_transfer_other",
            placeholder="e.g., Buyer and Seller split 50/50.",
        )

    # Right column: private transfer fee + notes
    with col_7d_2:
        st.markdown("**Private Transfer Fee**")
        st.radio(
            "Private transfer fee paid by:",
            options=["Buyer", "Seller", "Split", "Other", "Not applicable"],
            key="pa7d_private_transfer_party",
            horizontal=True,
        )
        st.text_input(
            "If Split/Other, describe:",
            key="pa7d_private_transfer_other",
            placeholder="e.g., Buyer pays HOA private transfer fee in full.",
        )

        st.text_area(
            "Other specific cost allocations or notes for Section 7D (optional)",
            key="pa7d_other_notes",
            height=100,
            placeholder="Example: Seller to pay county transfer tax; Buyer to pay city transfer tax. "
                        "Any special city/HOA rules about transfer fees.",
        )

    # ---------------------------
    # Section Navigation Buttons (Same style as other sections)
    # ---------------------------
    st.markdown("### Save & Continue")

    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        if st.button("⬅️ Back to Section 1", key="pa7_back_btn", use_container_width=True):
            st.session_state.active_pa_tab = 1  # zero-index: section 6

    with col_next:
        if st.button("Save Section 2 & Continue ➡️", key="pa7_next_btn", use_container_width=True):
            st.session_state.active_pa_tab = 7  # zero-index: section 8
            st.success("Section 2 saved. Moving to Section 8…")

