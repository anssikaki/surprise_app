import os
import logging
import streamlit as st
from openai import OpenAI

# --- UPM inspired style ----------------------------------------------------
UPM_PRIMARY_COLOR = "#009639"  # Approximated UPM green
UPM_STYLE = f"""
    <style>
        .stApp {{
            background-color: #f5f5f5;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {UPM_PRIMARY_COLOR};
        }}
        .css-1cpxqw2 {{
            color: {UPM_PRIMARY_COLOR};
        }}
        .stButton>button {{
            background-color: {UPM_PRIMARY_COLOR};
            color: white;
        }}
    </style>
"""

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Retrieve OpenAI API key from Streamlit secrets or environment variable
api_key = st.secrets.get("openai", {}).get("api_key") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# Apply UPM styling
st.set_page_config(page_title="UPM Futuristic Press Release")
st.markdown(UPM_STYLE, unsafe_allow_html=True)

# Initialize session state for conversation
if "press_release" not in st.session_state:
    st.session_state["press_release"] = ""
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("UPM Press Release from the Future")

st.write("Enter details about the company and select a future year to generate a press release written from that perspective.")

company_name = st.text_input("Company name")
future_year = st.number_input("Future year", min_value=2024, max_value=3000, value=2050, step=1)
additional_details = st.text_area("Additional details or achievements")

if st.button("Generate press release"):
    if not client:
        st.error("OpenAI API key is missing. Please set it in Streamlit secrets or as an environment variable named OPENAI_API_KEY.")
    elif not company_name:
        st.error("Please provide a company name.")
    else:
        prompt = (
            f"Write a press release from the year {future_year} about {company_name}. "
            f"Include the following details if relevant: {additional_details}. "
            "Make it futuristic, engaging, and optimistic."
        )
        logger.info("Generating press release for %s (%s)", company_name, future_year)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative press release writer from the future."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8
            )
            press_release = response.choices[0].message.content.strip()
            logger.debug("Press release content: %s", press_release)
            st.session_state["press_release"] = press_release
            st.session_state["messages"] = [
                {"role": "assistant", "content": press_release}
            ]
            st.subheader("Generated Press Release")
            st.write(press_release)
        except Exception as exc:
            logger.exception("Error while generating press release: %s", exc)
            st.error(f"An error occurred: {exc}")

# ----------------------- Chat with the press release -----------------------
if st.session_state["press_release"]:
    st.subheader("Chat with the Press Release")
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            st.markdown(f"**Assistant:** {msg['content']}")
        elif msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")

    user_msg = st.text_input("Ask a question", key="chat_input")
    if st.button("Send", key="send_button"):
        if not client:
            st.error("OpenAI API key is missing. Please set it in Streamlit secrets or as an environment variable named OPENAI_API_KEY.")
        elif user_msg:
            st.session_state["messages"].append({"role": "user", "content": user_msg})
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are discussing the following press release:\n{st.session_state['press_release']}"
                        }
                    ] + st.session_state["messages"],
                    temperature=0.7,
                )
                reply = response.choices[0].message.content.strip()
                st.session_state["messages"].append({"role": "assistant", "content": reply})
                if hasattr(st, "rerun"):
                    st.rerun()
                elif hasattr(st, "experimental_rerun"):
                    st.experimental_rerun()
            except Exception as exc:
                logger.exception("Error during chat: %s", exc)
                st.error(f"An error occurred: {exc}")

