import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title('Stock Dashboard')

# Setting default value to TSLA (Tesla)
ticker = st.sidebar.text_input('Ticker', value='TSLA')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start=start_date, end=end_date)
fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news, openai1 = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News", "OpenAI ChatGPT"])

with pricing_data:
    st.header('Price Movements')
    data2 = data
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace = True)
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100
    st.write('Annual Return is ', annual_return, '%')
    stdev = np.std(data2['% Change']) * np.sqrt(252)
    st.write('Standard Deviation is ', stdev*100, '%')
    st.write('Risk Adj. Return is', annual_return/(stdev*100))

from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    key = 'FD19ATE7G5C0SFC5'
    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement = fd.get_balance_sheet_annual(ticker)[0]
    is1 = income_statement.T[2:]
    is1.columns = list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow = fd.get_cash_flow_annual(ticker)[0]
    cf = cash_flow.T[2:]
    cf.columns = list(cash_flow.T.iloc[0])
    st.write(cf)
from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'].iloc[i])
        st.write(df_news['title'].iloc[i])
        st.write(df_news['summary'].iloc[i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

from pyChatGPT import ChatGPT
session_token = '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'
api2 = ChatGPT(session_token)
buy = api2.send_message(f'3 Reasons to buy {ticker} stock')
sell = api2.send_message(f'3 Reasons to sell {ticker} stock')
swot = api2.send_message(f'SWOT analysis of {ticker} stock')

with openai1:
    buy_reason, sell_reason, swot_analysis = st.tabs(['3 Reasons to buy', '3 Reasons to sell', 'SWOT analysis'])
    
    with buy_reason:
        st.subheader(f'3 reasons on why to BUY {ticker} Stock')
        st.write(buy['message'])
    with sell_reason:
        st.subheader(f'3 reasons on why to SELL {ticker} Stock')
        st.write(sell['message'])
    with swot_analysis:
        st.subheader(f'SWOT Analysis of {ticker} Stock')
        st.write(swot['message'])