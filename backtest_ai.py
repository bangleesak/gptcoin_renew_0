# import pyupbit
# from ai import ai_decision
from indicators import *  # RSI 계산 함수 필요

# # def backtest_with_ai(ticker, interval="minute10", count=300):
# #     df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
# #     if df is None or len(df) < 20:
# #         print("데이터 부족")
# #         return None  # 데이터가 부족하면 None 반환

# #     # RSI 계산
# #     df["rsi"] = calculate_rsi(df)
# #     if df["rsi"].isnull().sum() > 0:
# #         print("RSI 계산 오류: 일부 데이터가 결측값입니다.")
# #         return None  # RSI 계산이 제대로 되지 않으면 None 반환

# #     buy_price = 0
# #     total_profit = 0
# #     trade_count = 0

# #     for i in range(20, len(df)):
# #         sliced_df = df.iloc[:i+1]  # 현재 시점까지 슬라이싱
# #         close = df["close"].iloc[i]
# #         decision = ai_decision(sliced_df, ticker)

# #         # 매매 결정을 로그로 확인
# #         print(f"[{df.index[i]}] 결정: {decision['decision']}")

# #         if decision["decision"] == "buy" and buy_price == 0:
# #             buy_price = close
# #             print(f"[BUY] {df.index[i]} - {close:.0f}원")

# #         elif decision["decision"] == "sell" and buy_price > 0:
# #             change = (close - buy_price) / buy_price * 100
# #             total_profit += change
# #             trade_count += 1
# #             print(f"[SELL] {df.index[i]} - {close:.0f}원, 수익률: {change:.2f}%")
# #             buy_price = 0

# #     # 최종 출력
# #     if trade_count > 0:
# #         print(f"\n총 거래: {trade_count}회")
# #         print(f"누적 수익률: {total_profit:.2f}%")
# #     else:
# #         print("\n거래가 없었습니다. 수익률 계산 불가.")

# #     return total_profit

# def backtest_with_ai(ticker, interval="minute10", count=300):
#     df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)

#     buy_price = None
#     profit = 0
#     trades = 0

#     for i in range(30, len(df)):  # 충분한 과거 데이터 확보 후
#         sub_df = df.iloc[i-30:i]  # 최근 30개 캔들로 판단
#         decision = ai_decision(sub_df)

#         if decision['decision'] == 'buy' and buy_price is None:
#             buy_price = df.iloc[i]["close"]
#         elif decision['decision'] == 'sell' and buy_price is not None:
#             sell_price = df.iloc[i]["close"]
#             profit += (sell_price - buy_price) / buy_price
#             trades += 1
#             buy_price = None

#     return profit, trade_count  # 예: (5.4, 12)


# backtest_ai.py 또는 backtest/single_backtest.py 등

from ai import *
from trading import simulate_trade  # 시뮬레이션용 함수라고 가정
import pyupbit

# def backtest_with_ai(ticker, interval="minute10", count=300):
#     df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
#     if df is None or len(df) < 30:
#         return None

#     position = None
#     buy_price = 0
#     profit = 0.0
#     trade_count = 0

#     for i in range(20, len(df)):
#         sub_df = df.iloc[:i+1]
#         decision = ai_decision(sub_df, ticker)  # 여기서 ticker 빠뜨리면 오류 발생

#         price = sub_df['close'].iloc[-1]

#         if decision["decision"] == "buy" and position is None:
#             buy_price = price
#             position = "long"

#         elif decision["decision"] == "sell" and position == "long":
#             change = (price - buy_price) / buy_price * 100
#             profit += change
#             trade_count += 1
#             position = None

#     # ✅ 수익률과 거래 횟수 반환
#     return profit, trade_count

def backtest_with_ai(ticker, interval="minute10", count=300):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
    if df is None or len(df) < 30:
        return None

    df = enrich_with_indicators(df)  # RSI/MA 포함

    position = None
    buy_price = 0
    profit = 0.0
    trade_count = 0

    for i in range(30, len(df)):
        sub_df = df.iloc[:i+1]
        decision = ai_decision(sub_df, ticker)
        price = sub_df['close'].iloc[-1]

        if decision["decision"] == "buy" and position is None:
            buy_price = price
            position = "long"

        elif decision["decision"] == "sell" and position == "long":
            change = (price - buy_price) / buy_price * 100
            profit += change
            trade_count += 1
            position = None

    return profit, trade_count
