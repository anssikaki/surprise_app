import streamlit as st
from openai import OpenAI, OpenAIError

# Initialize OpenAI client
try:
    api_key = st.secrets.get("openai", {}).get("api_key", "")
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("🔑 OpenAI API key not found. Please set it in Streamlit secrets.")
    st.stop()

# Page configuration and theming
st.set_page_config(page_title="🚀 Press Release from the Future", layout="wide")
st.markdown("""
<style>
body {background-color: #f0f2f6;}
.stButton>button {border-radius: 8px;}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 Press Release from the Future")
st.write("_Craft playful, visionary press releases—then chat with them!_")

# Input form
with st.form(key="input_form"):
    company = st.text_input("🏢 Company Name", placeholder="e.g. SpaceEgg Inc.")
    product = st.text_input("✨ Product / Idea", placeholder="e.g. Quantum Toaster")
    year = st.number_input("📅 Future Year", min_value=2025, max_value=2100, value=2030)
    generate = st.form_submit_button("✨ Generate Press Release")

# Core interaction
if generate:
    if not company.strip() or not product.strip():
        st.error("Please fill in both company and product/idea. 🤚")
    else:
        # Visual flourish
        st.balloons()
        prompt = (
            f"Write a whimsical, visionary corporate press release as if it were published in {year} by {company}, "
            f"announcing their revolutionary {product}. "
            "Add humor, bold visuals, executive quotes, and a dash of futuristic vision. "
            "Include an engaging headline, key specs, market outlook, and potential societal impact—make it playful!"
        )
        with st.spinner("🖋️ Crafting avant-garde press release..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a witty, visionary press release writer who loves humor and futuristic flair."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.85,
                    max_tokens=600,
                )
                release = response.choices[0].message.content.strip()
                st.subheader("📰 Your Future Press Release")
                st.markdown(release)

                # Initialize chat state
                if "messages" not in st.session_state:
                    st.session_state.messages = [
                        {"role": "system", "content": "You are now chatting as the press release content. Respond playfully and in-character."},
                        {"role": "assistant", "content": release}
                    ]

                # Chat interface
                st.divider()
                st.subheader("💬 Chat with Your Press Release")
                user_msg = st.text_input("Ask the press release anything:")
                if user_msg:
                    st.session_state.messages.append({"role": "user", "content": user_msg})
                    with st.spinner("🤖 Thinking..."):
                        chat_resp = client.chat.completions.create(
                            model="gpt-4o",
                            messages=st.session_state.messages,
                            temperature=0.7,
                            max_tokens=300,
                        )
                        answer = chat_resp.choices[0].message.content.strip()
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        st.markdown(f"**Press Release says:** {answer}")

                # Visual concept art
                st.divider()
                st.subheader("🖼️ Generate Concept Art")
                if st.button("Create Futuristic Concept Image"):
                    image_prompt = f"High-definition illustration in vibrant neon of {company}'s {product} in the year {year}, visionary, sleek, futuristic style"
                    with st.spinner("🎨 Rendering image..."):
                        try:
                            img_resp = client.images.generate(
                                prompt=image_prompt,
                                size="1024x1024",
                                n=1
                            )
                            img_url = img_resp.data[0].url
                            st.image(img_url, caption="Concept Art", use_column_width=True)
                        except OpenAIError as e:
                            st.error(f"Image generation failed: {e}")

            except OpenAIError as e:
                st.error(f"Failed to generate press release: {e}")
