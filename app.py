import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# アプリのタイトル
st.title("株価チャート表示アプリ")

# ユーザーからティッカーシンボルを入力
ticker = st.text_input("株式のティッカーシンボルを入力してください (例: AAPL, TSLA, 9984.T)", "9432.T")

# 株価データの取得
try:
	stock_data = yf.Ticker(ticker)
	df = stock_data.history(period="1mo")  # 過去1ヶ月分のデータ
	if df.empty:
		st.error("データが見つかりません。正しいティッカーシンボルを入力してください。")
	else:
		# 短期移動平均線 (5日) と長期移動平均線 (10日) の計算
		df['5日移動平均'] = df['Close'].rolling(window=5).