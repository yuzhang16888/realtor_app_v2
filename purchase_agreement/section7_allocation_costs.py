import streamlit as st

SECTION7_KEY = "pa_section7_allocation_costs"
AI_INSIGHT_KEY = "pa_section7_ai_insights"  # holds AI text per subsection (7A–7D)


def _init_section7_state():
    if SECTION7_KEY not in st.session_state:
        st.session_state[SECTION7_KEY] = {
            # 7A – Inspections / reports
            "nhd_payer": "Seller",
            "nhd_provider": "",
            "other_report_1_desc": "",
            "other_report_1_payer": "Buyer",
            "other_report_2_desc": "",
            "other_report_2_payer": "Buyer",

            # 7B – Government requirements & retrofit
            "smoke_co_payer": "Seller",
            "other_gov_retrofit_desc": "",
            "other_gov_retrofit_payer": "Buyer",

            # 7C – Escrow & title
            "escrow_fee_payer": "50/50",
            "escrow_holder_name": "",
            "owners_title_payer": "Seller",
            "title_company_name": "",

            # 7D – Transfer taxes, HOA, other costs
            "county_transfer_tax_payer": "Seller",
            "city_transfer_tax_payer": "Seller",
            "hoa_transfer_fee_payer": "Buyer",
            "hoa_docs_4525_payer": "Seller",
            "hoa_other_docs_payer": "Buyer",
            "hoa_cert_fee_payer": "Buyer",
            "private_transfer_fee_payer": "Seller",
            "other_cost_desc_1": "",
            "other_cost_1_payer": "Buyer",
            "other_cost_desc_2": "",
            "other_cost_2_payer": "Buyer",

            # 7E – Home warranty
            "home_warranty_included": True,
            "home_warranty_max_cost": 600.0,
            "home_warranty_company": "",
            "home_warranty_air_con": False,
            "home_warranty_pool_spa": False,
            "home_warranty_other_cov": "",
        }

    if AI_INSIGHT_KEY not in st.session_state:
        # Holds text like {"7A": "AI answer...", "7B": "...", ...}
        st.session_state[AI_INSIGHT_KEY] = {}


def _payer_radio(label: str, key: str, data: dict, widget_key: str):
    options = ["Buyer", "Seller", "50/50", "Other"]
    current = data.get(key, options[0])
    if current not in options:
        current = options[0]
    data[key] = st.radio(
        label,
        options=options,
        index=options.index(current),
        horizontal=True,
        key=widget_key,
    )


def _render_ai_insight_block(subsection_code: str, title: str):
    """
    Reusable UI for the 'Ask AI Realtor' block per subsection (7A–7D).
    - subsection_code: "7A", "7B", etc.
    - title: short label to show in the insight box.
    """
    ai_state = st.session_state[AI_INSIGHT_KEY]

    ask_label = f"Ask AI Realtor about {subsection_code}"
    if st.button(
        ask_label,
        key=f"btn_ai_{subsection_code}",
        use_container_width=False,
    ):
        # TODO: Replace this placeholder with a real GPT call + Knowledge retrieval.
        ai_state[subsection_code] = (
            f"**AI insight – {subsection_code}. {title}**  \n"
            "This is a placeholder. In the next step, you can connect this button to "
            "your tuned GPT model and Knowledge folder to provide local norms, pros "
            "and cons, and negotiation tips for this cost allocation item."
        )

    if subsection_code in ai_state and ai_state[subsection_code]:
        st.markdown(ai_state[subsection_code])
        if st.button(
            f"Close AI insights for {subsection_code}",
            key=f"btn_close_ai_{subsection_code}",
            use_container_width=False,
        ):
            ai_state[subsection_code] = ""


def render_section7_allocation_costs():
    _init_section7_state()
    data = st.session_state[SECTION7_KEY]

    st.subheader("Section 7 – Allocation of Costs")

    st.markdown(
        "> This section mirrors the **Allocation of Costs** portion of the "
        "California Residential Purchase Agreement (RPA). It summarizes who pays "
        "for inspections, government-required items, escrow and title fees, "
        "transfer taxes, HOA-related charges, and any home warranty plan.\n\n"
        "Use the radios below to set who will pay for each item. You can also click "
        "**“Ask AI Realtor”** in each subsection to get additional context and "
        "practice-based guidance (which you can later power with your own Knowledge "
        "folder and tuned GPT model)."
    )

    # -----------------------
    # 7A. Inspections, Reports
    # -----------------------
    st.markdown("### 7A. Inspections, Reports and Certificates")

    _payer_radio(
        "Natural Hazard Disclosure (NHD) report",
        "nhd_payer",
        data,
        widget_key="sec7_nhd_payer_radio",
    )

    data["nhd_provider"] = st.text_input(
        "NHD provider (optional):",
        value=data["nhd_provider"],
        key="sec7_nhd_provider_input",
        placeholder="e.g., JCP-LGS, Property I.D., First American NHD",
    )

    st.markdown("**Other reports (optional)**")
    col1, col2 = st.columns(2)
    with col1:
        data["other_report_1_desc"] = st.text_input(
            "Report 1 description:",
            value=data["other_report_1_desc"],
            key="sec7_other_report1_desc_input",
            placeholder="e.g., Roof inspection, Sewer lateral inspection",
        )
    with col2:
        _payer_radio(
            "Report 1 payer",
            "other_report_1_payer",
            data,
            widget_key="sec7_other_report1_payer_radio",
        )

    col1, col2 = st.columns(2)
    with col1:
        data["other_report_2_desc"] = st.text_input(
            "Report 2 description:",
            value=data["other_report_2_desc"],
            key="sec7_other_report2_desc_input",
            placeholder="Optional second report",
        )
    with col2:
        _payer_radio(
            "Report 2 payer",
            "other_report_2_payer",
            data,
            widget_key="sec7_other_report2_payer_radio",
        )

    st.caption(
        "These items cover third-party reports and inspections that may be obtained "
        "before or during escrow."
    )

    _render_ai_insight_block("7A", "Inspections, Reports and Certificates")

    st.markdown("---")

    # ------------------------------------
    # 7B. Government Requirements/Retrofit
    # ------------------------------------
    st.markdown("### 7B. Government Requirements and Retrofit")

    _payer_radio(
        "Smoke alarm and carbon monoxide device installation (if required)",
        "smoke_co_payer",
        data,
        widget_key="sec7_smoke_co_payer_radio",
    )

    col1, col2 = st.columns(2)
    with col1:
        data["other_gov_retrofit_desc"] = st.text_input(
            "Other local retrofit / compliance work (optional):",
            value=data["other_gov_retrofit_desc"],
            key="sec7_other_gov_retrofit_desc_input",
            placeholder="e.g., Low-flow toilets, seismic gas shutoff valve",
        )
    with col2:
        _payer_radio(
            "Payer for other retrofit work",
            "other_gov_retrofit_payer",
            data,
            widget_key="sec7_other_gov_retrofit_payer_radio",
        )

    st.caption(
        "Local jurisdictions may require specific retrofit items as a condition of "
        "closing (e.g., water heater bracing, low-flow fixtures, gas shutoff valves)."
    )

    _render_ai_insight_block("7B", "Government Requirements and Retrofit")

    st.markdown("---")

    # -----------------------
    # 7C. Escrow and Title
    # -----------------------
    st.markdown("### 7C. Escrow and Title")

    _payer_radio(
        "Escrow fee",
        "escrow_fee_payer",
        data,
        widget_key="sec7_escrow_fee_payer_radio",
    )

    data["escrow_holder_name"] = st.text_input(
        "Escrow holder (company / office):",
        value=data["escrow_holder_name"],
        key="sec7_escrow_holder_name_input",
        placeholder="e.g., First American Title – San Francisco",
    )

    _payer_radio(
        "Owner’s title insurance policy",
        "owners_title_payer",
        data,
        widget_key="sec7_owners_title_payer_radio",
    )

    data["title_company_name"] = st.text_input(
        "Title company (for owner’s policy):",
        value=data["title_company_name"],
        key="sec7_title_company_name_input",
        placeholder="e.g., Chicago Title, Old Republic, First American",
    )

    st.caption(
        "Escrow and title fees can be paid by Buyer, Seller, or split. Custom varies "
        "by county and sometimes by city."
    )

    _render_ai_insight_block("7C", "Escrow and Title")

    st.markdown("---")

    # ---------------------------------------
    # 7D. Transfer Taxes, HOA, and Other Costs
    # ---------------------------------------
    st.markdown("### 7D. Transfer Taxes, HOA, and Other Costs")

    st.markdown("**Transfer taxes**")
    _payer_radio(
        "County transfer tax / fee",
        "county_transfer_tax_payer",
        data,
        widget_key="sec7_county_transfer_tax_payer_radio",
    )

    _payer_radio(
        "City transfer tax / fee",
        "city_transfer_tax_payer",
        data,
        widget_key="sec7_city_transfer_tax_payer_radio",
    )

    st.markdown("**HOA-related fees (if applicable)**")
    _payer_radio(
        "HOA transfer fee",
        "hoa_transfer_fee_payer",
        data,
        widget_key="sec7_hoa_transfer_fee_payer_radio",
    )

    _payer_radio(
        "HOA fees for Civil Code §4525 required documents",
        "hoa_docs_4525_payer",
        data,
        widget_key="sec7_hoa_docs_4525_payer_radio",
    )

    _payer_radio(
        "HOA fees for other HOA documents (non-§4525)",
        "hoa_other_docs_payer",
        data,
        widget_key="sec7_hoa_other_docs_payer_radio",
    )

    _payer_radio(
        "HOA certification fee",
        "hoa_cert_fee_payer",
        data,
        widget_key="sec7_hoa_cert_fee_payer_radio",
    )

    st.markdown("**Other costs**")
    col1, col2 = st.columns(2)
    with col1:
        data["private_transfer_fee_payer"] = st.radio(
            "Private transfer fee (if any)",
            options=["Buyer", "Seller", "50/50", "Other"],
            index=["Buyer", "Seller", "50/50", "Other"].index(
                data.get("private_transfer_fee_payer", "Seller")
                if data.get("private_transfer_fee_payer", "Seller") in ["Buyer", "Seller", "50/50", "Other"]
                else "Seller"
            ),
            horizontal=True,
            key="sec7_private_transfer_fee_payer_radio",
        )
    with col2:
        pass

    col1, col2 = st.columns(2)
    with col1:
        data["other_cost_desc_1"] = st.text_input(
            "Other cost 1 description (optional):",
            value=data["other_cost_desc_1"],
            key="sec7_other_cost1_desc_input",
            placeholder="e.g., Home inspection re-inspection fee",
        )
    with col2:
        _payer_radio(
            "Other cost 1 payer",
            "other_cost_1_payer",
            data,
            widget_key="sec7_other_cost1_payer_radio",
        )

    col1, col2 = st.columns(2)
    with col1:
        data["other_cost_desc_2"] = st.text_input(
            "Other cost 2 description (optional):",
            value=data["other_cost_desc_2"],
            key="sec7_other_cost2_desc_input",
            placeholder="e.g., City resale inspection fee",
        )
    with col2:
        _payer_radio(
            "Other cost 2 payer",
            "other_cost_2_payer",
            data,
            widget_key="sec7_other_cost2_payer_radio",
        )

    st.caption(
        "Transfer taxes and HOA-related fees often follow local custom and are a "
        "common point of negotiation, especially in competitive markets."
    )

    _render_ai_insight_block("7D", "Transfer Taxes, HOA, and Other Costs")

    st.markdown("---")

    # -----------------------
    # 7E. Home Warranty Plan
    # -----------------------
    st.markdown("### 7E. Home Warranty Plan")

    data["home_warranty_included"] = st.checkbox(
        "Include a one-year home warranty plan",
        value=bool(data["home_warranty_included"]),
        key="sec7_home_warranty_included_checkbox",
    )

    if data["home_warranty_included"]:
        col1, col2 = st.columns(2)
        with col1:
            data["home_warranty_max_cost"] = st.number_input(
                "Maximum cost of home warranty plan ($)",
                min_value=0.0,
                value=float(data["home_warranty_max_cost"]),
                step=50.0,
                format="%.2f",
                key="sec7_home_warranty_max_cost_input",
            )
        with col2:
            data["home_warranty_company"] = st.text_input(
                "Home warranty company (optional):",
                value=data["home_warranty_company"],
                key="sec7_home_warranty_company_input",
                placeholder="e.g., Old Republic, First American Home Warranty",
            )

        st.markdown("**Optional coverages**")
        col1, col2, col3 = st.columns(3)
        with col1:
            data["home_warranty_air_con"] = st.checkbox(
                "Air conditioning",
                value=bool(data["home_warranty_air_con"]),
                key="sec7_home_warranty_air_con_checkbox",
            )
        with col2:
            data["home_warranty_pool_spa"] = st.checkbox(
                "Pool / Spa",
                value=bool(data["home_warranty_pool_spa"]),
                key="sec7_home_warranty_pool_spa_checkbox",
            )
        with col3:
            data["home_warranty_other_cov"] = st.text_input(
                "Other coverage (optional):",
                value=data["home_warranty_other_cov"],
                key="sec7_home_warranty_other_cov_input",
                placeholder="e.g., Roof coverage, Washer/Dryer",
            )

        st.caption(
            "Home warranty plans differ in coverage and exclusions. Buyer should "
            "review the plan details to determine which coverages are appropriate."
        )
    else:
        st.info(
            "Buyer is choosing to **waive** a one-year home warranty plan in this "
            "draft. This does not prevent Buyer from purchasing a plan separately."
        )

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "💾 Save Section 7 – Allocation of Costs",
            key="sec7_save_btn",
            use_container_width=True,
        ):
            st.session_state[SECTION7_KEY] = data
            st.success("Section 7 – Allocation of Costs saved.")
    with col2:
        if st.button(
            "⬅️ Back to Section 6 – Other Terms",
            key="sec7_back_to_sec6_btn",
            use_container_width=True,
        ):
            st.session_state[SECTION7_KEY] = data
            # Tab index 4 = Section 6 – Other Terms (0-based)
            st.session_state.active_pa_tab = 4
            st.info("Moved back to Section 6 – Other Terms.")
