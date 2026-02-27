import csv
from batch_backtest import backtest_with_ai
import pyupbit

def run_batch_backtest(save_csv=True, top_n=3):
    tickers = pyupbit.get_tickers(fiat="KRW")
    results = []

    for ticker in tickers:
        if ticker == "KRW-BTC":
            continue

        # print(f">> 백테스트 중: {ticker}")
        result = backtest_with_ai(ticker)
        if result:
            results.append(result)

    # 수익률 기준 정렬
    results.sort(key=lambda x: x["profit"], reverse=True)

    # CSV 저장
    if save_csv:
        with open("backtest_results.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ticker", "trades", "profit"])
            writer.writeheader()
            writer.writerows(results)
        print("\n✅ 결과를 'backtest_results.csv'에 저장 완료")

    # 결과 출력
    print("\n=== 백테스트 결과 요약 ===")
    for r in results[:top_n]:
        print(f"{r['ticker']} | 거래: {r['trades']}회 | 수익률: {r['profit']}%")

    # 상위 N종목만 리턴
    top_tickers = [r["ticker"] for r in results[:top_n]]
    return top_tickers

if __name__ == "__main__":
    run_batch_backtest()
