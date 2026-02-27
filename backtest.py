import pyupbit
from trading import *

def simple_backtest(ticker, interval="minute10", count=200, rsi_threshold=30):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    df["rsi"] = calculate_rsi(df)
    
    buy_price = 0
    profit = 0
    trade_count = 0

    for i in range(1, len(df)):
        rsi = df["rsi"].iloc[i]
        close = df["close"].iloc[i]

        # 매수 조건
        if buy_price == 0 and rsi < rsi_threshold:
            buy_price = close
            print(f"[BUY] {df.index[i]} - Price: {buy_price:.0f}")

        # 매도 조건 (3% 이상 익절 또는 -1% 손절)
        elif buy_price > 0:
            change = (close - buy_price) / buy_price * 100

            if change >= 3 or change <= -1:
                profit += change
                trade_count += 1
                print(f"[SELL] {df.index[i]} - Price: {close:.0f}, Return: {change:.2f}%")
                buy_price = 0

    print(f"\n총 거래 횟수: {trade_count}회")
    print(f"누적 수익률: {profit:.2f}%")
