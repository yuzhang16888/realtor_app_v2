# purchase_agreement/section9_closing_possession.py

import streamlit as st


    

def render_section9_closing_possession():
    """
    Render Section 9 – Closing and Possession of the Purchase Agreement.
    All UI is contained inside this function so the module can be safely imported.
    """

    st.markdown("## 9. Closing and Possession")
    # -------------------------------
    # Ask AI + Connect with Human Realtor (Helper Block)
    # -------------------------------
    st.markdown("### Need help with Section 9 – Closing & Possession?")

    with st.expander("💬 Ask AI Realtor or Connect with a Human Realtor", expanded=False):
        st.markdown(
            "Use this helper if you’re unsure about closing timelines, rent-backs, or possession terms."
        )

        # AI question input
        ai_question = st.text_area(
            "Ask AI Realtor for Section 9",
            key="pa_9_ai_question",
            placeholder="Example: Is it better for me to close on a Friday or Monday? What are the pros and cons of allowing the seller to stay after closing?",
        )

        col_ai, col_human = st.columns(2)

        with col_ai:
            if st.button("Ask AI Realtor for Section 9", key="pa_9_ai_button"):
                # 🔧 Hook this into your AI backend / knowledge base
                # Example pattern (pseudo-code):
                # st.session_state.pa_9_ai_answer = call_ai_helper(section="9", question=ai_question)
                if not ai_question.strip():
                    st.warning("Please enter a question before asking AI Realtor.")
                else:
                    st.info(
                        "Your question has been sent to the AI Realtor helper. "
                        "Wire this button to your AI backend to return a real answer."
                    )

        with col_human:
            if st.button("Connect with a Human Realtor", key="pa_9_human_button"):
                st.session_state["pa_9_show_human_form"] = True

        # Human Realtor form (shown after button click)
        if st.session_state.get("pa_9_show_human_form", False):
            st.markdown("##### Connect with a Human Realtor")
            st.text_area(
                "Describe your situation and questions",
                key="pa_9_human_message",
                placeholder=(
                    "Example: I’m not sure if I should let the seller stay after closing. "
                    "Please review my situation and call or email me with advice."
                ),
            )
            st.text_input(
                "Preferred contact (phone or email)",
                key="pa_9_human_contact",
                placeholder="Example: 415-555-1234 or name@email.com",
            )

            if st.button("Submit to Human Realtor", key="pa_9_human_submit"):
                # 🔧 Wire this into your backend / database / email system
                # Example: save_to_db(section="9", message=..., contact=...)
                st.success(
                    "Your message has been submitted. A licensed Realtor will follow up using your preferred contact."
                )
                # Optionally hide the form after submission
                st.session_state["pa_9_show_human_form"] = False

    st.markdown("---")



    # -------------------------------
    # 9A. Closing Date
    # -------------------------------
    st.markdown("### 9A. Closing Date")

    col_date, col_timing = st.columns([1, 1.2])

    with col_date:
        st.date_input(
            "Target closing date",
            key="pa_9A_closing_date",
            help="Select the target close of escrow date.",
        )

    with col_timing:
        st.radio(
            "Close of escrow timing",
            options=[
                "On the date specified above",
                "On or before the date specified above",
            ],
            key="pa_9A_close_timing",
        )

    st.checkbox(
        "Allow a short automatic extension if needed for loan funding or recording (e.g., up to 5 days)",
        key="pa_9A_allow_extension",
    )

    st.text_area(
        "Notes or special instructions about the closing date (optional)",
        key="pa_9A_notes",
        placeholder="Example: Buyer and Seller agree that if lender or title needs extra time, the closing date may be extended up to 5 calendar days...",
    )

    st.markdown("---")

    # -------------------------------
    # 9B. Buyer Possession
    # -------------------------------
    st.markdown("### 9B. Buyer Possession")

    possession_choice = st.radio(
        "Buyer to take possession:",
        options=[
            "At close of escrow",
            "Upon recordation of the deed",
            "Other (describe below)",
        ],
        key="pa_9B_possession_choice",
    )

    if possession_choice == "Other (describe below)":
        st.text_input(
            "Describe possession terms",
            key="pa_9B_possession_other",
            placeholder="Example: Buyer to take possession 3 days after close of escrow...",
        )

    st.text_area(
        "Any additional details about buyer possession (optional)",
        key="pa_9B_notes",
        placeholder="Example: Buyer may access property for measurements or contractor bids at reasonable times with notice...",
    )

    st.markdown("---")

    # -------------------------------
    # 9C. Seller Remaining in Possession After Close
    # -------------------------------
    st.markdown("### 9C. Seller Remaining in Possession After Close of Escrow")

    seller_possession = st.radio(
        "Will the seller remain in possession after close of escrow?",
        options=[
            "No – Seller will deliver vacant possession at close",
            "Yes – Short-term seller possession (few days)",
            "Yes – Longer-term leaseback (30+ days)",
        ],
        key="pa_9C_seller_possession",
    )

    if seller_possession != "No – Seller will deliver vacant possession at close":
        st.markdown(
            "_If Seller stays after close, a separate written agreement is typically required (e.g., SIP or RLAS)._"
        )

        col_forms = st.columns(3)
        with col_forms[0]:
            st.checkbox(
                "Seller in Possession (SIP)",
                key="pa_9C_form_SIP",
                help="Short-term occupancy after close (typically 30 days or less).",
            )
        with col_forms[1]:
            st.checkbox(
                "Residential Lease After Sale (RLAS)",
                key="pa_9C_form_RLAS",
                help="Longer-term leaseback after closing.",
            )
        with col_forms[2]:
            st.checkbox(
                "Other agreement",
                key="pa_9C_form_other",
                help="Any other written agreement regarding seller’s occupancy.",
            )

        st.text_area(
            "Key details for seller remaining in possession",
            key="pa_9C_details",
            placeholder=(
                "Example: Seller to remain in possession up to 7 days after close at no cost. "
                "Seller responsible for utilities and property condition during occupancy..."
            ),
        )

    st.markdown("---")

    # -------------------------------
    # 9D. Keys, Garage Remotes & Access Devices
    # -------------------------------
    st.markdown("### 9D. Keys, Garage Remotes and Access Devices")

    st.radio(
        "Timing for delivery of keys and access devices",
        options=[
            "At close of escrow",
            "Upon recordation of the deed",
            "Other (describe below)",
        ],
        key="pa_9D_delivery_timing",
    )

    st.text_area(
        "Included keys, remotes and access items (optional)",
        key="pa_9D_items",
        placeholder=(
            "Example: Front door keys (2 sets), mailbox key, building fob(s), "
            "garage remotes (2), pool key, storage room key..."
        ),
    )

    st.text_area(
        "Any exceptions or special instructions (optional)",
        key="pa_9D_notes",
        placeholder="Example: One mailbox key currently missing; HOA to re-key mailbox at buyer’s expense...",
    )

    st.markdown("---")

    # -------------------------------
    # 9E. Final Verification of Property Condition
    # -------------------------------
    st.markdown("### 9E. Final Verification of Property Condition")

    final_verification_choice = st.radio(
        "Final verification of property condition:",
        options=[
            "Buyer will perform final verification (recommended)",
            "Buyer waives final verification (not recommended)",
        ],
        key="pa_9E_verification_choice",
    )

    if final_verification_choice == "Buyer will perform final verification (recommended)":
        col_vp = st.columns([1, 1])
        with col_vp[0]:
            st.date_input(
                "Target date for final walkthrough",
                key="pa_9E_walkthrough_date",
                help="Typically scheduled just before close of escrow.",
            )
        with col_vp[1]:
            st.text_input(
                "Who will coordinate access?",
                key="pa_9E_walkthrough_contact",
                placeholder="Example: Listing agent / Seller / Combo lockbox",
            )

    st.text_area(
        "Notes about final verification (optional)",
        key="pa_9E_notes",
        placeholder="Example: Buyer to confirm repairs are complete and property is in substantially the same condition as when offer was accepted...",
    )

    st.markdown("---")

    
    # -------------------------------
    # Bottom Navigation – Save / Next Section
    # -------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Section 9", key="pa_9_save"):
            # 🔧 Hook to your persistence logic (e.g., save to session/DB)
            st.success("Section 9 responses saved (connect this button to your save logic).")

    with col_right:
        if st.button("Next: Section 10", key="pa_9_next"):
            # 🔧 Update this index to match your tab / navigation system
            # Example if you're using st.session_state.active_pa_tab:
            # st.session_state.active_pa_tab = 9  # adjust to actual index for Section 10
            st.session_state["active_pa_tab"] = st.session_state.get("active_pa_tab", 0) + 1
            st.info("Moving to Section 10… (ensure this updates your main app navigation).")
