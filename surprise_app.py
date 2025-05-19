import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from openai import OpenAI
import yfinance as yf

# --- Configuration ---
TICKERS = ["UPM.HE", "STERV.HE", "METSB.HE"]  # Key forestry tickers: UPM, Stora Enso, Metsä Board
NEWS_QUERY = "forest industry OR forestry OR timber OR UPM"

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets.get("openai", {}).get("api_key", ""))

# Page config (centered layout for mobile)
st.set_page_config(page_title="Forest Industry Pulse", layout="centered")

# Responsive CSS for mobile
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
num_headlines = st.sidebar.slider("Number of Headlines", min_value=1, max_value=20, value=5)
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
        stock_data.append({"Ticker": ticker, "Latest Price (EUR)": hist["Price"].iloc[-1]})
        price_dfs.append(hist)
    except Exception:
        stock_data.append({"Ticker": ticker, "Latest Price (EUR)": "N/A"})

price_df = pd.DataFrame(stock_data).set_index("Ticker")
st.dataframe(price_df)

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
        st.error("Google News API key missing. Add under [news] in Streamlit secrets.")
    else:
        # Use 'everything' with qInTitle to filter forest-specific headlines
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={requests.utils.quote(NEWS_QUERY)}&qInTitle=forest&"
            f"sortBy=publishedAt&pageSize={num_headlines}&apiKey={google_key}"
        )
        
        NEWS_QUERY = "forest industry Finland"
        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={requests.utils.quote(NEWS_QUERY)}&"
            f"searchIn=title,description,content&"
            f"language=en&"
            f"sortBy=publishedAt&"
            f"pageSize={num_headlines}&"
            f"apiKey={google_key}"
        )
        
        res = requests.get(url)
        if res.ok:
            articles = [a for a in res.json().get("articles", []) if "forest" in a.get("title", "").lower()]
        else:
            st.error(f"Google News API error: {res.status_code}")
elif news_source == "Bing News":
    bing_key = st.secrets.get('news', {}).get('bing_api_key')
    if not bing_key:
        st.error("Bing News API key missing. Add under [news] in Streamlit secrets.")
    else:
        url = (
            f"https://api.bing.microsoft.com/v7.0/news/search?"
            f"q=forest%20industry&count={num_headlines}"
        )
        headers = {"Ocp-Apim-Subscription-Key": bing_key}
        res = requests.get(url, headers=headers)
        if res.ok:
            articles = res.json().get("value", [])
        else:
            st.error(f"Bing News API error: {res.status_code}")

if not articles:
    st.warning("No news articles found. Try a different news source or adjust the number of headlines.")

for idx, art in enumerate(articles, start=1):
    title = art.get("title", "No title")
    link = art.get("url", art.get("link", "#"))
    if news_source == "Google News":
        src = art.get("source", {}).get("name")
        time = art.get("publishedAt")
    else:
        src = art.get("provider", [{}])[0].get("name")
        time = art.get("datePublished")
    st.markdown(f"**{idx}. [{title}]({link})**  \n_Source: {src} | {time}_")

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
            st.write(response.choices[0].message.content.strip())
        except:
            st.error("Failed to fetch AI insight.")

# --- Chat Box ---
st.header("💬 Ask the Pulse")
user_question = st.text_input("Enter your question for the forest industry AI:")
if st.button("Ask"):
    if user_question.strip():
        with st.spinner("Thinking..."):
            chat_resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert on the forest industry with access to real-time data."},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7,
                max_tokens=200
            )
            st.write(chat_resp.choices[0].message.content.strip())
    else:
        st.error("Please enter a question.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ by [Your Name]")
