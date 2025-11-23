# -----------------------
# 7A. Inspections, Reports
# -----------------------
st.markdown("### 7A. Inspections, Reports and Certificates")

# Move AI button RIGHT HERE
_render_ai_insight_block("7A", "Inspections, Reports and Certificates")

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
