import streamlit as st

def render_section16_20_info():
    """
    Combined info view for Sections 16–20.
    These are mostly informational / boilerplate type sections about:
    - Repairs / allocation of costs beyond the main ones
    - Taxes & withholding
    - Prorations, HOA fees, and other closing adjustments
    - Other default terms that usually are not heavily edited by buyers
    """

    st.markdown("## Sections 16–20 – Repairs, Taxes & Other Information")

    st.markdown(
        "These sections generally cover more detailed **information and default rules** about:\n"
        "- How certain repair responsibilities or obligations are handled beyond the main cost section.\n"
        "- Property taxes, supplemental taxes, and potential **withholding obligations** (for example, FIRPTA).\n"
        "- How items like HOA dues, property taxes, and rent (if any) are **prorated at closing**.\n"
        "- Some additional default terms that usually stay as written unless there is a special situation.\n\n"
        "Most buyers do **not** change these paragraphs, but it’s still useful to understand what they say."
    )

    st.markdown("---")

    st.markdown("### Section 16 – Repairs and Property-Related Items")
    st.markdown(
        "- May clarify who is responsible for certain **repairs or property conditions** "
        "that are not covered elsewhere.\n"
        "- Sometimes cross-references inspection or repair-related addenda."
    )

    with st.expander("📄 More about Section 16 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for more detailed language or explanation. You can paste specific CAR RPA text "
            "or your brokerage guidance here later._"
        )

    st.markdown("---")

    st.markdown("### Section 17 – Taxes & Withholding")
    st.markdown(
        "- Discusses **property taxes**, supplemental taxes, and potential **withholding requirements** "
        "when the seller is a non-resident, entity, or otherwise subject to tax withholding laws.\n"
        "- Important for sellers and escrow, but buyers should know that these items may appear in closing figures."
    )

    with st.expander("📄 More about Section 17 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for more detailed tax / withholding text or links. You can add more precise "
            "guidance from CAR, escrow, or tax professionals here later._"
        )

    st.markdown("---")

    st.markdown("### Section 18 – Prorations & Adjustments")
    st.markdown(
        "- Explains how items like **property taxes, HOA dues, rent, and other recurring charges** are "
        "**prorated between buyer and seller** as of the closing date.\n"
        "- Helps make sure each side pays their fair share for the period they own the property."
    )

    with st.expander("📄 More about Section 18 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for the detailed proration language from the contract. You can embed examples "
            "or escrow explanations here later._"
        )

    st.markdown("---")

    st.markdown("### Section 19–20 – Additional Boilerplate Items")
    st.markdown(
        "- Often include a mix of **miscellaneous provisions** or cross-references to other documents.\n"
        "- Typically do not require buyer edits, but are part of the legal framework of the agreement."
    )

    with st.expander("📄 More about Sections 19–20 (placeholder)", expanded=False):
        st.markdown(
            "_Placeholder for any remaining text or explanation about Sections 19–20. "
            "You can add more detail over time._"
        )

    st.markdown("---")

    st.info(
        "These sections are mostly **supporting details**. If you have a complex tax or ownership situation, "
        "your agent and escrow officer can help explain how these apply to your specific transaction."
    )
