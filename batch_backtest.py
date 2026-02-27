# 여러 종목 일괄 백테스트 루틴 예시

import pyupbit
from ai import ai_decision
from indicators import calculate_rsi

def backtest_with_ai(ticker, interval="minute10", count=300, verbose=False):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    if df is None or len(df) < 20:
        return None

    df["rsi"] = calculate_rsi(df)

    buy_price = 0
    total_profit = 0
    trade_count = 0

    for i in range(20, len(df)):
        sliced_df = df.iloc[:i+1]
        close = df["close"].iloc[i]
        decision = ai_decision(sliced_df, ticker)

        if decision["decision"] == "buy" and buy_price == 0:
            buy_price = close
            if verbose:
                print(f"[{ticker}] BUY at {close:.0f}")

        elif decision["decision"] == "sell" and buy_price > 0:
            change = (close - buy_price) / buy_price * 100
            total_profit += change
            trade_count += 1
            if verbose:
                print(f"[{ticker}] SELL at {close:.0f}, Return: {change:.2f}%")
            buy_price = 0

    return {
        "ticker": ticker,
        "trades": trade_count,
        "profit": round(total_profit, 2)
    }
