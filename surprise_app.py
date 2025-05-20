_import os
import streamlit as st
from openai import OpenAI

api_key = st.secrets.get("openai", {}).get("api_key") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None
st.title("Placeholder App")
st.write("Configure OpenAI API key via `.streamlit/secrets.toml`:")
