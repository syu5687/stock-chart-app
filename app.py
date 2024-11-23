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
        df['5日移動平均'] = df['Close'].rolling(window=5).mean()
        df['10日移動平均'] = df['Close'].rolling(window=10).mean()

        # チャート作成
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='ローソク足'
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['5日移動平均'],
            mode='lines',
            name='5日移動平均',
            line=dict(color='blue', width=1.5)
        ))
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['10日移動平均'],
            mode='lines',
            name='10日移動平均',
            line=dict(color='red', width=1.5)
        ))

        fig.update_layout(
            title=f"{ticker} 株価チャート",
            xaxis_title="日付",
            yaxis_title="価格 (JPY)",
            xaxis_rangeslider_visible=False
        )

        # チャートをアプリに表示
        st.plotly_chart(fig)
except Exception as e:
    st.error(f"エラーが発生しました: {e}")
