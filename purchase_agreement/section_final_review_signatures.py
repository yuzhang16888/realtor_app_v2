# purchase_agreement/section_final_review_signatures.py

import streamlit as st
from purchase_agreement.state import init_purchase_agreement_state


def render_final_review_signatures():
    """
    Final Review – pull key info from:
    - Section 1 (offer basics) via purchase_agreement["section_1"]
    - Section 3 (finance) via pa_section3_finance
    - (Optional) contingencies + expiration if available
    """
    # Ensure the purchase_agreement structure exists, same as Section 1 does
    init_purchase_agreement_state()

    st.markdown("## Final Review – Key Terms Snapshot")

    # ---- Section 1: who & what ----
    pa = st.session_state.get("purchase_agreement", {})
    s1 = pa.get("section_1", {})

    buyer_names = s1.get("buyer_names") or "Not entered yet"

    address_parts = [
        s1.get("property_address") or "",
        s1.get("city") or "",
        s1.get("county") or "",
        s1.get("zip_code") or "",
    ]
    address_str = ", ".join([p for p in address_parts if p])

    price = s1.get("purchase_price")
    price_text = f"${price:,.0f}" if price else "Not entered yet"

    if s1.get("close_type") == "days_after_acceptance" and s1.get("close_days_after"):
        coe_text = f"{s1['close_days_after']} days after acceptance"
    elif s1.get("close_type") == "specific_date" and s1.get("close_date"):
        coe_text = s1["close_date"].strftime("%B %d, %Y")
    else:
        coe_text = "Not specified yet"

    st.markdown("### 1. Buyer & Property")
    st.write(
        f"- **Buyer(s):** {buyer_names}\n"
        f"- **Property:** {address_str or 'Not entered yet'}\n"
        f"- **Purchase price:** {price_text}\n"
        f"- **Target close of escrow:** {coe_text}"
    )

    st.markdown("---")

    # ---- Section 3: finance snapshot ----
    s3 = st.session_state.get("pa_section3_finance", {})

    is_all_cash = bool(s3.get("is_all_cash"))
    initial_deposit = s3.get("initial_deposit_amount") or 0
    initial_deposit_text = f"${initial_deposit:,.0f}" if initial_deposit else "Not entered yet"

    first_loan_amount = s3.get("first_loan_amount") or 0
    second_loan_amount = s3.get("second_loan_amount") or 0
    total_loans = first_loan_amount + second_loan_amount

    if is_all_cash:
        financing_summary = "All-cash offer (no loan needed to close)."
    elif total_loans > 0:
        financing_summary = f"Financed offer with approximately ${total_loans:,.0f} in loans."
    else:
        financing_summary = "Financing details not completed yet."

    st.markdown("### 2. Financing & Deposit")
    st.write(
        f"- **Initial deposit (earnest money):** {initial_deposit_text}\n"
        f"- **Financing structure:** {financing_summary}"
    )
    st.caption(
        "This is a drafting summary based on your entries in Section 1 and Section 3. "
        "Always confirm final numbers with your lender and agent."
    )

    st.markdown("---")

    # ---- Contingencies (from Section 3, since you already track them there) ----
    has_loan_cont = s3.get("has_loan_contingency")
    has_appraisal_cont = s3.get("has_appraisal_contingency")
    loan_cont_days = s3.get("loan_contingency_days")
    appr_cont_days = s3.get("appraisal_contingency_days")

    contingencies_lines = []
    if has_loan_cont is True:
        if loan_cont_days:
            contingencies_lines.append(f"• Loan contingency – {loan_cont_days} days after acceptance")
        else:
            contingencies_lines.append("• Loan contingency – included")
    elif has_loan_cont is False:
        contingencies_lines.append("• Loan contingency – **removed**")

    if has_appraisal_cont is True:
        if appr_cont_days:
            contingencies_lines.append(f"• Appraisal contingency – {appr_cont_days} days after acceptance")
        else:
            contingencies_lines.append("• Appraisal contingency – included")
    elif has_appraisal_cont is False:
        contingencies_lines.append("• Appraisal contingency – **removed**")

    if not contingencies_lines:
        contingencies_lines.append("• Contingency details not fully entered yet.")

    st.markdown("### 3. Key Contingencies (Snapshot)")
    st.write("\n".join(contingencies_lines))

    st.markdown("---")

    # ---- Offer expiration – placeholder wiring for Section 31 ----
    s31 = st.session_state.get("pa_section31_expiration", {})
    expiration_summary = s31.get("expiration_summary") or (
        "Expiration details will appear here once wired from Section 31."
    )

    st.markdown("### 4. Offer Expiration (high-level)")
    st.write(expiration_summary)

    st.info(
        "If any of these look off, you can click back to the Core Deal Terms tab "
        "to adjust, then return here."
    )

    # Optional: tiny debug expander so you can see what state exists
    with st.expander("🔍 Debug – raw state (only for you as builder)", expanded=False):
        st.write("**purchase_agreement['section_1']**")
        st.json(s1)
        st.write("**pa_section3_finance**")
        st.json(s3)
