# purchase_agreement/section2_agency.py

import streamlit as st
from purchase_agreement.state import init_purchase_agreement_state

SNAPSHOT_IMAGE_PATH = "assets/section2_agency_snapshot.png"  # optional image path


def render_section_2_agency():
    """Section 2 – Agency / Broker Representation. For now we assume no agent."""
    init_purchase_agreement_state()
    s2 = st.session_state.purchase_agreement["section_2"]

    st.markdown("### Section 2 – Agency and Brokerage (Assuming No Agent)")

    st.info(
        "This part of the California RPA identifies the real estate brokers and agents "
        "who represent the buyer and seller. Since we're assuming you **do not have an agent** "
        "right now, we’ll skip the detailed inputs and treat you as an unrepresented buyer for drafting purposes."
    )

    # Try to show image snapshot first, fallback to text snapshot
    st.markdown("#### Snapshot of Section 2 (for context)")

    image_shown = False
    try:
        # If you add a real image file later, this will show it.
        st.image(SNAPSHOT_IMAGE_PATH, caption="Excerpt: Section 2 – Agency / Brokerage", use_container_width=True)
        image_shown = True
    except Exception:
        image_shown = False

    if not image_shown:
        with st.expander("📄 Text snapshot: Section 2 — Agency (for reference)", expanded=False):
            st.markdown(
                """
                ```
                SECTION 2 — AGENCY

                2A. Listing Broker (Seller's Broker):
                    Firm: ____________________________
                    License #: _______________________
                    Agent: ___________________________
                    DRE License #: ___________________

                2B. Buyer’s Broker:
                    Firm: ____________________________
                    License #: _______________________
                    Agent: ___________________________
                    DRE License #: ___________________

                2C. Agency relationships and disclosures are described here.
                ```
                """
            )

    st.markdown("#### How we’re handling this section right now")

    st.write(
        "- Because you’re using this tool as a **direct buyer** without naming a broker, we will:\n"
        "  - Leave the broker/agent lines blank in the internal draft.\n"
        "  - Treat you as an unrepresented buyer for drafting and explanation purposes.\n\n"
        "If you later work with a licensed agent or broker, they can fill in this section correctly "
        "with their firm name, license number, and DRE info."
    )

    # For now we just lock it to "no agent"
    s2["has_agent"] = False
    s2["notes"] = (
        "User is proceeding as an unrepresented buyer. "
        "Broker/agent fields to be completed later by a licensed real estate professional."
    )

    st.success(
        "Section 2 has been noted as 'no agent currently identified'. "
        "We’ll move on under the assumption that broker details will be added later by a professional."
    )
