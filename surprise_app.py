import streamlit as st
import requests
from openai import OpenAI

client = OpenAI(api_key=st.secrets.get("openai", {}).get("api_key", ""))
st.set_page_config(page_title="Empty page", layout="centered")
st.title("Empty page")

#try: 
#    response = client.chat.completions.create(
#                model="gpt-4o",
#                messages=[
#                    {"role": "system", "content": "You are a helpful assistant."},
#                    {"role": "user", "content": prompt}
#                ],
#                temperature=0.7,
#                max_tokens=200
#            )
#            st.write(response.choices[0].message.content.strip())
#except:
#            st.error("Failed to fetch AI insight.")
