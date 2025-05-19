import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]

# response = openai.ChatCompletion.create(
#    model="gpt-4o",
#    messages=[
#        {"role": "user", "content": "Summarize this text: " + input_text}
#    ]
#)

# st.write(response.choices[0].message.content)
