# purchase_agreement/state.py

import streamlit as st

def init_purchase_agreement_state():
    """
    Ensure purchase_agreement + section_1 keys exist in session_state.
    Other sections (2, 3, etc.) can reuse the same purchase_agreement dict.
    """
    if "purchase_agreement" not in st.session_state:
        st.session_state.purchase_agreement = {}

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
        }
