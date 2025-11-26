# purchase_agreement/section3_finance.py

import streamlit as st

SECTION3_KEY = "pa_section3_finance"


def _init_section3_state():
    if SECTION3_KEY not in st.session_state:
        st.session_state[SECTION3_KEY] = {
            # 3A – Initial Deposit
            "initial_deposit_amount": 0.0,
            "initial_deposit_method": "Direct to escrow holder",
            "initial_deposit_instrument": "Wire transfer",
            "initial_deposit_days": 3,
            "show_deposit_explanation": False,

            # 3B – Increased Deposit
            "has_increased_deposit": False,
            "increased_deposit_amount": 0.0,
            "increased_deposit_days": 10,

            # 3C–3E – All-Cash / Loans
            "is_all_cash": False,
            "proof_of_funds_days": 3,

            "first_loan_amount": 0.0,
            "first_loan_type": "Conventional",
            "first_loan_fixed_or_arm": "Fixed rate",
            "first_loan_max_rate": 8.0,
            "first_loan_max_points": 1.0,

            "has_second_loan": False,
            "second_loan_amount": 0.0,
            "second_loan_type": "Conventional",
            "second_loan_fixed_or_arm": "Fixed rate",
            "second_loan_max_rate": 9.0,
            "second_loan_max_points": 1.0,

            "additional_financing_terms": "",

            # 3F / 3G / 3H
            "purchase_price_total_manual": 0.0,  # fallback if we can't read Section 1
            "down_payment_balance_amount": 0.0,
            "verification_funds_days": 3,

            # 3I – Appraisal Contingency
            "has_appraisal_contingency": True,
            "appraisal_contingency_days": 17,

            # 3J – Loan Application / Letter
            "loan_letter_days": 3,
            "loan_preapproval_attached": False,

            # 3K – Loan Contingency
            "has_loan_contingency": True,
            "loan_contingency_days": 21,
        }


def _get_purchase_price_from_section1() -> float:
    """
    Try to pull Purchase Price from Section 1 state if available.
    If not found, return 0.0 and let user enter manually.
    """
    # Adjust these keys later if your Section 1 uses different naming
    possible_keys = [
        "pa_section1_offer",
        "section1_offer",
        "purchase_agreement_section1",
    ]
    for key in possible_keys:
        sec = st.session_state.get(key)
        if isinstance(sec, dict) and "purchase_price" in sec:
            try:
                return float(sec["purchase_price"])
            except Exception:
                return 0.0
    return 0.0


def render_section3_finance():
    _init_section3_state()
    data = st.session_state[SECTION3_KEY]

    st.subheader("Section 3 – Finance Terms")

    st.markdown(
        "> This section mirrors **Section 3 – Finance Terms** of the California "
        "Residential Purchase Agreement (RPA). It covers deposits, loans, and key "
        "financing contingencies. This is an AI-generated drafting aid and does "
        "**not** replace legal or financial advice."
    )

    # --- 3A. Initial Deposit ---
    st.markdown("### 3A. Initial Deposit")

    col1, col2 = st.columns(2)
    with col1:
        data["initial_deposit_amount"] = st.number_input(
            "Initial deposit amount ($)",
            min_value=0.0,
            value=float(data["initial_deposit_amount"]),
            step=1000.0,
            format="%.2f",
        )
    with col2:
        data["initial_deposit_days"] = st.number_input(
            "Days After Acceptance to deliver deposit",
            min_value=0,
            value=int(data["initial_deposit_days"]),
            step=1,
        )

    # How delivered
    deposit_method_options = [
        "Direct to escrow holder",
        "Given to buyer’s agent to hold then deliver to escrow",
    ]
    current_method = data.get("initial_deposit_method", deposit_method_options[0])
    if current_method not in deposit_method_options:
        current_method = deposit_method_options[0]

    data["initial_deposit_method"] = st.selectbox(
        "How will the deposit be delivered?",
        deposit_method_options,
        index=deposit_method_options.index(current_method),
    )

    # Instrument
    instrument_options = [
        "Wire transfer",
        "Cashier’s check",
        "Personal check",
        "Other",
    ]
    curr_instr = data.get("initial_deposit_instrument", instrument_options[0])
    if curr_instr not in instrument_options:
        curr_instr = instrument_options[0]

    data["initial_deposit_instrument"] = st.selectbox(
        "Form of deposit",
        instrument_options,
        index=instrument_options.index(curr_instr),
    )

    # Short market norm + risk blurb
    st.markdown(
        "**💡 Market norm in California**  \n"
        "In many California residential purchases, the **total earnest money deposit is "
        "commonly around 3% of the purchase price**, especially when the parties "
        "agree to a **liquidated damages** clause.\n\n"
        "**⚠️ Important:** Your deposit can be at risk if you **default under the "
        "contract after removing contingencies** or cancel for a reason **not allowed "
        "by the agreement**. This app does **not** replace legal advice."
    )

    # Explain in details / Close explanation toggle
    if not data.get("show_deposit_explanation", False):
        if st.button("Explain in details", key="btn_show_deposit_details"):
            data["show_deposit_explanation"] = True
    else:
        st.markdown("#### When is my deposit at risk in California?")
        st.markdown(
            "1. **Canceling after removing contingencies**  \n"
            "   Once you’ve **removed your contingencies in writing** (inspection, "
            "appraisal, loan, etc.) and then refuse or fail to close, the seller may be "
            "able to claim your deposit as **liquidated damages**, often capped at 3% on "
            "1–4 unit owner-occupied property.\n\n"
            "2. **Ignoring a Notice to Perform**  \n"
            "   If you don’t do something the contract requires (for example: you don’t "
            "deliver the deposit on time, or don’t provide proof of funds or loan "
            "pre-approval), and you still don’t perform after the seller sends a "
            "**Notice to Buyer to Perform**, the seller may cancel and may have the "
            "right to keep the deposit as a remedy.\n\n"
            "3. **Canceling for a reason that’s not covered by any contingency**  \n"
            "   If you simply change your mind, get “cold feet,” or walk away for a "
            "reason that isn’t protected by an **active contingency**, the seller may "
            "be entitled to your deposit.\n\n"
            "4. **Waiving the loan contingency and then failing to get the loan**  \n"
            "   If you **waive your loan contingency** (or never include one) but later "
            "your financing falls apart, that is usually treated as a **buyer default**, "
            "and the seller may try to keep the deposit.\n\n"
            "5. **Misrepresentation or bad faith**  \n"
            "   If you misrepresent your ability to close (for example, fake proof of "
            "funds or deliberate non-payment), you can be treated as in breach, and "
            "your deposit may be at risk, in addition to other possible remedies.\n\n"
            "6. **You sign a cancellation that gives the deposit to the seller**  \n"
            "   Escrow usually needs **instructions signed by both sides** to release "
            "the deposit. If you agree in writing to give your deposit (or part of it) "
            "to the seller, you should not expect that portion back.\n\n"
            "*This is a general overview of common California practice. The exact "
            "treatment of your deposit depends on your specific contract and facts. "
            "For advice, speak with your real estate broker or a California real estate "
            "attorney.*"
        )
        if st.button("Close explanation", key="btn_hide_deposit_details"):
            data["show_deposit_explanation"] = False

    st.markdown("---")

    # --- 3B. Increased Deposit ---
    st.markdown("### 3B. Increased Deposit (optional)")
    data["has_increased_deposit"] = st.checkbox(
        "Will there be an additional increased deposit?",
        value=bool(data["has_increased_deposit"]),
    )

    if data["has_increased_deposit"]:
        col1, col2 = st.columns(2)
        with col1:
            data["increased_deposit_amount"] = st.number_input(
                "Increased deposit amount ($)",
                min_value=0.0,
                value=float(data["increased_deposit_amount"]),
                step=1000.0,
                format="%.2f",
            )
        with col2:
            data["increased_deposit_days"] = st.number_input(
                "Days After Acceptance to deliver increased deposit",
                min_value=0,
                value=int(data["increased_deposit_days"]),
                step=1,
            )
        st.caption(
            "If the liquidated damages clause is initialed, the increased deposit is "
            "usually included in the liquidated damages amount."
        )

    st.markdown("---")

    # --- 3C–3E. All-Cash / Loan Terms ---
    st.markdown("### 3C–3E. All-Cash / Loan Terms")

    data["is_all_cash"] = st.checkbox(
        "All-cash offer (Buyer does not need a loan to close)",
        value=bool(data["is_all_cash"]),
    )

    if data["is_all_cash"]:
        data["proof_of_funds_days"] = st.number_input(
            "Days After Acceptance for Buyer to provide proof of funds",
            min_value=0,
            value=int(data["proof_of_funds_days"]),
            step=1,
        )
        st.info(
            "All-cash offer selected. The agreement will state that Buyer does not "
            "need a loan to purchase the property and will provide written verification "
            "of sufficient funds to close."
        )
    else:
        # First Loan
        st.markdown("#### First Loan")
        col1, col2 = st.columns(2)
        with col1:
            data["first_loan_amount"] = st.number_input(
                "First loan amount ($)",
                min_value=0.0,
                value=float(data["first_loan_amount"]),
                step=10000.0,
                format="%.2f",
            )
        with col2:
            first_loan_type_options = [
                "Conventional",
                "FHA",
                "VA",
                "Seller financing",
                "Assumed financing",
                "Other",
            ]
            cur_type = data.get("first_loan_type", first_loan_type_options[0])
            if cur_type not in first_loan_type_options:
                cur_type = first_loan_type_options[0]

            data["first_loan_type"] = st.selectbox(
                "First loan type",
                first_loan_type_options,
                index=first_loan_type_options.index(cur_type),
            )

        col1, col2 = st.columns(2)
        with col1:
            structure_options = ["Fixed rate", "Adjustable rate (ARM)"]
            cur_struct = data.get("first_loan_fixed_or_arm", structure_options[0])
            if cur_struct not in structure_options:
                cur_struct = structure_options[0]

            data["first_loan_fixed_or_arm"] = st.selectbox(
                "First loan structure",
                structure_options,
                index=structure_options.index(cur_struct),
            )
        with col2:
            data["first_loan_max_rate"] = st.number_input(
                "Maximum initial interest rate (%)",
                min_value=0.0,
                value=float(data["first_loan_max_rate"]),
                step=0.125,
                format="%.3f",
            )

        data["first_loan_max_points"] = st.number_input(
            "Maximum points Buyer will pay (% of loan amount)",
            min_value=0.0,
            value=float(data["first_loan_max_points"]),
            step=0.25,
            format="%.2f",
        )

        # Second Loan
        st.markdown("#### Second Loan (optional)")
        data["has_second_loan"] = st.checkbox(
            "Add a second loan?",
            value=bool(data["has_second_loan"]),
        )

        if data["has_second_loan"]:
            col1, col2 = st.columns(2)
            with col1:
                data["second_loan_amount"] = st.number_input(
                    "Second loan amount ($)",
                    min_value=0.0,
                    value=float(data["second_loan_amount"]),
                    step=10000.0,
                    format="%.2f",
                )
            with col2:
                second_loan_type_options = [
                    "Conventional",
                    "Seller financing",
                    "Assumed financing",
                    "Other",
                ]
                cur_type2 = data.get(
                    "second_loan_type", second_loan_type_options[0]
                )
                if cur_type2 not in second_loan_type_options:
                    cur_type2 = second_loan_type_options[0]

                data["second_loan_type"] = st.selectbox(
                    "Second loan type",
                    second_loan_type_options,
                    index=second_loan_type_options.index(cur_type2),
                )

            col1, col2 = st.columns(2)
            with col1:
                cur_struct2 = data.get(
                    "second_loan_fixed_or_arm", structure_options[0]
                )
                if cur_struct2 not in structure_options:
                    cur_struct2 = structure_options[0]

                data["second_loan_fixed_or_arm"] = st.selectbox(
                    "Second loan structure",
                    structure_options,
                    index=structure_options.index(cur_struct2),
                )
            with col2:
                data["second_loan_max_rate"] = st.number_input(
                    "Maximum initial interest rate for second loan (%)",
                    min_value=0.0,
                    value=float(data["second_loan_max_rate"]),
                    step=0.125,
                    format="%.3f",
                )

            data["second_loan_max_points"] = st.number_input(
                "Maximum points on second loan (% of loan amount)",
                min_value=0.0,
                value=float(data["second_loan_max_points"]),
                step=0.25,
                format="%.2f",
            )

        # FHA/VA paragraph – only if first loan is FHA or VA
        if data["first_loan_type"] in ("FHA", "VA"):
            st.markdown("#### FHA / VA Loans")
            st.markdown(
                "> **FHA/VA:** For any FHA or VA loan specified in 3D(1), Buyer has "
                "**17 (or ☐)** Days After Acceptance to Deliver to Seller written "
                "notice (C.A.R. Form FVA) of any lender-required repairs or costs that "
                "Buyer requests Seller to pay for or otherwise correct. Seller has no "
                "obligation to pay or satisfy lender requirements unless agreed in "
                "writing. A FHA/VA amendatory clause (C.A.R. Form FVAC) shall be part "
                "of this transaction."
            )

    # Additional Financing Terms
    st.markdown("### 3E. Additional Financing Terms (optional)")
    data["additional_financing_terms"] = st.text_area(
        "Additional terms related to financing, credits, rate buydown, or special structures:",
        value=data["additional_financing_terms"],
        height=120,
        placeholder=(
            "Example: Seller to credit Buyer up to $10,000 toward recurring and "
            "non-recurring closing costs, subject to lender approval. Buyer to pay any "
            "discount points needed to obtain chosen interest rate."
        ),
    )

    st.markdown("---")

    # --- 3F. Purchase Price (Total) ---
    st.markdown("### 3F. Purchase Price (Total)")
    auto_price = _get_purchase_price_from_section1()
    if auto_price > 0:
        st.info(
            "Purchase Price is pulled from Section 1. If this does not match, please "
            "update Section 1 – Offer Terms."
        )
        st.write(f"**Purchase Price (Total):** ${auto_price:,.2f}")
        data["purchase_price_total_manual"] = auto_price
    else:
        data["purchase_price_total_manual"] = st.number_input(
            "Purchase Price (Total) – should match Section 1",
            min_value=0.0,
            value=float(data["purchase_price_total_manual"]),
            step=10000.0,
            format="%.2f",
        )

    st.markdown("---")

    # --- 3G. Balance of Down Payment ---
    st.markdown("### 3G. Balance of Down Payment")
    data["down_payment_balance_amount"] = st.number_input(
        "Balance of down payment or purchase price to be deposited with escrow ($)",
        min_value=0.0,
        value=float(data["down_payment_balance_amount"]),
        step=10000.0,
        format="%.2f",
        help="Typically Purchase Price – Deposits – Loan Amount(s).",
    )

    st.markdown("---")

    # --- 3H. Verification of Down Payment and Closing Costs ---
    st.markdown("### 3H. Verification of Down Payment and Closing Costs")
    data["verification_funds_days"] = st.number_input(
        "Days After Acceptance for Buyer to provide verification of funds",
        min_value=0,
        value=int(data["verification_funds_days"]),
        step=1,
    )
    st.caption(
        "Buyer typically provides bank statements or other proof of funds for the down "
        "payment and closing costs within this time period."
    )

    st.markdown("---")

    # --- 3I. Appraisal Contingency ---
    st.markdown("### 3I. Appraisal Contingency")

    data["has_appraisal_contingency"] = st.checkbox(
        "Include appraisal contingency (property must appraise at or above purchase price)",
        value=bool(data["has_appraisal_contingency"]),
    )

    if data["has_appraisal_contingency"]:
        data["appraisal_contingency_days"] = st.number_input(
            "Days After Acceptance to remove appraisal contingency",
            min_value=0,
            value=int(data["appraisal_contingency_days"]),
            step=1,
        )
    else:
        st.warning(
            "No appraisal contingency selected. If the property appraises below the "
            "purchase price but you are otherwise loan-qualified, you may not be able "
            "to cancel under the loan contingency alone."
        )

    st.markdown("---")

    # --- 3J. Loan Application / Preapproval ---
    st.markdown("### 3J. Loan Application and Preapproval Letter")

    col1, col2 = st.columns(2)
    with col1:
        data["loan_letter_days"] = st.number_input(
            "Days After Acceptance to Deliver prequalification / preapproval letter",
            min_value=0,
            value=int(data["loan_letter_days"]),
            step=1,
        )
    with col2:
        data["loan_preapproval_attached"] = st.checkbox(
            "Pre-approval / pre-qualification letter attached",
            value=bool(data["loan_preapproval_attached"]),
        )

    st.markdown(
        "Within this time period, Buyer is expected to Deliver to Seller a letter from "
        "Buyer’s lender or loan broker stating that, based on a review of Buyer’s "
        "written loan application and credit report, Buyer is prequalified or "
        "preapproved for the loan(s) specified in 3D. For adjustable-rate loans, the "
        "letter must be based on the **qualifying rate**, not just the initial rate."
    )

    st.markdown("---")

    # --- 3K. Loan Contingency ---
    st.markdown("### 3K. Loan Contingency")

    data["has_loan_contingency"] = st.checkbox(
        "Include loan contingency (Buyer’s obligation is contingent on obtaining the specified loan)",
        value=bool(data["has_loan_contingency"]),
    )

    st.markdown(
        "Buyer shall act diligently and in good faith to obtain the designated loan(s), "
        "including submitting all necessary documentation, paying required fees, and "
        "cooperating with the lender throughout the loan process."
    )

    if data["has_loan_contingency"]:
        data["loan_contingency_days"] = st.number_input(
            "Days After Acceptance to remove loan contingency",
            min_value=0,
            value=int(data["loan_contingency_days"]),
            step=1,
        )
        st.caption(
            "The Loan Contingency protects the Buyer. Removing it early exposes the "
            "deposit if financing later fails."
        )
    else:
        st.error(
            "No Loan Contingency. Buyer’s obligations are not conditioned upon "
            "obtaining a loan. If Buyer cannot obtain financing and fails to close, "
            "Buyer may be in default and Seller may be entitled to retain the deposit "
            "as liquidated damages if that provision is initialed."
        )

    # --- Save + Navigation Buttons ---
    # st.markdown("---")
    # col1, col2 = st.columns(2)
    # with col1:
    #     if st.button("💾 Save Section 3 – Finance Terms", use_container_width=True):
    #         st.session_state[SECTION3_KEY] = data
    #         st.success("Section 3 – Finance Terms saved.")
    # with col2:
    #     if st.button("➡️ Move to Section 4", use_container_width=True):
    #         st.session_state[SECTION3_KEY] = data
    #         # assuming tabs are 0-indexed and Section 4 is index 3
    #         st.session_state.active_pa_tab = 4&5
    #         st.info("Moved to Section 4.")
