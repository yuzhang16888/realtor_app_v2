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
    # 🔹 Live Summary removed on purpose


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


def _render_section_1_summary(s1: dict):
    """Bottom summary + plain-English explanation + navigation."""
    if not s1.get("buyer_names") and not s1.get("property_address"):
        st.write("Fill in a few fields above and I’ll summarize Section 1 for you here.")
        return

    st.markdown("**Draft – Section 1: Offer**")

    st.write(
        f"- **Buyer(s):** {s1.get('buyer_names') or '—'}\n"
        f"- **Property:** {s1.get('property_address') or '—'}, "
        f"{s1.get('city') or ''} {s1.get('county') or ''} {s1.get('zip_code') or ''}\n"
        f"- **APN:** {s1.get('apn') or 'Not provided'}"
    )

    price_text = f"${s1['purchase_price']:,}" if s1.get("purchase_price") else "—"
    st.write(f"- **Purchase price:** {price_text}")

    if s1.get("close_type") == "days_after_acceptance":
        days = s1.get("close_days_after")
        st.write(
            f"- **Close of escrow:** {days} days after acceptance"
            if days
            else "- **Close of escrow:** —"
        )
    else:
        close_date = s1.get("close_date")
        st.write(
            f"- **Close of escrow:** {close_date.strftime('%b %d, %Y')}"
            if close_date
            else "- **Close of escrow:** —"
        )

    # Plain-English summary
    st.markdown("---")
    if st.button("✨ Generate plain-English summary of Section 1"):
        s1["human_summary"] = _generate_section_1_human_summary(s1)

    if s1.get("human_summary"):
        st.markdown("##### Plain-English Summary")
        st.write(s1["human_summary"])

    # Navigation: back to inputs / move to Section 2
    st.markdown("---")
    colA, colB = st.columns(2)

    with colA:
        # Markdown link that jumps to the top anchor
        st.markdown("**↺ Review Section 1 Inputs**  \n[Back to top](#section1_top)")

    with colB:
        st.markdown(
            "**Move to Section 2 →**  \n"
            "Next, click the **'Section 2 – Agency / Brokerage'** tab at the top."
        )

    st.caption(
        "This is a drafting summary only. It does not create a binding contract. "
        "A licensed real estate professional must transfer these terms into the official CAR RPA form."
    )


def _generate_section_1_human_summary(s1: dict) -> str:
    """Create a friendly, human-readable paragraph using the user's inputs."""
    buyer = s1.get("buyer_names") or "The buyer"
    address_parts = [
        s1.get("property_address") or "",
        s1.get("city") or "",
        s1.get("county") or "",
        s1.get("zip_code") or "",
    ]
    address = ", ".join([p for p in address_parts if p])

    price = s1.get("purchase_price")
    if price:
        price_text = f"${price:,.0f}"
    else:
        price_text = "a price to be determined"

    if s1.get("close_type") == "days_after_acceptance" and s1.get("close_days_after"):
        coe_text = f"{s1['close_days_after']} days after the seller accepts the offer"
    elif s1.get("close_type") == "specific_date" and s1.get("close_date"):
        coe_text = s1["close_date"].strftime("%B %d, %Y")
    else:
        coe_text = "on a date to be agreed between buyer and seller"

    apn_text = ""
    if s1.get("apn"):
        apn_text = f" (APN: {s1['apn']})"

    summary = (
        f"{buyer} are offering to purchase the property at {address}{apn_text}. "
        f"The proposed purchase price is {price_text}, "
        f"with a target close of escrow {coe_text}."
    )

    return summary
