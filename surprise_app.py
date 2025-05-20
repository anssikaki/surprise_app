import streamlit as st
from openai import OpenAI

api_key = st.secrets.get("openai", {}).get("api_key", "")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Empty page")
st.title("Empty page")
