import pyupbit
from utils import get_balance_safe, get_current_price_safe
from indicators import calculate_rsi
from config import *

# last_buy_price = None

# def execute_trade(upbit, decision, df):
#     global last_buy_price
#     current_price = get_current_price_safe("KRW-BTC")

#     if decision["decision"] == "buy":
#         rsi = calculate_rsi(df)
#         if rsi > RSI_THRESHOLD:
#             print(f"### RSI {rsi:.2f} > {RSI_THRESHOLD}: Buy blocked ###")
#             return

#         my_krw = get_balance_safe(upbit, "KRW")
#         if my_krw * 0.9995 > MIN_ORDER_KRW:
#             print("### Buy Executed ###")
#             upbit.buy_market_order("KRW-BTC", my_krw * 0.9995)
#             last_buy_price = current_price
#         else:
#             print("### Not enough KRW to Buy ###")

#     elif decision["decision"] == "sell":
#         my_btc = get_balance_safe(upbit, "BTC")
#         if my_btc * current_price > MIN_ORDER_KRW:
#             print("### Sell Executed ###")
#             upbit.sell_market_order("KRW-BTC", my_btc)
#             last_buy_price = None
#         else:
#             print("### Not enough BTC to Sell ###")

#     elif decision["decision"] == "hold":
#         print("### Hold ###")
# def execute_trade(upbit, decision, df, ticker):
#     current_price = pyupbit.get_current_price(ticker)
#     coin = ticker.split("-")[1]

#     # 마지막 매입 가격
#     global last_buy_price

#     if decision["decision"] == "buy":
#         krw = upbit.get_balance("KRW")
#         if krw > 5500:  # 최소 주문 금액이 5000원 이상이어야 함
#             upbit.buy_market_order(ticker, krw * 0.9995)
#             last_buy_price = current_price  # 매수 시점의 가격 저장
#             print(f"{ticker}: 매수 실행됨")
#         else:
#             print(f"{ticker}: 매수 불가 (잔고 부족)")

#     elif decision["decision"] == "sell":
#         coin_balance = upbit.get_balance(coin)
#         if coin_balance * current_price > 5500:  # 최소 매도 금액
#             # 수익률 계산
#             if last_buy_price is not None:
#                 profit_percentage = (current_price - last_buy_price) / last_buy_price * 100
#                 print(f"{ticker}: 수익률 = {profit_percentage:.2f}%")

#                 if profit_percentage <= -1:  # 수익률이 -1% 이하일 경우 매도
#                     upbit.sell_market_order(ticker, coin_balance)
#                     print(f"{ticker}: 매도 실행됨 (수익률 {profit_percentage:.2f}%)")
#                 else:
#                     print(f"{ticker}: 수익률이 -1% 이상으로 매도되지 않음")
#             else:
#                 print(f"{ticker}: 마지막 매입 가격이 없음")
#         else:
#             print(f"{ticker}: 매도 불가 (잔고 부족)")

#     elif decision["decision"] == "hold":
#         print(f"{ticker}: 보유 유지")


last_buy_prices = {}
def execute_trade(upbit, decision, df, ticker):
    current_price = get_current_price_safe(ticker)

    if decision["decision"] == "buy":
        if ticker not in last_buy_prices:
            krw = get_balance_safe(upbit, "KRW")
            if krw * 0.9995 > MIN_ORDER_KRW:
                upbit.buy_market_order(ticker, krw * 0.9995)
                last_buy_prices[ticker] = current_price
                print(f"### {ticker} 매수 ###")

    elif decision["decision"] == "sell":
        if ticker in last_buy_prices:
            coin_ticker = ticker.replace("KRW-", "")
            volume = get_balance_safe(upbit, coin_ticker)
            if volume * current_price > MIN_ORDER_KRW:
                upbit.sell_market_order(ticker, volume)
                print(f"### {ticker} 매도 ###")
                del last_buy_prices[ticker]

    elif decision["decision"] == "hold":
        print(f"### {ticker} 유지 ###")

def check_stop_conditions(upbit):
    global last_buy_price
    if last_buy_price is None:
        return False

    current_price = get_current_price_safe("KRW-BTC")
    if current_price <= last_buy_price * STOP_LOSS:
        print("### Stop-loss triggered ###")
        my_btc = get_balance_safe(upbit, "BTC")
        if my_btc > 0:
            upbit.sell_market_order("KRW-BTC", my_btc)
        last_buy_price = None
        return True

    if current_price >= last_buy_price * TAKE_PROFIT:
        print("### Take-profit triggered ###")
        my_btc = get_balance_safe(upbit, "BTC")
        if my_btc > 0:
            upbit.sell_market_order("KRW-BTC", my_btc)
        last_buy_price = None
        return True

    return False

# 수익률 계산 함수
def calculate_profit_percent(current_price, buy_price):
    return (current_price - buy_price) / buy_price * 100


# 익절 체크 (예: 수익률 3% 이상일 때 매도)
def check_take_profit(upbit, ticker, last_buy_price, threshold=3):
    current_price = pyupbit.get_current_price(ticker)
    coin = ticker.split("-")[1]
    coin_balance = upbit.get_balance(coin)

    if last_buy_price is None or coin_balance == 0:
        return False

    profit_percent = calculate_profit_percent(current_price, last_buy_price)

    if profit_percent >= threshold:
        upbit.sell_market_order(ticker, coin_balance)
        print(f"{ticker}: ### Take-profit triggered (수익률 {profit_percent:.2f}%) ###")
        return True

    return False


# 손절 체크 (수익률 0% 미만이면 매도)
def check_cut_loss(upbit, ticker, last_buy_price):
    current_price = pyupbit.get_current_price(ticker)
    coin = ticker.split("-")[1]
    coin_balance = upbit.get_balance(coin)

    if last_buy_price is None or coin_balance == 0:
        return False

    profit_percent = calculate_profit_percent(current_price, last_buy_price)

    if profit_percent < 0:
        upbit.sell_market_order(ticker, coin_balance)
        print(f"{ticker}: ### 손절 실행 (수익률 {profit_percent:.2f}%) ###")
        return True

    return False


# trading.py

def simulate_trade(position, current_price, buy_price):
    """
    간단한 매매 시뮬레이션 로직.
    position: 현재 포지션 ("long" 또는 None)
    current_price: 현재 가격
    buy_price: 매수 가격
    """
    if position == "long":
        profit = (current_price - buy_price) / buy_price * 100
        return profit
    return 0.0
