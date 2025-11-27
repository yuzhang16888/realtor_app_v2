# purchase_agreement/section1_offer.py

import streamlit as st
from datetime import date, timedelta
from purchase_agreement.state import init_purchase_agreement_state  # absolute import


def render_section_1_offer():
    """
    Main entry for Section 1 – Offer.
    Simple linear flow (no mode selector).
    """
    init_purchase_agreement_state()
    s1 = st.session_state.purchase_agreement["section_1"]

    st.markdown("### California Purchase Agreement – Section 1: Offer")
    # Anchor for "back to top" link
    st.markdown('<a name="section1_top"></a>', unsafe_allow_html=True)

    st.info(
        "In California, the Residential Purchase Agreement (RPA) is usually 10+ pages. "
        "Section 1 is the **foundation**: who is buying, what property, how much, "
        "and when you plan to close escrow."
    )

    _render_section_1_form(s1)
    # (We removed the old Live Summary on purpose)


def _render_section_1_form(s1: dict):
    """Single, guided form for Section 1."""

    # --- Step 1: Buyer names ---
    st.markdown("#### Step 1: Buyer name(s)")

    with st.expander("📄 Snapshot: Section 1 — OFFER (for reference)", expanded=False):
        st.markdown(
            """
            ```
            SECTION 1 — OFFER

            1A. Buyer: ____________________________

            1B. Property to be acquired:
                 Street Address: ____________________________
                 City: ______________   County: ______________   ZIP: ________
                 APN (optional): ____________________________

            1C. Purchase Price: $________________

            1D. Close of Escrow:
                 ☐ _____ Days After Acceptance
                 ☐ Specific Date: ______________
            ```
            """
        )

    with st.expander("What this means", expanded=True):
        st.write(
            "- This is the legal name of the person/people who will **own** the property.\n"
            "- It should match your ID and loan application.\n"
            "- If you’re buying with a partner or spouse, list everyone who should be on title."
        )

    s1["buyer_names"] = st.text_input(
        "Buyer full legal name(s)",
        value=s1.get("buyer_names", ""),
        placeholder="e.g. Jane Liu and David Chen",
    )

    # --- Step 2: Property details ---
    st.markdown("#### Step 2: Property details")

    with st.expander("What this means", expanded=True):
        st.write(
            "- This is the exact property you want to buy.\n"
            "- Use the same address as on the MLS listing or property tax record.\n"
            "- County and ZIP are used for title, tax records, and escrow.\n"
            "- APN (Assessor’s Parcel Number) is helpful, but optional for now."
        )

    col1, col2 = st.columns(2)
    with col1:
        s1["property_address"] = st.text_input(
            "Property street address",
            value=s1.get("property_address", ""),
            placeholder="123 Any Street #502",
        )
        s1["city"] = st.text_input(
            "City",
            value=s1.get("city", ""),
            placeholder="San Francisco",
        )
    with col2:
        s1["county"] = st.text_input(
            "County",
            value=s1.get("county", ""),
            placeholder="San Francisco",
        )
        s1["zip_code"] = st.text_input(
            "ZIP Code",
            value=s1.get("zip_code", ""),
            max_chars=10,
            placeholder="94107",
        )

    s1["apn"] = st.text_input(
        "APN (Assessor’s Parcel Number) – optional",
        value=s1.get("apn", ""),
        placeholder="Leave blank if unknown",
    )

    # --- Step 3: Purchase price ---
    st.markdown("#### Step 3: Purchase price")

    with st.expander("What this means", expanded=True):
        st.write(
            "- This is the total price you’re offering to pay for the property.\n"
            "- It becomes the base for your loan amount, earnest money deposit, and appraisal.\n"
            "- In competitive markets, offers may be above list price."
        )

    purchase_price = st.number_input(
        "Offer price (USD)",
        min_value=0,
        step=1000,
        value=s1.get("purchase_price") or 0,
        format="%d",
    )
    s1["purchase_price"] = int(purchase_price) if purchase_price else None

    # --- Step 4: Close of escrow ---
    st.markdown("#### Step 4: Close of escrow timing")

    with st.expander("What this means", expanded=True):
        st.write(
            "- This is the **target date** when the purchase completes and title transfers.\n"
            "- Common timelines:\n"
            "  - 30 days for financed offers\n"
            "  - 21–25 days for very strong financed buyers\n"
            "  - 10–14 days for all-cash buyers\n"
            "- Your lender must be able to meet this timeline."
        )

    close_type = st.radio(
        "How do you want to define the close of escrow for Section 1?",
        options=["Days after acceptance", "Specific calendar date"],
        index=0
        if s1.get("close_type", "days_after_acceptance") == "days_after_acceptance"
        else 1,
    )

    if close_type == "Days after acceptance":
        close_days = st.number_input(
            "Number of days after offer acceptance",
            min_value=5,
            max_value=90,
            step=1,
            value=s1.get("close_days_after", 30),
        )
        s1["close_type"] = "days_after_acceptance"
        s1["close_days_after"] = int(close_days)
        s1["close_date"] = None
    else:
        default_date = s1.get("close_date") or (date.today() + timedelta(days=30))
        close_date = st.date_input(
            "Target closing date",
            value=default_date,
        )
        s1["close_type"] = "specific_date"
        s1["close_date"] = close_date
        s1["close_days_after"] = None

    # 👉 NEW: sync a clean snapshot into st.session_state["pa_section1_offer"]
    _sync_section1_snapshot(s1)


def _sync_section1_snapshot(s1: dict):
    """
    Store a clean snapshot of Section 1 in a dedicated key so other sections
    (Section 3, Final Review, etc.) can read it reliably.
    """
    st.session_state["pa_section1_offer"] = {
        "buyer_names": s1.get("buyer_names"),
        "property_address": s1.get("property_address"),
        "city": s1.get("city"),
        "county": s1.get("county"),
        "zip_code": s1.get("zip_code"),
        "apn": s1.get("apn"),
        "purchase_price": s1.get("purchase_price"),
        "close_type": s1.get("close_type"),
        "close_days_after": s1.get("close_days_after"),
        "close_date": s1.get("close_date"),
    }
