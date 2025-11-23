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
        "Agreement. Use it for any additional business terms or conditions that are "
        "not already captured in Sections 1–5."
    )

    data["other_terms"] = st.text_area(
        "Other terms and conditions (optional):",
        value=data["other_terms"],
        height=200,
        key="sec6_other_terms_input",
        placeholder=(
            "Example: Buyer and Seller agree that Seller may remain in possession for "
            "up to 3 days after Close of Escrow under a separate occupancy agreement, "
            "or any other special terms you want reflected in the contract."
        ),
    )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "💾 Save Section 6 – Other Terms",
            key="sec6_save_btn",
            use_container_width=True,
        ):
            st.session_state[SECTION6_KEY] = data
            st.success("Section 6 – Other Terms saved.")
    with col2:
        if st.button(
            "➡️ Move to Section 7 – Allocation of Costs",
            key="sec6_next_sec7_btn",
            use_container_width=True,
        ):
            st.session_state[SECTION6_KEY] = data
            # Tab index 5 → Section 7 (0-based: 0..5)
            st.session_state.active_pa_tab = 5
            st.info("Moved to Section 7 – Allocation of Costs.")
