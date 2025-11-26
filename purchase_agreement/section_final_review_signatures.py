# purchase_agreement/section_final_review_signatures.py

import streamlit as st
from datetime import datetime


def _get_value(*keys, default="Not provided yet"):
    """
    Helper: safely pull the first non-empty value from st.session_state by trying
    multiple possible keys. This lets you gradually wire your existing sections
    to this summary without the app crashing.
    """
    for key in keys:
        if key in st.session_state and st.session_state.get(key):
            return st.session_state.get(key)
    return default


def _format_expiration():
    """Helper to format the expiration date/time from Section 31."""
    exp_date = st.session_state.get("pa31_date")
    exp_time = st.session_state.get("pa31_time")

    if not exp_date or not exp_time:
        return "Not set yet"

    try:
        if isinstance(exp_date, datetime):
            d = exp_date.date()
        else:
            d = exp_date
        if isinstance(exp_time, datetime):
            t = exp_time.time()
        else:
            t = exp_time

        dt = datetime.combine(d, t)
        return dt.strftime("%B %d, %Y at %I:%M %p")
    except Exception:
        return "Unable to format expiration – please double-check Section 31."


def render_final_review_signatures():
    """
    Final Review & Signatures – Summary of key inputs before sending / signing.

    This section is intentionally READ-ONLY (summary) and pulls from st.session_state.
    You can adjust the keys below to match your actual Section 1 / 3 / 7 / 14 / 31 fields.
    """

    st.markdown("## Final Review & Signatures")

    st.markdown(
        "Before you sign or send this offer to the seller, please review the **key terms** "
        "below. Make sure they match what you intend. If anything looks off, go back to the "
        "earlier sections and update it first."
    )

    st.markdown("---")

    # --------------------------------------------------
    # 1. Who is buying the property
    # --------------------------------------------------
    st.markdown("### 1. Buyer(s) – Who is making this offer?")

    buyer_1 = _get_value("pa_buyer_1_name", "buyer_1_name")
    buyer_2 = _get_value("pa_buyer_2_name", "buyer_2_name", default="(No second buyer)")

    st.markdown(
        f"- **Buyer 1:** {buyer_1}\n"
        f"- **Buyer 2 (if any):** {buyer_2}"
    )

    st.info(
        "Names here should match how you intend to take title. If you plan to buy "
        "through an LLC, trust, or entity, make sure that is reflected in the actual contract."
    )

    st.markdown("---")

    # --------------------------------------------------
    # 2. Property – What are you buying?
    # --------------------------------------------------
    st.markdown("### 2. Property – Address of the home you’re offering on")

    property_address = _get_value(
        "pa_property_address",
        "property_address",
        "pa1_property_address",
    )

    st.markdown(f"- **Property address:** {property_address}")

    st.info(
        "Double-check that this address matches the MLS listing and your agent’s information."
    )

    st.markdown("---")

    # --------------------------------------------------
    # 3. Financing Terms – Price, earnest money, cash vs loan
    # --------------------------------------------------
    st.markdown("### 3. Financing Terms – How you are paying for this property")

    purchase_price = _get_value(
        "pa_purchase_price",
        "offer_price",
        "pa1_purchase_price",
    )

    earnest_money = _get_value(
        "pa_earnest_money_amount",
        "earnest_money_amount",
        "pa1_earnest_deposit",
    )

    financing_type = _get_value(
        "pa_financing_type",  # e.g. 'All Cash', 'Convention Loan + Down Payment'
        "financing_type",
        default="Not specified yet (cash vs financing not clearly set)",
    )

    loan_amount = _get_value(
        "pa_loan_amount",
        "loan_amount",
        default="Not specified",
    )

    down_payment = _get_value(
        "pa_down_payment_amount",
        "down_payment_amount",
        default="Not specified",
    )

    st.markdown("#### 3A. Purchase Price & Earnest Money")
    st.markdown(
        f"- **Offer price:** {purchase_price}\n"
        f"- **Earnest money / initial deposit:** {earnest_money}"
    )

    st.markdown("#### 3B. Cash vs Financing")
    st.markdown(
        f"- **Financing type:** {financing_type}\n"
        f"- **Estimated loan amount:** {loan_amount}\n"
        f"- **Estimated down payment:** {down_payment}"
    )

    st.info(
        "Your earnest money and financing structure should match what your lender "
        "pre-approval letter supports. If anything changed, let your agent and lender know."
    )

    st.markdown("---")

    # --------------------------------------------------
    # 4. Contingencies – How much protection & time you have
    # --------------------------------------------------
    st.markdown("### 4. Contingencies – Time and protection for your due diligence")

    contingency_days = _get_value(
        "pa14B1_contingency_days",
        "contingency_days",
        default="Not set yet",
    )

    contingency_notes = _get_value(
        "pa14B1_notes",
        "contingency_notes",
        default="(No additional notes were recorded.)",
    )

    st.markdown("#### 4A. Overall Buyer Contingency Period")
    st.markdown(
        f"- **Total contingency period:** {contingency_days} day(s) after acceptance"
    )

    st.markdown("#### 4B. Notes about your contingencies")
    st.markdown(f"{contingency_notes}")

    st.info(
        "This is the period for inspections, appraisal (if applicable), loan approval, "
        "and reviewing disclosures. Shorter periods are more competitive but give you less time."
    )

    st.markdown("---")

    # --------------------------------------------------
    # 5. Offer Expiration – How long the offer stays open
    # --------------------------------------------------
    st.markdown("### 5. Expiration of Offer – How long the seller has to decide")

    expiration_display = _format_expiration()

    st.markdown(
        f"- **Offer expires on:** {expiration_display}"
    )

    st.info(
        "If the seller signs **after** this expiration, it may not be a valid acceptance "
        "unless you confirm and re-approve with your agent. Make sure this timing matches "
        "your strategy and the seller’s availability."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Confirm & next steps
    # --------------------------------------------------
    st.markdown("### Final Check Before Signatures")

    confirm_reviewed = st.checkbox(
        "I have reviewed the key terms above and they match what I intend to offer.",
        key="pa_final_review_confirmed",
    )

    st.warning(
        "This tool does **not** replace legal advice. Before signing or sending your offer, "
        "review the full contract with your real estate agent, and consult an attorney if you have questions."
    )

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        if st.button("💾 Save Final Review", key="pa_final_save"):
            # Hook this into your persistence / DB if needed
            st.success("Final review saved (connect this button to your actual save logic).")

    with col_right:
        if st.button("Continue to Signatures / Export", key="pa_final_next"):
            if not confirm_reviewed:
                st.error(
                    "Please confirm that you have reviewed the key terms above before continuing."
                )
            else:
                # Example: move to a 'Signatures / Export' tab in your app
                # st.session_state['active_pa_tab'] = <index_of_signatures_tab>
                st.info(
                    "Proceeding to signatures / export… (wire this into your app navigation or PDF/email flow)."
                )
