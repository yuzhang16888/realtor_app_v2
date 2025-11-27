# purchase_agreement/ai_helpers.py

from pathlib import Path
from functools import lru_cache
import json
from typing import Optional, Dict, Any

import streamlit as st
from openai import OpenAI


# ------------------------------
# 1. Load OpenAI client securely
# ------------------------------

def get_openai_client() -> OpenAI:
    """
    Securely load the OpenAI client using ONLY st.secrets.
    No API key will ever be written in code.
    """
    if "OPENAI_API_KEY" not in st.secrets:
        raise ValueError(
            "Missing OPENAI_API_KEY in Streamlit secrets.\n\n"
            "Go to your Streamlit deployment → Secrets → add:\n"
            "OPENAI_API_KEY = \"your-key-here\""
        )

    # Streamlit automatically exposes secrets as environment variables for OpenAI's SDK.
    return OpenAI()


# ------------------------------
# 2. Load your Knowledge Base
# ------------------------------

@lru_cache(maxsize=1)
def load_knowledge_text() -> str:
    """
    Load Knowledge/content.md as a single string.
    """
    this_file = Path(__file__).resolve()
    project_root = this_file.parent.parent  # go from /purchase_agreement → project root
    knowledge_path = project_root / "Knowledge" / "content.md"

    if knowledge_path.exists():
        return knowledge_path.read_text(encoding="utf-8")

    return ""


# ------------------------------
# 3. Helper to build section context
# ------------------------------

def _build_section_context(
    section: Optional[str],
    section_state: Optional[Dict[str, Any]],
) -> str:
    """
    Turn section id + section_state into a short context string for the model.
    """
    if not section and not section_state:
        return ""

    parts = []
    if section:
        parts.append(f"This conversation is about Section {section} of the CAR RPA.")

    if section_state:
        try:
            state_json = json.dumps(section_state, indent=2, default=str)
        except Exception:
            state_json = str(section_state)

        parts.append(
            "Here is the current structured data for this section of the offer. "
            "Use it only as context to tailor your explanation; do not just repeat it verbatim:\n"
            + state_json
        )

    return "\n\n".join(parts)


# ------------------------------
# 4. Main AI Helper
# ------------------------------

def call_purchase_agreement_ai(
    user_prompt: str,
    section: str = "7",
    section_state: Optional[Dict[str, Any]] = None,
    system_override: Optional[str] = None,
    model: str = "gpt-4.1-mini",
) -> str:
    """
    Main function all sections will use.

    - Calls GPT securely
    - Adds system instructions (your Realtor persona)
    - Adds your knowledge content
    - Optionally adds:
        * section_state as structured context
        * system_override as extra system instructions (e.g. default explainer text)
    - Returns the GPT answer as plain text
    """

    client = get_openai_client()
    knowledge_text = load_knowledge_text()

    # Base persona for AI Realtor
    base_system_prompt = f"""
You are an experienced California residential real estate agent and transaction coordinator.
You help buyers correctly understand and fill out the California Residential Purchase Agreement (CAR RPA).

You do NOT give legal advice, tax advice, or binding lending approvals.
Always recommend confirming details with a licensed real estate agent, lender, and/or California real estate attorney.
"""

    # Add knowledge base content if available
    if knowledge_text:
        base_system_prompt += f"""

You also have access to the following internal knowledge base.
Never say it is a file; simply use the info when helpful, especially for examples and explanations:

{knowledge_text}
"""

    # Add section-specific context
    section_context = _build_section_context(section, section_state)

    messages = [
        {"role": "system", "content": base_system_prompt.strip()},
    ]

    if section_context:
        messages.append(
            {
                "role": "system",
                "content": section_context,
            }
        )

    # Optional extra system instructions (e.g. Section 3 default explainer)
    if system_override:
        messages.append(
            {
                "role": "system",
                "content": system_override,
            }
        )

    # Finally, the actual user question
    messages.append(
        {"role": "user", "content": user_prompt.strip()}
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        # Friendly error string so the UI can display it
        return (
            "There was an error talking to the AI backend. "
            "Please try again, or check your API key / network.\n\n"
            f"Technical details: {e}"
        )
