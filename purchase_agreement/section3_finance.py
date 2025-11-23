# pa_section3_finance.py

import streamlit as st

SECTION3_KEY = "pa_section3_finance"

def _init_section3_state():
    if SECTION3_KEY not in st.session_state:
        st.session_state[SECTION3_KEY] = {
            "initial_deposit_amount": 0.0,
            "initial_deposit_method": "Direct to escrow",
            "initial_deposit_instrument": "Wire transfer",
            "initial_deposit_days": 3,

            "has_increased_deposit": False,
            "increased_deposit_amount": 0.0,
            "increased_deposit_days": 10,

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

            "down_payment_balance_amount": 0.0,

            "verification_funds_days": 3,
            "has_appraisal_contingency": True,
            "appraisal_contingency_days": 17,

            "has_loan_contingency": True,
            "loan_contingency_days": 21,

            "sale_of_buyer_property_contingency": False,
            "buyer_property_address": "",
            "buyer_property_notes": "",
        }


def render_section3_finance():
    _init_section3_state()
    data = st.session_state[SECTION3_KEY]

    st.subheader("Section 3 – Finance Terms")

    st.markdown(
        "> This section mirrors **Section 3 – Finance Terms** of the California "
        "Residential Purchase Agreement (RPA). It controls deposits, loans, and "
        "financing-related contingencies. This is an AI-generated drafting aid and "
        "**not legal or financial advice**."
    )

    # --- 3A Initial Deposit ---
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
            "Days after Acceptance to deliver deposit",
            min_value=0,
            value=int(data["initial_deposit_days"]),
            step=1,
        )

    data["initial_deposit_method"] = st.selectbox(
        "How will the deposit be delivered?",
        [
            "Direct to escrow holder",
            "Given to buyer’s agent to hold then deliver to escrow",
        ],
        index=[
            "Direct to escrow holder",
            "Given to buyer’s agent to hold then deliver to escrow",
        ].index(data["initial_deposit_method"]),
    )

    data["initial_deposit_instrument"] = st.selectbox(
        "Form of deposit",
        ["Wire transfer", "Cashier’s check", "Personal check", "Other"],
        index=["Wire transfer", "Cashier’s check", "Personal check", "Other"].index(
            data["initial_deposit_instrument"]
        ),
    )

    # --- 3B Increased Deposit ---
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
                "Days after Acceptance to deliver increased deposit",
                min_value=0,
                value=int(data["increased_deposit_days"]),
                step=1,
            )
        st.caption(
            "Note: If you use the standard liquidated damages clause, this increased "
            "deposit is usually included in the liquidated damages amount."
        )

    # --- 3C / 3D All Cash vs Loans ---
    st.markdown("### 3C–3D. All-Cash vs Loan Financing")

    data["is_all_cash"] = st.checkbox(
        "All-cash offer (no loan contingency; Buyer does not need a loan to close)",
        value=bool(data["is_all_cash"]),
    )

    if data["is_all_cash"]:
        data["proof_of_funds_days"] = st.number_input(
            "Days after Acceptance for Buyer to provide proof of funds",
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
            data["first_loan_type"] = st.selectbox(
                "First loan type",
                ["Conventional", "FHA", "VA", "Seller financing", "Assumed financing", "Other"],
                index=[
                    "Conventional",
                    "FHA",
                    "VA",
                    "Seller financing",
                    "Assumed financing",
                    "Other",
                ].index(data["first_loan_type"]),
            )

        col1, col2 = st.columns(2)
        with col1:
            data["first_loan_fixed_or_arm"] = st.selectbox(
                "First loan structure",
                ["Fixed rate", "Adjustable rate (ARM)"],
                index=[
                    "Fixed rate",
                    "Adjustable rate (ARM)",
                ].index(data["first_loan_fixed_or_arm"]),
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
                data["second_loan_type"] = st.selectbox(
                    "Second loan type",
                    ["Conventional", "Seller financing", "Assumed financing", "Other"],
                    index=[
                        "Conventional",
                        "Seller financing",
                        "Assumed financing",
                        "Other",
                    ].index(data["second_loan_type"]),
                )

            col1, col2 = st.columns(2)
            with col1:
                data["second_loan_fixed_or_arm"] = st.selectbox(
                    "Second loan structure",
                    ["Fixed rate", "Adjustable rate (ARM)"],
                    index=[
                        "Fixed rate",
                        "Adjustable rate (ARM)",
                    ].index(data["second_loan_fixed_or_arm"]),
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

    # --- 3E Additional Financing Terms ---
    st.markdown("### 3E. Additional Financing Terms (optional)")
    data["additional_financing_terms"] = st.text_area(
        "Additional terms related to financing, credits, rate buydown, or special structures:",
        value=data["additional_financing_terms"],
        height=120,
        placeholder=(
            "Example: Seller to credit Buyer up to $10,000 toward recurring and non-recurring "
            "closing costs, subject to lender approval. Buyer to pay any discount points "
            "needed to obtain chosen interest rate."
        ),
    )

    # --- 3F Balance of Down Payment / Purchase Price ---
    st.markdown("### 3F. Balance of Down Payment / Purchase Price")
    data["down_payment_balance_amount"] = st.number_input(
        "Balance of down payment or purchase price to be deposited with escrow ($)",
        min_value=0.0,
        value=float(data["down_payment_balance_amount"]),
        step=10000.0,
        format="%.2f",
        help="Typically Purchase Price – Deposits – Loan Amount(s).",
    )

    # --- 3G Verification of Down Payment and Closing Costs ---
    st.markdown("### 3G. Verification of Down Payment and Closing Costs")
    data["verification_funds_days"] = st.number_input(
        "Days after Acceptance for Buyer to provide verification of funds",
        min_value=0,
        value=int(data["verification_funds_days"]),
        step=1,
    )

    # --- 3H Appraisal Contingency ---
    st.markdown("### 3H. Appraisal Contingency")
    data["has_appraisal_contingency"] = st.checkbox(
        "Include appraisal contingency (property must appraise at or above purchase price)",
        value=bool(data["has_appraisal_contingency"]),
    )

    if data["has_appraisal_contingency"]:
        data["appraisal_contingency_days"] = st.number_input(
            "Days after Acceptance to remove appraisal contingency",
            min_value=0,
            value=int(data["appraisal_contingency_days"]),
            step=1,
        )
    else:
        st.warning(
            "No appraisal contingency selected. If the property appraises below the purchase "
            "price but you are otherwise loan-qualified, you may not be able to cancel under "
            "the loan contingency alone."
        )

    # --- 3I Loan Application / Letter ---
    st.markdown("### 3I. Loan Application / Pre-Approval Letter")
    st.caption(
        "Buyer typically delivers a pre-qualification or pre-approval letter within a few days "
        "after Acceptance, based on written application and credit review."
    )

    # --- 3J Loan Contingency ---
    st.markdown("### 3J. Loan Contingency")
    data["has_loan_contingency"] = st.checkbox(
        "Include loan contingency (Buyer’s obligation is contingent on obtaining the specified loan)",
        value=bool(data["has_loan_contingency"]),
    )

    if data["has_loan_contingency"]:
        data["loan_contingency_days"] = st.number_input(
            "Days after Acceptance to remove loan contingency",
            min_value=0,
            value=int(data["loan_contingency_days"]),
            step=1,
        )
    else:
        st.error(
            "No loan contingency. If Buyer does not obtain the loan and cannot close, "
            "Seller may be entitled to retain the deposit or pursue other remedies."
        )

    # --- 3L Sale of Buyer’s Property ---
    st.markdown("### 3L. Sale of Buyer’s Property")
    data["sale_of_buyer_property_contingency"] = st.checkbox(
        "Is this purchase contingent on the sale of Buyer’s current property?",
        value=bool(data["sale_of_buyer_property_contingency"]),
    )

    if data["sale_of_buyer_property_contingency"]:
        data["buyer_property_address"] = st.text_input(
            "Buyer’s property address",
            value=data["buyer_property_address"],
        )
        data["buyer_property_notes"] = st.text_area(
            "Notes (e.g., whether that property is listed, in escrow, etc.)",
            value=data["buyer_property_notes"],
            height=100,
        )
        st.caption(
            "In the formal RPA, this would usually be documented using the "
            "Contingency for Sale of Buyer’s Property addendum (COP)."
        )

    # --- Save + Navigation Buttons ---
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Section 3 – Finance Terms", use_container_width=True):
            st.session_state[SECTION3_KEY] = data
            st.success("Section 3 – Finance Terms saved.")
    with col2:
        if st.button("➡️ Move to Section 4", use_container_width=True):
            st.session_state[SECTION3_KEY] = data
            # assuming tabs are 0-indexed and Section 4 is index 3
            st.session_state.active_pa_tab = 3
            st.info("Moved to Section 4.")
