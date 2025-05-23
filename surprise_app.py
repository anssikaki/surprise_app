import os
import logging 
import streamlit as st
from openai import OpenAI

st.write("test app")
# Example syntax for using OpenAI API
# api_key = st.secrets.get("openai", {}).get("api_key") or os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)
# response = client.chat.completions.create(
#             model='gpt-4o',
#             messages=[{'role': 'user', 'content': prompt}],
#             temperature=0.7,
#         )
# resp = response.choices[0].message.content
