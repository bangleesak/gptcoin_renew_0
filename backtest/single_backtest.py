import pyupbit
from ai import ai_decision

def single_backtest(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=200)
    balance = 1000000  # 시작 자금
    holding = 0
    buy_price = 0

    for i in range(20, len(df)):
        partial_df = df.iloc[:i+1]
        decision = ai_decision(partial_df, ticker)
        close_price = df.iloc[i]["close"]

        if decision["decision"] == "buy" and balance > 0:
            holding = balance / close_price
            buy_price = close_price
            balance = 0
        elif decision["decision"] == "sell" and holding > 0:
            balance = holding * close_price
            holding = 0

    final_value = balance + holding * df.iloc[-1]["close"]
    profit = (final_value - 1000000) / 1000000 * 100
    return {"ticker": ticker, "profit": profit}
