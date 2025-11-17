# purchase_agreement/state.py

import streamlit as st

def init_purchase_agreement_state():
    """
    Ensure purchase_agreement + section state exist in session_state.
    """
    if "purchase_agreement" not in st.session_state:
        st.session_state.purchase_agreement = {}

    # Section 1
    if "section_1" not in st.session_state.purchase_agreement:
        st.session_state.purchase_agreement["section_1"] = {
            "buyer_names": "",
            "property_address": "",
            "city": "",
            "county": "",
            "zip_code": "",
            "apn": "",
            "purchase_price": None,
            "close_type": "days_after_acceptance",  # or "specific_date"
            "close_days_after": 30,
            "close_date": None,
            "human_summary": "",  # plain-English summary we generate
        }

    # Section 2 (Agency / Broker) – for now we assume no agent
    if "section_2" not in st.session_state.purchase_agreement:
        st.session_state.purchase_agreement["section_2"] = {
            "has_agent": False,
            "notes": "User assumed to have no agent; broker representation sections skipped for now.",
        }
