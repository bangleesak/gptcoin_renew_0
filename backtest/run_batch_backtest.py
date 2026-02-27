import csv
import pyupbit
from backtest.single_backtest import single_backtest

def run_batch_backtest():
    tickers = pyupbit.get_tickers(fiat="KRW")
    tickers = [t for t in tickers if t != "KRW-BTC"]
    results = []

    for ticker in tickers:
        try:
            result = single_backtest(ticker)
            results.append(result)
        except Exception as e:
            print(f"{ticker} 오류: {e}")

    results.sort(key=lambda x: x["profit"], reverse=True)

    with open("backtest_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["ticker", "profit"])
        writer.writeheader()
        writer.writerows(results)

    top_tickers = [r["ticker"] for r in results[:5]]
    return top_tickers
