import streamlit as st
from openai import OpenAI, OpenAIError

# Initialize OpenAI client with API key stored in Streamlit secrets
try:
    api_key = st.secrets.get("openai", {}).get("api_key", "")
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("OpenAI API key not found in Streamlit secrets.")
    st.stop()

# Page configuration
st.set_page_config(page_title="Press Release from the Future", layout="centered")

# App title and description
st.title("Press Release from the Future")
st.markdown(
    ""
    "Enter your company name, product or idea, and a future year to generate a visionary corporate press release."
    ""
)

# Inputs
company = st.text_input("Company Name")
product = st.text_input("Product / Idea")
year = st.number_input(
    "Future Year", min_value=2025, max_value=2100, step=1, value=2030
)

# Generate button
if st.button("Generate Press Release"):
    # Validate inputs
    if not company.strip() or not product.strip():
        st.error("Please enter both a company name and a product/idea.")
    else:
        # Construct prompt for ChatGPT
        prompt = (
            f"Write a detailed corporate press release as if published in the year {year} "
            f"by {company}, announcing their new {product}. "
            "Include an engaging headline, quotes from executives, key technical specifications, "
            "market outlook, and potential future impact of the product."
        )

        # Generate and display response
        with st.spinner("Generating press release..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful and creative assistant specialized in crafting corporate press releases."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=500,
                )
                # Extract and display the press release text
                press_release = response.choices[0].message.content.strip()
                st.subheader("Generated Press Release")
                st.write(press_release)

            except OpenAIError as e:
                st.error(f"Failed to generate press release: {e}")
