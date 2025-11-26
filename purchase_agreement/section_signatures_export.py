# purchase_agreement/section_signatures_export.py

import streamlit as st
from datetime import datetime, date
from io import BytesIO


def _get_value(*keys, default="Not provided yet"):
    """
    Helper: safely pull the first non-empty value from st.session_state by
    trying multiple possible keys.
    """
    for key in keys:
        if key in st.session_state and st.session_state.get(key):
            return st.session_state.get(key)
    return default


def _format_expiration():
    """Format the expiration date/time from Section 31."""
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


def _build_offer_summary_text() -> str:
    """
    Build a plain-text summary of the key deal terms.
    This is used for PDF export and for email content.
    """

    buyer_1 = _get_value("pa_buyer_1_name", "buyer_1_name")
    buyer_2 = _get_value("pa_buyer_2_name", "buyer_2_name", default="(No second buyer)")

    property_address = _get_value(
        "pa_property_address",
        "property_address",
        "pa1_property_address",
    )

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
        "pa_financing_type",
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

    expiration_display = _format_expiration()

    lines = [
        "OFFER SUMMARY",
        "==============",
        "",
        "BUYER(S):",
        f"  Buyer 1: {buyer_1}",
        f"  Buyer 2: {buyer_2}",
        "",
        "PROPERTY:",
        f"  Address: {property_address}",
        "",
        "FINANCING TERMS:",
        f"  Offer Price: {purchase_price}",
        f"  Earnest Money / Initial Deposit: {earnest_money}",
        f"  Financing Type: {financing_type}",
        f"  Estimated Loan Amount: {loan_amount}",
        f"  Estimated Down Payment: {down_payment}",
        "",
        "CONTINGENCIES:",
        f"  Overall Contingency Period: {contingency_days} day(s) after acceptance",
        f"  Notes: {contingency_notes}",
        "",
        "OFFER EXPIRATION:",
        f"  Expires: {expiration_display}",
        "",
        "NOTE: This summary is for convenience only and does not replace the full contract.",
    ]

    return "\n".join(lines)


def _create_offer_summary_pdf(summary_text: str):
    """
    Create a simple PDF from the summary text.
    Returns bytes, or None if reportlab is not available.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except Exception:
        return None

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Basic text layout
    x_margin = 50
    y = height - 50

    for line in summary_text.split("\n"):
        c.drawString(x_margin, y, line)
        y -= 14
        if y < 50:  # new page if we run out of space
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def render_signatures_export():
    """
    Final step: Signatures & Export.

    - Shows key summary (who, where, how paying, contingencies, expiration).
    - Lets the user confirm they've reviewed.
    - Offers:
      * Download offer summary as PDF (if reportlab is available).
      * Prepare an email summary (UI placeholder – to be wired to backend).
    """

    st.markdown("## Signatures & Export")

    st.markdown(
        "This is the **final checkpoint** before your offer is signed and sent. "
        "Review the summary, confirm it looks right, then choose how you’d like to export it."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Key summary (read-only)
    # --------------------------------------------------
    st.markdown("### Key Terms Summary")

    summary_text = _build_offer_summary_text()

    # Show a nicely formatted version in the app
    st.text(summary_text)

    st.info(
        "This summary is for convenience only. The **actual contract** (RPA and any addenda) "
        "controls the terms of your offer."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Signature placeholders (not a legal e-sign system)
    # --------------------------------------------------
    st.markdown("### Buyer Signature Details (for your own records)")

    col_sig1, col_sig2 = st.columns(2)

    with col_sig1:
        buyer1_sig_name = st.text_input(
            "Buyer 1 – Name as it will appear on the contract",
            key="pa_sig_buyer1_name",
            value=_get_value("pa_buyer_1_name", "buyer_1_name", default=""),
        )
        buyer1_sig_date = st.date_input(
            "Buyer 1 – Signing Date",
            key="pa_sig_buyer1_date",
            value=date.today(),
        )

    with col_sig2:
        buyer2_sig_name = st.text_input(
            "Buyer 2 – Name (if any)",
            key="pa_sig_buyer2_name",
            value=_get_value("pa_buyer_2_name", "buyer_2_name", default=""),
        )
        buyer2_sig_date = st.date_input(
            "Buyer 2 – Signing Date (if any)",
            key="pa_sig_buyer2_date",
            value=date.today(),
        )

    st.caption(
        "These fields help you keep track of how your names and dates should appear. "
        "Actual legal signatures are usually handled through a secure e-sign platform "
        "like Glide, DocuSign, or your brokerage’s system."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Confirmation checkbox
    # --------------------------------------------------
    st.markdown("### Confirmation")

    confirm_reviewed = st.checkbox(
        "I have reviewed the summary above and it matches what I intend to offer.",
        key="pa_signatures_confirmed",
    )

    st.warning(
        "This app does **not** provide legal advice. Before signing or sending your offer, "
        "review the full contract with your real estate agent, and consult an attorney if you have questions."
    )

    st.markdown("---")

    # --------------------------------------------------
    # Export options: PDF + Email
    # --------------------------------------------------
    st.markdown("### Export Options")

    col_pdf, col_email = st.columns(2)

    # -------- PDF DOWNLOAD --------
    with col_pdf:
        pdf_bytes = _create_offer_summary_pdf(summary_text)

        if pdf_bytes is not None:
            st.download_button(
                label="📄 Download Offer Summary as PDF",
                data=pdf_bytes,
                file_name="offer_summary.pdf",
                mime="application/pdf",
                key="pa_download_offer_pdf",
            )
        else:
            st.info(
                "PDF generation library (`reportlab`) is not available in this environment. "
                "You can install it with `pip install reportlab` and restart the app to enable "
                "PDF downloads."
            )

    # -------- EMAIL UI (placeholder) --------
    with col_email:
        st.markdown("#### Email This Summary")

        email_to = st.text_input(
            "Send to (your email or your agent’s email)",
            key="pa_email_to",
            placeholder="you@example.com or agent@example.com",
        )

        email_note = st.text_area(
            "Optional note to include in the email",
            key="pa_email_note",
            height=100,
            placeholder="Example: Here is my draft offer summary. Please review and let me know your thoughts.",
        )

        send_email_clicked = st.button(
            "📧 Prepare Email Request",
            key="pa_send_email_btn",
        )

        if send_email_clicked:
            if not email_to.strip():
                st.error("Please provide at least one email address.")
            elif not confirm_reviewed:
                st.error(
                    "Please confirm you’ve reviewed the summary before sending it out."
                )
            else:
                # Placeholder – you can wire this to an email API or backend.
                st.session_state["pa_email_request"] = {
                    "to": email_to.strip(),
                    "note": email_note.strip(),
                    "summary_text": summary_text,
                }
                st.success(
                    "Email request prepared. Connect this to your backend or email service "
                    "to actually send the message."
                )

    st.markdown("---")

    # --------------------------------------------------
    # Done / Back buttons
    # --------------------------------------------------
    col_back, col_done = st.columns(2)

    with col_back:
        if st.button("⬅️ Go Back to Final Review", key="pa_signatures_back"):
            # Example: move back one tab if you use tab index
            # st.session_state['active_pa_tab'] = <index_of_final_review_tab>
            st.info("Returning to Final Review… (wire this into your navigation).")

    with col_done:
        if st.button("✅ I’m Done for Now", key="pa_signatures_done"):
            if not confirm_reviewed:
                st.error(
                    "Please confirm that you have reviewed the summary above before marking it as done."
                )
            else:
                st.success(
                    "Great work! Your offer details are captured. You can now coordinate with your "
                    "agent to send and sign the official contract."
                )
