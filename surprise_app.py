import streamlit as st
from openai import OpenAI

# Configure your page
st.set_page_config(page_title="Fun AI Playground", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .feature-box { background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    .output-box { background-color: #ffffff; padding: 15px; border-left: 5px solid #4CAF50; border-radius: 5px; margin-top: 10px; }
    .haiku-box { background-color: #fff8e1; padding: 15px; border-left: 5px solid #FFC107; border-radius: 5px; margin-top: 10px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True
)

# Initialize the OpenAI client with API key
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Session state for joke history to avoid repeats
if 'jokes' not in st.session_state:
    st.session_state.jokes = []

# App title and sidebar
st.sidebar.title("🎉 Fun AI Playground")
mode = st.sidebar.radio("Choose an activity:", ["Summarizer", "Joke Generator", "Haiku Writer"] )

# Main container
st.markdown("# Welcome!")

# Summarizer feature
if mode == "Summarizer":
    with st.container():
        st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
        st.header("📝 Text Summarizer")
        input_text = st.text_area("Paste or write text here...")
        if st.button("Summarize"):
            if not input_text.strip():
                st.error("Please enter some text first.")
            else:
                with st.spinner("Summarizing..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a friendly assistant that provides concise summaries."},
                            {"role": "user",   "content": f"Summarize the following text:\n\n{input_text}"}
                        ],
                        temperature=0.7,
                        max_tokens=200
                    )
                    summary = response.choices[0].message.content.strip()
                st.markdown(f"<div class='output-box'>{summary}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Joke generator feature
elif mode == "Joke Generator":
    with st.container():
        st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
        st.header("🤣 Joke Generator")
        if st.button("Tell me a joke!"):
            with st.spinner("Thinking..."):
                # Attempt to get a non-repeated joke
                attempts = 0
                joke = ""
                while attempts < 3:
                    resp = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a stand-up comedian who always provides a new, family-friendly joke."},
                            {"role": "user",   "content": "Tell me a funny, family-friendly joke."}
                        ],
                        temperature=0.9,
                        max_tokens=150
                    )
                    joke = resp.choices[0].message.content.strip()
                    if joke not in st.session_state.jokes:
                        st.session_state.jokes.append(joke)
                        break
                    attempts += 1
                st.markdown(f"<div class='output-box'>{joke}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Haiku writer feature
elif mode == "Haiku Writer":
    with st.container():
        st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
        st.header("🌸 Haiku Writer")
        topic = st.text_input("Topic for haiku (e.g., sunrise, forest, rainy day):")
        if st.button("Generate Haiku"):
            if not topic.strip():
                st.error("Please provide a topic.")
            else:
                with st.spinner("Composing haiku..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a poet specializing in traditional Japanese haiku."},
                            {"role": "user",   "content": f"Write a beautiful, evocative haiku about {topic}."}
                        ],
                        temperature=0.8,
                        max_tokens=50
                    )
                    haiku = response.choices[0].message.content.strip()
                st.markdown(f"<div class='haiku-box'>{haiku}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
