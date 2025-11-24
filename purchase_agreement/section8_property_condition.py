import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai


def render_section8_property_condition():
    """
    Section 8 – Property Condition & Repairs
    """

    st.markdown("## Section 8 – Property Condition & Repairs")

       # ---------------------------
    # 🔹 GPT / AI Realtor – at the top of Section 8
    # ---------------------------
    with st.expander("💬 Need help with Section 8? Ask AI Realtor", expanded=True):
        st.markdown(
            "Use this assistant to understand how \"as-is\" condition, repairs, and "
            "credits typically work in California purchase agreements.\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        default_prompt = (
            "You are an experienced California residential real estate agent. "
            "Help the buyer understand how to complete Section 8 – Property Condition & Repairs "
            "in the CAR Residential Purchase Agreement. Explain typical norms for 'as-is' sales, "
            "seller repairs, credits in lieu of repairs, and home warranties. "
            "Always remind them that everything is negotiable and practices vary by area."
        )

        # Use a form so pressing Enter in the text input will submit (Ask AI)
        with st.form("pa8_ai_form"):
            user_prompt = st.text_input(
                "What do you want help with in Section 8?",
                key="pa8_ai_prompt",
                placeholder=(
                    "Example: What does it really mean when the property is sold 'as-is' in California? "
                    "Can I still ask for repairs after inspections?"
                ),
            )

            col_ai1, col_ai2 = st.columns([3, 2])
            with col_ai1:
                use_context = st.checkbox(
                    "Include default Section 8 context in my question",
                    value=True,
                    key="pa8_ai_use_context",
                )
            with col_ai2:
                ask_clicked = st.form_submit_button(
                    "Ask AI Realtor about Section 8",
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
                full_prompt = user_prompt.strip()
                if use_context:
                    full_prompt = default_prompt + "\n\nUser question:\n" + user_prompt.strip()

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        answer = call_purchase_agreement_ai(full_prompt, section="8")
                    except Exception as e:
                        answer = (
                            "There was an error calling the AI backend for Section 8.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa8_ai_answer"] = answer

        # Handle Connect with Human Realtor
        if connect_clicked:
            st.session_state["pa8_show_human_realtor_form"] = True

        # Show AI answer if we have one
        if "pa8_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion")
            st.info(st.session_state["pa8_ai_answer"])

        # Show the human-realtor contact form if toggled on
        if st.session_state.get("pa8_show_human_realtor_form", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info = st.text_input(
                "Your preferred phone or email",
                key="pa8_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )
            human_question = st.text_area(
                "What would you like to ask a human?",
                key="pa8_human_question",
                height=100,
                placeholder="Share your questions or situation so a human realtor can follow up.",
            )

            send_clicked = st.button(
                "Send my question to a Human Realtor",
                key="pa8_human_send_btn",
                use_container_width=True,
            )

            if send_clicked:
                if not contact_info.strip() or not human_question.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    # Here is where you would integrate an email, database, or CRM.
                    # For now, we just store it in session_state.
                    st.session_state["pa8_human_realtor_request"] = {
                        "contact": contact_info.strip(),
                        "question": human_question.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )




    # ---------------------------
    # 8A. Property Condition / “As-Is”
    # ---------------------------
    st.markdown("### 8A. Property Condition / “As-Is”")

    st.write(
        "Clarify whether the property is being sold in its present physical condition "
        "subject to buyer’s inspection rights, or if the seller is agreeing to specific "
        "condition-related obligations."
    )

    col_8a_1, col_8a_2 = st.columns(2)

    with col_8a_1:
        st.checkbox(
            "Property is sold in its present physical condition ('as-is'), "
            "subject to buyer's inspection and investigation rights.",
            key="pa8a_as_is_checkbox",
            value=True,
        )

        st.text_area(
            "Any exceptions or special condition agreements (optional)",
            key="pa8a_exceptions",
            height=80,
            placeholder="Example: Roof to be free of active leaks; pool equipment to be in working order.",
        )

    with col_8a_2:
        st.text_area(
            "Buyer’s key concerns about property condition (optional)",
            key="pa8a_buyer_condition_concerns",
            height=80,
            placeholder="Example: foundation movement, past water intrusion, unpermitted work.",
        )

    st.markdown("---")

    # ---------------------------
    # 8B. Seller Repair Obligations (Before Close of Escrow)
    # ---------------------------
    st.markdown("### 8B. Seller Repair Obligations (Before Close of Escrow)")

    st.write(
        "If the seller is agreeing up front to perform certain repairs or corrections "
        "before Close of Escrow, capture those here."
    )

    col_8b_1, col_8b_2 = st.columns(2)

    with col_8b_1:
        st.markdown("**Specific Repairs Seller Agrees to Complete**")
        st.text_area(
            "Repairs to be completed by Seller before Close of Escrow",
            key="pa8b_seller_repairs",
            height=100,
            placeholder="Example: Repair active leak under kitchen sink; service HVAC; replace broken window in bedroom.",
        )

    with col_8b_2:
        st.markdown("**Repair Cost Limits / Caps (if any)**")
        st.number_input(
            "Optional cap on Seller’s total repair costs (USD)",
            key="pa8b_repair_cap",
            min_value=0.0,
            step=500.0,
            format="%.0f",
            help="Leave as 0 if no specific cap is being agreed to.",
        )

        st.text_area(
            "Additional notes about repair standards and timing (optional)",
            key="pa8b_repair_notes",
            height=80,
            placeholder="Example: Repairs to be done by licensed contractors with receipts provided to Buyer.",
        )

    st.markdown("---")

    # ---------------------------
    # 8C. Credits in Lieu of Repairs
    # ---------------------------
    st.markdown("### 8C. Credits in Lieu of Repairs")

    st.write(
        "Sometimes, instead of the Seller doing work, the parties agree to a credit to "
        "Buyer at Close of Escrow in lieu of repairs."
    )

    col_8c_1, col_8c_2 = st.columns(2)

    with col_8c_1:
        st.markdown("**Buyer Credit Amount (if any)**")
        st.number_input(
            "Credit to Buyer at Close of Escrow (USD)",
            key="pa8c_credit_amount",
            min_value=0.0,
            step=500.0,
            format="%.0f",
            help="Enter 0 if not offering a credit instead of repairs.",
        )

    with col_8c_2:
        st.text_area(
            "Reason / scope covered by the credit",
            key="pa8c_credit_reason",
            height=80,
            placeholder="Example: Credit in lieu of Seller repairing roof and updating electrical panel.",
        )

    st.markdown("---")

    # ---------------------------
    # 8D. Home Warranty Plan
    # ---------------------------
    st.markdown("### 8D. Home Warranty Plan")

    st.write(
        "Indicate whether a home warranty plan will be provided, who pays for it, "
        "and any cost limit."
    )

    col_8d_1, col_8d_2 = st.columns(2)

    with col_8d_1:
        provide_warranty = st.radio(
            "Will a home warranty plan be provided?",
            options=["No", "Yes"],
            key="pa8d_warranty_provided",
            horizontal=True,
        )

        if provide_warranty == "Yes":
            st.radio(
                "Home warranty plan paid by:",
                options=["Buyer", "Seller", "Split", "Other"],
                key="pa8d_warranty_party",
                horizontal=True,
            )
            st.text_input(
                "If Split/Other, describe:",
                key="pa8d_warranty_other",
                placeholder="e.g., Seller pays first $600, remainder Buyer.",
            )

    with col_8d_2:
        if provide_warranty == "Yes":
            st.number_input(
                "Maximum cost for home warranty plan (USD)",
                key="pa8d_warranty_cap",
                min_value=0.0,
                step=100.0,
                format="%.0f",
                help="Enter 0 if there is no specific cost cap.",
            )
            st.text_input(
                "Preferred home warranty company (optional)",
                key="pa8d_warranty_company",
                placeholder="Example: First American, Old Republic, etc.",
            )
        else:
            st.text_area(
                "Notes about why no home warranty is being provided (optional)",
                key="pa8d_no_warranty_notes",
                height=80,
                placeholder="Example: Buyer prefers to choose and pay for their own coverage after closing.",
            )

    st.markdown("---")

    # ---------------------------
    # 8E. Other Property Condition Terms (Free-form)
    # ---------------------------
    st.markdown("### 8E. Other Property Condition Terms (Free-form)")

    st.write(
        "Use this area for any additional property condition or repair-related terms "
        "you want to capture for Section 8."
    )

    st.text_area(
        "Other specific terms or clarifications for Section 8",
        key="pa8_other_terms_freeform",
        height=120,
        placeholder="Example: Seller to complete city-required retrofit work prior to Close of Escrow. "
                    "Buyer acknowledges existing cosmetic wear consistent with age of property.",
    )

      # ---------------------------
    # Section Navigation Buttons (Same style as other sections)
    # ---------------------------
    st.markdown("### Save & Continue")

    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        if st.button("⬅️ Back to Section 7", key="pa7_back_btn", use_container_width=True):
            st.session_state.active_pa_tab = 6  # zero-index: section 6

    with col_next:
        if st.button("Save Section 8 & Continue ➡️", key="pa7_next_btn", use_container_width=True):
            st.session_state.active_pa_tab = 8  # zero-index: section 8
            st.success("Section 7 saved. Moving to Section 8…")

