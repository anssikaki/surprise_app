import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from openai import OpenAI
import yfinance as yf
import random

# --- Configuration ---
TICKERS = ["UPM.HE", "STERV.HE", "VAPO.HE"]  # Add your key forestry tickers here
NEWS_QUERY = "forest industry OR forestry OR timber OR UPM"

# Initialize clients
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Page config
st.set_page_config(page_title="Forest Industry Pulse", layout="wide")
st.title("🌲 Forest Industry Pulse")

# Sidebar controls
st.sidebar.header("Settings")
news_source = st.sidebar.selectbox("News Source", ["Google News", "Bing News"])
num_headlines = st.sidebar.slider("Number of Headlines", min_value=5, max_value=20, value=10)
refresh = st.sidebar.button("Refresh Data")

if refresh:
    st.experimental_rerun()

# --- Real-time Stock Tracker ---
st.header("📈 Real-time Stock Prices")
stock_data = []
for ticker in TICKERS:
    try:
        hist = yf.Ticker(ticker).history(period="1d", interval="5m")
        latest_price = hist["Close"].iloc[-1]
        stock_data.append({"Ticker": ticker, "Price (EUR)": latest_price})
    except Exception:
        stock_data.append({"Ticker": ticker, "Price (EUR)": "N/A"})

stock_df = pd.DataFrame(stock_data).set_index("Ticker")
col1, col2 = st.columns([1, 2])
with col1:
    st.dataframe(stock_df, height=200)
with col2:
    example = TICKERS[0]
    df_plot = yf.Ticker(example).history(period="1d", interval="15m")["Close"].reset_index()
    fig = px.line(df_plot, x="Datetime", y="Close", title=f"Intraday Price: {example}")
    st.plotly_chart(fig, use_container_width=True)

# --- News Headlines ---
st.header("📰 Recent News Headlines")
# Fetch articles
if news_source == "Google News":
    url = (
        f"https://newsapi.org/v2/everything?q={NEWS_QUERY}"
        f"&apiKey={st.secrets['news']['google_api_key']}"
        f"&pageSize={num_headlines}&sortBy=publishedAt"
    )
    res = requests.get(url).json()
    articles = res.get("articles", [])
else:
    url = (
        f"https://api.bing.microsoft.com/v7.0/news/search?q={NEWS_QUERY}&count={num_headlines}"
    )
    headers = {"Ocp-Apim-Subscription-Key": st.secrets['news']['bing_api_key']}
    res = requests.get(url, headers=headers).json()
    articles = res.get("value", [])

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
        f"""**{idx}. [{title}]({link})**  
_Source: {src} | Published: {time}_"""
    )

# --- AI Insights ---
st.header("🤖 AI Summaries & Sentiment Analysis")
for art in articles:
    title = art.get("title", "No title")
    link = art.get("url", "#")
    with st.expander(title):
        prompt = (
            f"You are a financial analyst.\n"
            f"Article title: {title}\n"
            f"Provide:\n"
            f"1. A concise summary (2-3 sentences).\n"
            f"2. Sentiment (Positive, Neutral, Negative) based on the title.\n"
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
