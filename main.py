import time
import pyupbit
from datetime import datetime
from ai import ai_decision
from utils import check_manual_stop
from config import *
from trading import *
from backtest.single_backtest import *  # 백테스트 모듈 import
from backtest_ai import *
TARGET_TICKERS = ["KRW-PUNDIX"]  # ✅ 거래할 종목 지정

# def main_loop():
#     upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

#     while True:
#         # if check_manual_stop():
#         #     print("### Trading manually stopped by stop.txt ###")
#         #     break

#         for ticker in TARGET_TICKERS:
#             try:
#                 df = pyupbit.get_ohlcv(ticker, interval="minute10", count=100)
#                 if df is None or len(df) < 20:
#                     continue

#                 decision = ai_decision(df, ticker)
#                 execute_trade(upbit, decision, df, ticker)

#                 if check_stop_conditions(upbit):
#                     return  # 종료 조건 만족 시 루프 탈출

#                 time.sleep(0.3)

#             except Exception as e:
#                 print(f"{ticker} 오류 발생: {e}")

#         time.sleep(INTERVAL_SECONDS)

# def main_loop():
#     upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
#     tickers = ["KRW-PUNDIX"]  # 단타 대상 종목

#     while True:
#         if check_manual_stop():
#             print("### Trading manually stopped ###")
#             break

#         for ticker in tickers:
#             try:
#                 df = pyupbit.get_ohlcv(ticker, interval="minute10", count=100)
#                 if df is None or len(df) < 20:
#                     continue

#                 decision = ai_decision(df, ticker)
#                 execute_trade(upbit, decision, df, ticker)

#                 time.sleep(0.3)

#             except Exception as e:
#                 print(f"{ticker} 오류 발생: {e}")

#         time.sleep(INTERVAL_SECONDS)

def main_loop():
    upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)
    tickers = ["KRW-PUNDIX"]  # 단타 대상 종목
    total_consumed = 0  # 누적 소비 금액

    while True:  # 무한 루프를 추가하여 계속 실행되도록 함
        # 수동 매매 중단 조건을 체크하지 않음
        # if check_manual_stop():
        #     print("### Trading manually stopped ###")
        #     break

        for ticker in tickers:
            try:
                df = pyupbit.get_ohlcv(ticker, interval="minute10", count=100)
                if df is None or len(df) < 20:
                    continue

                decision = ai_decision(df, ticker)
                execute_trade(upbit, decision, df, ticker)

                #  # 현재 시간 기록
                # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # # 소비 금액 누적
                # total_consumed += 0.01

                # print(f"[{current_time}] {ticker} 거래 실행됨 - 누적 소비: ${total_consumed:.2f}")

                time.sleep(0.3)

            except Exception as e:
                print(f"{ticker} 오류 발생: {e}")

        time.sleep(INTERVAL_SECONDS)

# 

# if __name__ == "__main__":
#     while True:  # 무한 루프 추가
#         for ticker in TARGET_TICKERS:
#             print(f"\n📊 백테스트 시작: {ticker}")
#             profit = backtest_with_ai(ticker, interval="day", count=300)

#             # 수익률이 None이 아니면 계속 반복하도록 변경
#             if profit is not None:
#                 profit_display = profit if profit is not None else 0.0  # None일 경우 0.0으로 처리
#                 print(f"✅ 수익률 {profit_display:.2f}% → 실시간 매매 시작")
#                 main_loop()  # 수익률에 관계없이 매매 시작
#             else:
#                 print("❌ 수익률 정보가 없습니다.")
#                 # 이 부분에서 매매가 중단되지 않도록 할 수 있습니다. 예를 들어, 수익률 정보가 없으면 계속 진행.

#             time.sleep(5)  # 5초 대기 후 반복

# if __name__ == "__main__":
#     while True:  # 무한 루프
#         for ticker in TARGET_TICKERS:
#             print(f"\n📊 백테스트 시작: {ticker}")
#             result = backtest_with_ai(ticker, interval="day", count=300)

#             if result is not None:
#                 # 수익률과 거래 횟수 언팩
#                 profit_percent, trade_count = result if isinstance(result, tuple) else (result, 0)
#                 print(f"✅ 수익률 {profit_percent:.2f}% (거래 {trade_count}회) → 실시간 매매 시작")
#                 main_loop()  # 수익률에 관계없이 매매 시작
#             else:
#                 print("❌ 수익률 정보가 없습니다.")

#             time.sleep(5)

if __name__ == "__main__":
    while True:
        for ticker in TARGET_TICKERS:
            print(f"\n📊 백테스트 시작: {ticker}")
            result = backtest_with_ai(ticker, interval="day", count=300)

            if result is not None:
                profit_percent, trade_count = result
                print(f"✅ 수익률 {profit_percent:.2f}% (거래 {trade_count}회) → 실시간 매매 시작")
                main_loop()
            else:
                print("❌ 수익률 정보가 없습니다.")

            time.sleep(5)
