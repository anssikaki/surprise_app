import streamlit as st
from openai import OpenAI

# Configure your page
st.set_page_config(page_title="Fun AI Playground", layout="wide")

# Initialize the OpenAI client (v1+)
client = OpenAI()

# App title and sidebar
st.markdown("# 🎉 Welcome to the Fun AI Playground!")
mode = st.sidebar.radio("Choose an activity:", ["Summarizer", "Joke Generator", "Haiku Writer"] )

# Summarizer feature
if mode == "Summarizer":
    st.header("📝 Text Summarizer")
    input_text = st.text_area("Enter the text you want to summarize:")
    if st.button("Summarize!"):
        if not input_text.strip():
            st.error("Please paste or write some text first.")
        else:
            with st.spinner("Summarizing..."):
                response = client.chat.completions.create(
                    model="gpt-4o",  # or gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": "You are a friendly assistant that provides concise summaries."},
                        {"role": "user",   "content": f"Summarize the following text:\n\n{input_text}"}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                summary = response.choices[0].message.content.strip()
            st.success(summary)

# Joke generator feature
elif mode == "Joke Generator":
    st.header("🤣 Joke Generator")
    if st.button("Tell me a joke!"):
        with st.spinner("Thinking of something funny..."):
            response = client.chat.completions.create(
                model="gpt-4o",  # or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a stand-up comedian with a knack for light-hearted, family-friendly humor."},
                    {"role": "user",   "content": "Tell me a funny, family-friendly joke."}
                ],
                temperature=0.9,
                max_tokens=150
            )
            joke = response.choices[0].message.content.strip()
        st.write(f"### {joke}")

# Haiku writer feature
elif mode == "Haiku Writer":
    st.header("🌸 Haiku Writer")
    topic = st.text_input("Enter a topic for your haiku (e.g., sunrise, forest, rainy day):")
    if st.button("Generate Haiku!"):
        if not topic.strip():
            st.error("Please provide a topic for your haiku.")
        else:
            with st.spinner("Composing haiku..."):
                response = client.chat.completions.create(
                    model="gpt-4o",  # or gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": "You are a poet specializing in traditional Japanese haiku."},
                        {"role": "user",   "content": f"Write a beautiful, evocative haiku about {topic}."}
                    ],
                    temperature=0.8,
                    max_tokens=50
                )
                haiku = response.choices[0].message.content.strip()
            st.markdown(f"---\n**{haiku}**\n---")
