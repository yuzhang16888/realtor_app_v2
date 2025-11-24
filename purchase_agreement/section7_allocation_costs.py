import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai


def render_section7_allocation_costs():
    """
    Render Section 7 – Allocation of Costs.
    All Streamlit calls stay inside this function.
    """

    st.markdown("## Section 7 – Allocation of Costs")

    # ---------------------------
    # 🔹 GPT / AI Realtor – at the top of Section 7
    # ---------------------------
    with st.expander("💬 Need help with Section 7? Ask AI Realtor", expanded=True):
        st.markdown(
            "Use this assistant to understand typical cost allocations in California "
            "(for example: who usually pays escrow fees, title insurance, HOA docs, etc.).\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        default_prompt = (
            "You are an experienced California residential real estate agent. "
            "Help the buyer understand how to complete Section 7 – Allocation of Costs "
            "in the CAR Residential Purchase Agreement. Explain typical local norms, "
            "but always remind them that practices vary by area and are negotiable."
        )

        user_prompt = st.text_area(
            "What do you want help with in Section 7?",
            key="pa7_ai_prompt",
            height=120,
            placeholder=(
                "Example: I'm not sure who usually pays for escrow fees and the "
                "owner's title policy in San Francisco. Can you explain common options "
                "and what’s typical in the Bay Area?"
            ),
        )

        col_ai1, col_ai2 = st.columns([3, 1])
        with col_ai1:
            use_context = st.checkbox(
                "Include default Section 7 context in my question",
                value=True,
                key="pa7_ai_use_context",
            )
        with col_ai2:
            ask_clicked = st.button(
                "Ask AI Realtor about Section 7",
                key="pa7_ai_button",
                use_container_width=True,
            )

        # When button is clicked
        if ask_clicked:
            # Debug marker so we can see that the click is working
            st.write("🛠️ Debug: Ask AI button was clicked.")

            if not user_prompt.strip():
                st.warning("Please enter a question or description first.")
            else:
                full_prompt = user_prompt.strip()
                if use_context:
                    full_prompt = default_prompt + "\n\nUser question:\n" + user_prompt.strip()

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer = call_purchase_agreement_ai(full_prompt, section="7")
                    except Exception as e:
                        answer = (
                            "There was an error calling the AI backend for Section 7.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa7_ai_answer"] = answer

        # Always show the latest answer if we have one
        if "pa7_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa7_ai_answer"])

    st.markdown("---")

    # ---------------------------
    # 7A. Inspections, Reports and Certificates
    # ---------------------------
    st.markdown("### 7A. Inspections, Reports and Certificates")

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
    st.markdown("### 7B. Escrow and Title")

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
    st.markdown("### 7C. HOA / Community Association Fees and Documents")

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
  
    st.markdown("### 7D. Other Costs – Transfer Taxes & Fees")

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

    st.success("Section 7 – Allocation of Costs saved in session. Continue when you’re ready.")
