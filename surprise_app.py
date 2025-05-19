import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from openai import OpenAI
import yfinance as yf

# --- Configuration ---
TICKERS = ["UPM.HE", "STERV.HE", "METSB.HE"]  # Key forestry tickers: UPM, Stora Enso, Metsä Board

# Initialize clients
client = OpenAI(api_key=st.secrets.get("openai", {}).get("api_key", ""))

# Page config (centered layout for mobile)
st.set_page_config(page_title="Forest Industry Pulse", layout="centered")

# Custom CSS for responsive fonts and tables
st.markdown(
    """
    <style>
    @media (max-width: 600px) {
        h1 { font-size: 1.6rem !important; }
        .stDataFrame table td, .stDataFrame table th { font-size: 0.8rem !important; }
        .stMarkdown p, .stMarkdown h2 { font-size: 0.9rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🌲 Forest Industry Pulse")

# Sidebar controls
st.sidebar.header("Settings")
news_source = st.sidebar.selectbox("News Source", ["Google News", "Bing News"])
num_headlines = st.sidebar.slider("Number of Headlines", min_value=5, max_value=20, value=10)
if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

# --- Real-time Stock Tracker ---
st.header("📈 Intraday Stock Prices")
stock_data = []
price_dfs = []
for ticker in TICKERS:
    try:
        hist = yf.Ticker(ticker).history(period="1d", interval="5m")[["Close"]].reset_index()
        hist.rename(columns={"Close": "Price"}, inplace=True)
        hist["Ticker"] = ticker
        latest_price = hist["Price"].iloc[-1]
        stock_data.append({"Ticker": ticker, "Latest Price (EUR)": latest_price})
        price_dfs.append(hist)
    except Exception:
        stock_data.append({"Ticker": ticker, "Latest Price (EUR)": "N/A"})

# Display latest prices as full-width table
price_df = pd.DataFrame(stock_data).set_index("Ticker")
st.dataframe(price_df)

# Plot intraday for all tickers full-width
if price_dfs:
    all_prices = pd.concat(price_dfs)
    fig = px.line(all_prices, x="Datetime", y="Price", color="Ticker", title="Intraday Prices for All Companies")
    st.plotly_chart(fig, use_container_width=True)

# --- News Headlines ---
st.header("📰 Recent News Headlines")
articles = []

if news_source == "Google News":
    google_key = st.secrets.get('news', {}).get('google_api_key')
    if not google_key:
        st.error("Google News API key missing. Please add it to Streamlit secrets under [news].")
    else:
        url = (
            f"https://newsapi.org/v2/top-headlines?country=fi"
            f"&category=business&pageSize={num_headlines}&apiKey={google_key}"
        )
        res = requests.get(url)
        if res.ok:
            articles = res.json().get("articles", [])
        else:
            st.error(f"Google News API error: {res.status_code}")
elif news_source == "Bing News":
    bing_key = st.secrets.get('news', {}).get('bing_api_key')
    if not bing_key:
        st.error("Bing News API key missing. Please add it to Streamlit secrets under [news].")
    else:
        url = f"https://api.bing.microsoft.com/v7.0/news/search?q=forest%20industry&count={num_headlines}"
        headers = {"Ocp-Apim-Subscription-Key": bing_key}
        res = requests.get(url, headers=headers)
        if res.ok:
            articles = res.json().get("value", [])
        else:
            st.error(f"Bing News API error: {res.status_code}")

# Display headlines stacked vertically for mobile
for idx, art in enumerate(articles, start=1):
    title = art.get("title", "No title")
    link = art.get("url", art.get("link", "#"))
    if news_source == "Google News":
        src = art.get("source", {}).get("name")
        time = art.get("publishedAt")
    else:
        src = art.get("provider", [{}])[0].get("name")
        time = art.get("datePublished")
    st.markdown(f"**{idx}. [{title}]({link})**  
_Source: {src} | {time}_")

# --- AI Insights ---
st.header("🤖 AI Summaries & Sentiment Analysis")
for art in articles:
    title = art.get("title", "No title")
    with st.expander(title):
        prompt = (
            f"You are a financial analyst.\n"
            f"Article title: {title}\n"
            f"Provide:\n"
            f"1. A concise summary (2-3 sentences).\n"
            f"2. Sentiment (Positive, Neutral, Negative).\n"
            f"3. Key risk or trend highlight.\n"
        )
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful, concise AI financial assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            insight = response.choices[0].message.content.strip()
            st.write(insight)
        except Exception:
            st.error("Failed to fetch AI insight.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by [Your Name]")
