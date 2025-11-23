# purchase_agreement/ai_helpers.py

from pathlib import Path
from functools import lru_cache

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
# 3. Main AI Helper
# ------------------------------

def call_purchase_agreement_ai(user_prompt: str, section: str = "7") -> str:
    """
    Main function Section 7 will use.
    - Calls GPT securely
    - Adds system instructions
    - Adds your knowledge content
    - Returns the GPT answer
    """

    client = get_openai_client()
    knowledge_text = load_knowledge_text()

    system_prompt = f"""
You are an experienced California residential real estate agent and transaction coordinator.
You help buyers correctly understand and fill out the California Residential Purchase Agreement (CAR RPA).
This conversation is about Section {section} of the agreement.

You do NOT give legal advice.
Always recommend confirming details with a licensed agent or attorney.
"""

    if knowledge_text:
        system_prompt += f"""

You also have access to the following internal knowledge base. 
Never say it is a file; simply use the info when helpful:

{knowledge_text}
"""

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt.strip()},
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.3,
    )

    return response.choices[0].message.content
