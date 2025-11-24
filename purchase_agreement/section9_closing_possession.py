# purchase_agreement/section9_closing_possession.py

import streamlit as st
from purchase_agreement.ai_helpers import call_purchase_agreement_ai

# ⬇️ IMPORTANT:
# Make sure to import call_purchase_agreement_ai the same way you do in Section 8, e.g.:
# from purchase_agreement.ai_helpers import call_purchase_agreement_ai


def render_section9_closing_possession():
    """
    Render Section 9 – Closing and Possession of the Purchase Agreement.
    """

    st.markdown("## 9. Closing and Possession")

    # ---------------------------
    # 🔹 GPT / AI Realtor – at the top of Section 9
    # ---------------------------
    with st.expander("💬 Need help with Section 9? Ask AI Realtor", expanded=True):
        st.markdown(
            "Use this assistant to understand closing timelines, possession, rent-backs, "
            "key/remote delivery, and final walkthroughs in California purchase agreements.\n\n"
            "**Reminder:** This is not legal advice. Always confirm with your broker or attorney."
        )

        default_prompt_9 = (
            "You are an experienced California residential real estate agent. "
            "Help the buyer understand how to complete Section 9 – Closing and Possession "
            "in the CAR Residential Purchase Agreement. Explain typical norms for: "
            "close of escrow timing, when the buyer gets possession, seller rent-backs, "
            "key/remote delivery, and final walkthroughs. "
            "Always remind them that everything is negotiable and practices vary by area."
        )

        # Use a form so pressing Enter in the text input will submit (Ask AI)
        with st.form("pa9_ai_form"):
            user_prompt_9 = st.text_input(
                "What do you want help with in Section 9?",
                key="pa9_ai_prompt",
                placeholder=(
                    "Example: Is it risky to let the seller stay 10 days after closing?\n"
                    "Example: Should I plan possession at close or on recordation?\n"
                    "Example: When should I schedule the final walkthrough?"
                ),
            )

            col_ai1, col_ai2 = st.columns([3, 2])
            with col_ai1:
                use_context_9 = st.checkbox(
                    "Include default Section 9 context in my question",
                    value=True,
                    key="pa9_ai_use_context",
                )
            with col_ai2:
                ask_clicked_9 = st.form_submit_button(
                    "Ask AI Realtor about Section 9",
                    use_container_width=True,
                )
                connect_clicked_9 = st.form_submit_button(
                    "Connect with a Human Realtor",
                    use_container_width=True,
                )

        # Handle Ask AI (form submit or Enter)
        if ask_clicked_9:
            if not user_prompt_9.strip():
                st.warning("Please enter a question or description first.")
            else:
                full_prompt_9 = user_prompt_9.strip()
                if use_context_9:
                    full_prompt_9 = (
                        default_prompt_9
                        + "\n\nUser question:\n"
                        + user_prompt_9.strip()
                    )

                with st.spinner("Thinking like a California Realtor..."):
                    try:
                        # 🔹 Same backend call as Section 8, but with section="9"
                        answer_9 = call_purchase_agreement_ai(
                            full_prompt_9, section="9"
                        )
                    except Exception as e:
                        answer_9 = (
                            "There was an error calling the AI backend for Section 9.\n\n"
                            f"Details: {e}"
                        )

                    st.session_state["pa9_ai_answer"] = answer_9

        # Handle Connect with Human Realtor
        if connect_clicked_9:
            st.session_state["pa9_show_human_realtor_form"] = True

        # Show AI answer if we have one
        if "pa9_ai_answer" in st.session_state:
            st.markdown("#### 🧠 AI Realtor Suggestion (Section 9)")
            st.info(st.session_state["pa9_ai_answer"])

        # Show the human-realtor contact form if toggled on
        if st.session_state.get("pa9_show_human_realtor_form", False):
            st.markdown("#### 🤝 Connect with a Human Realtor")

            contact_info_9 = st.text_input(
                "Your preferred phone or email",
                key="pa9_human_contact",
                placeholder="Example: 415-555-1234 or you@example.com",
            )
            human_question_9 = st.text_area(
                "What would you like to ask a human?",
                key="pa9_human_question",
                height=100,
                placeholder="Share your questions or situation so a human realtor can follow up.",
            )

            send_clicked_9 = st.button(
                "Send my question to a Human Realtor",
                key="pa9_human_send_btn",
                use_container_width=True,
            )

            if send_clicked_9:
                if not contact_info_9.strip() or not human_question_9.strip():
                    st.warning("Please provide both your contact info and your question.")
                else:
                    # Integrate with email / DB / CRM if desired
                    st.session_state["pa9_human_realtor_request"] = {
                        "contact": contact_info_9.strip(),
                        "question": human_question_9.strip(),
                    }
                    st.success(
                        "Your request has been recorded. A human realtor will reach out to you using the contact info you provided."
                    )

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
        placeholder=(
            "Example: Buyer and Seller agree that if lender or title needs extra time, "
            "the closing date may be extended up to 5 calendar days..."
        ),
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
        placeholder=(
            "Example: Buyer may access property for measurements or contractor bids at "
            "reasonable times with notice..."
        ),
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
            "_If Seller stays after close, a separate written agreement is typically "
            "required (e.g., SIP or RLAS)._"
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
        placeholder=(
            "Example: One mailbox key currently missing; HOA to re-key mailbox at buyer’s "
            "expense..."
        ),
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
        placeholder=(
            "Example: Buyer to confirm repairs are complete and property is in substantially "
            "the same condition as when offer was accepted..."
        ),
    )

    st.markdown("---")

    # -------------------------------
    # Bottom Navigation – Save / Next Section
    # -------------------------------
    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Section 9", key="pa_9_save"):
            # Hook to your persistence logic (e.g., save to session/DB)
            st.success("Section 9 responses saved (connect this button to your save logic).")

    with col_right:
        if st.button("Next: Section 10", key="pa_9_next"):
            # Update this to match your app's navigation
            # Example if you're using st.session_state.active_pa_tab:
            # st.session_state.active_pa_tab = 9  # or another index for Section 10
            st.session_state["active_pa_tab"] = st.session_state.get("active_pa_tab", 0) + 1
            st.info("Moving to Section 10… (ensure this updates your main app navigation).")
