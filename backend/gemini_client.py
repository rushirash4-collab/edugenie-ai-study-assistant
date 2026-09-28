"""
Google Gemini client configuration, model creation, and error interception.
"""

import os
import warnings
import streamlit as st

# Suppress library deprecation warnings for clean runtime logs
warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from typing import Optional


def resolve_api_key(user_input_key: str = "") -> str:
    """
    Resolves the Gemini API key through the defined hierarchy:
    1. Streamlit Secrets (st.secrets["GEMINI_API_KEY"])
    2. Environment Variable (os.getenv("GEMINI_API_KEY"))
    3. User Input from UI / session state
    """
    if user_input_key and user_input_key.strip():
        return user_input_key.strip()
    
    # Check Streamlit secrets
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass
    
    # Check environment variable
    env_key = os.getenv("GEMINI_API_KEY", "")
    if env_key and env_key.strip():
        return env_key.strip()
        
    return ""


def get_gemini_model(
    api_key: str,
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.7
) -> Optional[genai.GenerativeModel]:
    """Configures and returns a Gemini GenerativeModel instance with fallback handling."""
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        generation_config = {
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 4096,
        }
        
        # Valid production Google Gemini model candidates in order of preference
        candidate_models = [
            model_name,
            "gemini-1.5-flash",
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-flash-latest"
        ]
        
        # Deduplicate candidates while preserving order
        seen = set()
        deduped_candidates = [m for m in candidate_models if m and not (m in seen or seen.add(m))]
        
        for candidate in deduped_candidates:
            try:
                model = genai.GenerativeModel(model_name=candidate, generation_config=generation_config)
                return model
            except Exception:
                continue
                
        return genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
    except Exception as e:
        st.error(f"⚠️ Error configuring Gemini model: {str(e)}")
        return None


def handle_gemini_error(e: Exception) -> str:
    """Formats Gemini API errors with actionable feedback for rate limits and auth issues."""
    err_str = str(e)
    if "429" in err_str or "ResourceExhausted" in err_str or "quota" in err_str.lower():
        return "⚠️ **Rate Limit Exceeded:** You have reached the quota for this Gemini model. Please wait a moment before trying again or switch to `gemini-1.5-flash`."
    elif "403" in err_str or "API_KEY_INVALID" in err_str or "PERMISSION_DENIED" in err_str:
        return "🔑 **Invalid API Key:** The provided Google Gemini API Key is invalid or lacks proper permissions. Verify your key at [Google AI Studio](https://aistudio.google.com/app/apikey)."
    elif "503" in err_str or "ServiceUnavailable" in err_str:
        return "🔄 **Service Temporarily Unavailable:** Google AI services are experiencing temporary load. Please retry in a few seconds."
    return f"⚠️ **Generation Error:** {err_str}"
