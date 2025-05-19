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

# Page config
st.set_page_config(page_title="Forest Industry Pulse", layout="wide")
st.title("🌲 Forest Industry Pulse")

# Sidebar controls
st.sidebar.header("Settings")
news_source = st.sidebar.selectbox("News Source", ["Google News", "Bing News"])
num_headlines = st.sidebar.slider("Number of Headlines", min_value=5, max_value=20, value=10)
if st.sidebar.button("Refresh Data"):
    st.experimental_rerun()

# --- Real-time Stock Tracker ---
st.header("📈 Intraday Stock Prices")

# Fetch data for all tickers and show prices
stock_data = []
price_dfs = []
for ticker in TICKERS:
    try:
        hist = yf.Ticker(ticker).history(period="7d", interval="5m")[["Close"]].reset_index()
        hist.rename(columns={"Close": "Price"}, inplace=True)
        hist["Ticker"] = ticker
        latest_price = hist["Price"].iloc[-1]
        stock_data.append({"Ticker": ticker, "Latest Price (EUR)": latest_price})
        price_dfs.append(hist)
    except Exception:
        stock_data.append({"Ticker": ticker, "Latest Price (EUR)": "N/A"})

# Display latest prices
price_df = pd.DataFrame(stock_data).set_index("Ticker")
col1, col2 = st.columns([1, 2])
with col1:
    st.dataframe(price_df, height=200)

# Plot intraday for all tickers
if price_dfs:
    all_prices = pd.concat(price_dfs)
    fig = px.line(all_prices, x="Datetime", y="Price", color="Ticker", title="Intraday Prices for All Companies")
    with col2:
        st.plotly_chart(fig, use_container_width=True)

# --- News Headlines ---
st.header("📰 Recent News Headlines")
articles = []

if news_source == "Google News":
    # Fetch top headlines (general) for Finland to get random news
    google_key = st.secrets.get('news', {}).get('google_api_key')
    if not google_key:
        st.error("Google News API key missing. Please add it to Streamlit secrets under [news].")
    else:
        url = (
            f"https://newsapi.org/v2/top-headlines?country=fi"
            f"&apiKey={google_key}&pageSize={num_headlines}"
        )
        res = requests.get(url)
        if res.status_code == 200:
            articles = res.json().get("articles", [])
        else:
            st.error(f"News API error: {res.status_code}")

elif news_source == "Bing News":
    bing_key = st.secrets.get('news', {}).get('bing_api_key')
    if not bing_key:
        st.error("Bing News API key missing. Please add it to Streamlit secrets under [news].")
    else:
        url = f"https://api.bing.microsoft.com/v7.0/news/search?q=forest&pageSize={num_headlines}"
        headers = {"Ocp-Apim-Subscription-Key": bing_key}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            articles = res.json().get("value", [])
        else:
            st.error(f"Bing News API error: {res.status_code}")

# Display headlines
for idx, art in enumerate(articles, start=1):
    title = art.get("title", "No title")
    link = art.get("url", "#")
    if news_source == "Google News":
        src = art.get("source", {}).get("name")
        time = art.get("publishedAt")
    else:
        src = art.get("provider", [{}])[0].get("name")
        time = art.get("datePublished")
    st.markdown(
        f"**{idx}. [{title}]({link})**  \n_Source: {src} | Published: {time}_"
    )

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

# Footer
st.markdown("---")
st.caption("Built with ❤️ by [Your Name]")
