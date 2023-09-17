import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import zeta_valley as zv
import numpy as np
import yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
import random
TIPS_BEFORE_BUYING = [
    "Always do your own research and due diligence before buying a stock.",
    "Diversify your portfolio to spread risk.",
    "Invest in companies you understand and believe in for the long term.",
    "Avoid making decisions based solely on price movements or market speculation.",
    "Monitor your investments regularly and stay updated with market news.",
    "Consider the company's fundamentals, such as earnings, valuation, and growth potential.",
    "Always be cautious of stocks with extremely high valuations or rapid price increases.",
    "Set a budget and avoid investing money you can't afford to lose.",
    "Consider setting stop-loss orders to limit potential losses.",
    "Stay patient and avoid emotional decision-making."
]
random.shuffle(TIPS_BEFORE_BUYING)
selected_tips = TIPS_BEFORE_BUYING[:3] 
# Load environment variables
load_dotenv()

# Retrieve API keys from .env file
alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')

# Streamlit app
st.title('Stocklit Dashboard')

# Sidebar inputs
ticker = st.sidebar.text_input('Ticker', value='TSLA')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Download stock data
data = yf.download(ticker, start=start_date, end=end_date).reset_index()
fig = px.line(data, x='Date', y='Adj Close', title=ticker)
fig = px.line(data, x=data.index.name, y='Adj Close', title=ticker)
fig.update_traces(line=dict(color='red'))
st.plotly_chart(fig)

# Tabs
pricing_data, fundamental_data, news, stock_comparison, tips_tab = st.tabs(
    ["Pricing Data", "Fundamental Data", "Trending News", "Stock Comparison", "Tips"]
)
with tips_tab:
    st.write("Consider the following tips before investing in stocks:")
    for tip in selected_tips:
        st.write(f"- {tip}")
# Pricing Data tab
with pricing_data:
    st.header('Price Movements')
    data2 = data.copy()
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['% Change'].mean() * 252 * 100
    st.write('Annual Return is ', annual_return, '%')
    stdev = np.std(data2['% Change']) * np.sqrt(252)
    st.write('Standard Deviation is ', stdev * 100, '%')
    st.write('Risk Adj. Return is', annual_return / (stdev * 100))

# Fundamental Data tab
with fundamental_data:
    #fd = FundamentalData(key=alpha_vantage_key, output_format='pandas')
    st.subheader('Balance Sheet')
    balance_sheet = zv.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = zv.get_income_statement_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = zv.get_cash_flow_annual(ticker)[0]  # Corrected the typo here
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)

# Top 10 News tab
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i + 1}')
        st.write(df_news['published'].iloc[i])
        st.write(df_news['title'].iloc[i])
        st.write(df_news['summary'].iloc[i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment: {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment: {news_sentiment}')

# Stock Comparison tab
with stock_comparison:
    st.header("Stock Comparison")
    selected_tickers = st.multiselect(
        'Select stocks for comparison',
        ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'GOOGL'],
        default=['TSLA', 'AAPL']
    )

    comparison_data = {}
    for t in selected_tickers:
        comparison_data[t] = yf.download(t, start=start_date, end=end_date)

    comparison_fig = px.line(title='Stock Comparison')
    for t, d in comparison_data.items():
        comparison_fig.add_scatter(x=d.index, y=d['Adj Close'], name=t)
    st.plotly_chart(comparison_fig)

    comparison_metrics = {}
    for t, d in comparison_data.items():
        daily_return = d['Adj Close'] / d['Adj Close'].shift(1) - 1
        annual_return = daily_return.mean() * 252
        stdev = np.std(daily_return) * np.sqrt(252)
        comparison_metrics[t] = {
            'Annual Return': annual_return,
            'Standard Deviation': stdev,
            'Risk Adj. Return': annual_return / stdev
        }

    comparison_df = pd.DataFrame(comparison_metrics).T
    st.table(comparison_df)
