import os
import logging
import streamlit as st
from openai import OpenAI

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

st.set_page_config(page_title="Press Release from the Future")
st.title("Press Release from the Future")

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
            st.subheader("Generated Press Release")
            st.write(press_release)
        except Exception as exc:
            logger.exception("Error while generating press release: %s", exc)
            st.error(f"An error occurred: {exc}")

