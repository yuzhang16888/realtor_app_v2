# purchase_agreement/section4_sale_of_buyer_property.py

import streamlit as st

SECTION4_KEY = "pa_section4_sale_of_buyer_property"


def _init_section4_state():
    if SECTION4_KEY not in st.session_state:
        st.session_state[SECTION4_KEY] = {
            # Section 4 – Sale of Buyer’s Property (A/B choice)
            "is_contingent_on_sale": False,  # False = Option A, True = Option B

            # If contingent (Option B):
            "buyer_property_address": "",
            "buyer_property_status": "Not listed",
            "buyer_property_notes": "",

            # Section 5 – Addenda & Advisories (related to this contingency)
            "other_addenda_notes": "",
        }


def render_section4_sale_of_buyer_property():
    _init_section4_state()
    data = st.session_state[SECTION4_KEY]

    st.subheader("Section 4 & 5 – Subject to Sale of Buyer’s Property")

    st.markdown(
        "> This screen combines **Section 4 – Sale of Buyer’s Property** and the "
        "related portion of **Section 5 – Addenda and Advisories**. In most "
        "California transactions, the purchase is **not** contingent on the sale of "
        "another property. If it **is** contingent, a **C.A.R. Form COP** addendum "
        "is typically required and listed in the Addenda section."
    )

    # ---------------------------
    # 4. SALE OF BUYER'S PROPERTY
    # ---------------------------
    st.markdown("### 4. Sale of Buyer’s Property")

    st.markdown("**Which statement applies to Buyer?**")

    option_labels = {
        "A": (
            "A. This Agreement and Buyer’s ability to obtain financing are **NOT** "
            "contingent upon the sale of any property owned by Buyer."
        ),
        "B": (
            "B. This Agreement and Buyer’s ability to obtain financing **ARE** contingent "
            "upon the sale of property owned by Buyer as specified in the attached "
            "addendum (C.A.R. Form COP)."
        ),
    }

    current_option = "B" if data.get("is_contingent_on_sale") else "A"

    selected = st.radio(
        label="",
        options=["A", "B"],
        format_func=lambda x: option_labels[x],
        index=0 if current_option == "A" else 1,
    )

    data["is_contingent_on_sale"] = (selected == "B")

    if not data["is_contingent_on_sale"]:
        st.info(
            "You’ve selected **Option A**. The purchase is NOT contingent on the sale "
            "of any other property owned by Buyer."
        )
    else:
        st.warning(
            "You’ve selected **Option B**. The purchase IS contingent on the sale of "
            "another property owned by Buyer. A C.A.R. **Contingency for Sale of "
            "Buyer’s Property** (Form COP) should be prepared and attached."
        )

        st.markdown("#### Buyer’s Other Property Details")

        data["buyer_property_address"] = st.text_input(
            "Buyer’s property address (required for contingency):",
            value=data["buyer_property_address"],
            placeholder="e.g., 1234 Main Street, San Francisco, CA 94107",
        )

        status_options = [
            "Not listed",
            "Listed (Active)",
            "In contract / In escrow",
            "Pending close",
            "Recently closed (proceeds not received)",
        ]
        cur_status = data.get("buyer_property_status", status_options[0])
        if cur_status not in status_options:
            cur_status = status_options[0]

        data["buyer_property_status"] = st.selectbox(
            "Status of Buyer’s property:",
            status_options,
            index=status_options.index(cur_status),
        )

        data["buyer_property_notes"] = st.text_area(
            "Additional notes (optional):",
            value=data["buyer_property_notes"],
            height=100,
            placeholder=(
                "Example: Property is listed at $1,200,000 with ABC Realty. "
                "Expected close of escrow on or before March 15, 2026."
            ),
        )

        st.caption(
            "In the formal RPA, the specific terms of this contingency are handled in "
            "the attached **C.A.R. Form COP**. This screen just captures the key "
            "business points for drafting."
        )

    st.markdown("---")

    # ------------------------------------------
    # 5. ADDENDA AND ADVISORIES (related to 4)
    # ------------------------------------------
    st.markdown("### 5. Addenda and Advisories (Related to Sale of Buyer’s Property)")

    if data["is_contingent_on_sale"]:
        st.markdown(
            "- ✅ **C.A.R. Form COP – Contingency for Sale of Buyer’s Property**  "
            " *(Required because you selected Option B above.)*"
        )
    else:
        st.markdown(
            "- ☐ **C.A.R. Form COP – Contingency for Sale of Buyer’s Property**  "
            " *(Not required because you selected Option A above.)*"
        )

    data["other_addenda_notes"] = st.text_area(
        "Other addenda / advisories related to Buyer’s sale (optional):",
        value=data["other_addenda_notes"],
        height=100,
        placeholder=(
            "Example: Note if the Seller also requires a particular advisory, or if "
            "there are other related addenda you want listed in Section 5."
        ),
    )

    st.caption(
        "In the final Purchase Agreement draft, these selections will be reflected in "
        "the **Addenda and Advisories** section so the correct forms can be attached."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Section 4 & 5 – Subject to Sale of Buyer’s Property",
                     use_container_width=True):
            st.session_state[SECTION4_KEY] = data
            st.success("Section 4 & 5 – Subject to Sale of Buyer’s Property saved.")
    with col2:
        if st.button("⬅️ Back to Section 3 – Finance Terms", use_container_width=True):
            st.session_state[SECTION4_KEY] = data
            # Section 3 tab index = 2 (0-based: 0,1,2,3)
            st.session_state.active_pa_tab = 2
            st.info("Moved back to Section 3.")
