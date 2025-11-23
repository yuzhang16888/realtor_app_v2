# purchase_agreement/section6_other_terms.py

import streamlit as st

SECTION6_KEY = "pa_section6_other_terms"


def _init_section6_state():
    if SECTION6_KEY not in st.session_state:
        st.session_state[SECTION6_KEY] = {
            "other_terms": "",
        }


def render_section6_other_terms():
    _init_section6_state()
    data = st.session_state[SECTION6_KEY]

    st.subheader("Section 6 – Other Terms")

    st.markdown(
        "> This section corresponds to **Section 6 – Other Terms** in the Purchase "
        "Agreement. It is used for any additional terms and conditions that are not "
        "captured elsewhere in the contract."
    )

    data["other_terms"] = st.text_area(
        "Other terms and conditions (optional):",
        value=data["other_terms"],
        height=180,
        placeholder=(
            "Example: Buyer and Seller agree that seller may remain in possession "
            "for up to 3 days after Close of Escrow under a separate occupancy "
            "agreement, or any other special terms you want reflected in the contract."
        ),
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Section 6 – Other Terms", use_container_width=True):
            st.session_state[SECTION6_KEY] = data
            st.success("Section 6 – Other Terms saved.")
    with col2:
        if st.button("➡️ Move to Section 7 – Allocation of Costs", use_container_width=True):
            st.session_state[SECTION6_KEY] = data
            # Tab index 5 → Section 7 (0-based: 0..5)
            st.session_state.active_pa_tab = 6
            st.info("Moved to Section 7 – Allocation of Costs.")
