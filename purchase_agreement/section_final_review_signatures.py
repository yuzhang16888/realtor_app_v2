# purchase_agreement/section_final_review_signatures.py

import streamlit as st


def render_final_review_signatures():
    st.markdown("## Final Review – Key Terms Snapshot")

    # ---- Pull data from various sections safely ----
    pa = st.session_state.get("purchase_agreement", {})
    s1 = pa.get("section_1", {})                     # Section 1 – Offer
    s3 = st.session_state.get("pa_section3_finance", {})  # Section 3 – Finance
    # If you later add state keys for contingencies / expiration, you can read them here:
    s14 = st.session_state.get("pa_section14_contingencies", {})
    s31 = st.session_state.get("pa_section31_expiration", {})

    # ---- Section 1: Who is buying & what property ----
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

    # ---- Section 3: Financing snapshot ----
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

    # ---- (Optional) Contingencies from Section 14 ----
    # These keys will depend on how you structure Section 14.
    # For now we read them defensively and show a generic line if missing.
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

    # ---- Offer expiration (Section 31) – placeholder wiring ----
    # Adjust these keys to match however Section 31 stores its state.
    expiration_summary = s31.get("expiration_summary") or "Expiration details will appear here once wired from Section 31."

    # ==========================================================
    # DISPLAY LAYOUT
    # ==========================================================
    st.markdown("### 1. Buyer & Property")

    st.write(
        f"- **Buyer(s):** {buyer_names}\n"
        f"- **Property:** {address_str or 'Not entered yet'}\n"
        f"- **Purchase price:** {price_text}\n"
        f"- **Target close of escrow:** {coe_text}"
    )

    st.markdown("---")

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

    st.markdown("### 3. Key Contingencies (Snapshot)")

    st.write("\n".join(contingencies_lines))

    st.markdown("---")

    st.markdown("### 4. Offer Expiration (high-level)")

    st.write(expiration_summary)

    st.info(
        "If any of these look off, you can click back to the relevant tab "
        "(Core Deal Terms, Contingencies, or Expiration) to adjust, then return here."
    )
