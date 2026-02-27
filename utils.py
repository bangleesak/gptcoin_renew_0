import pyupbit
import os

def get_balance_safe(upbit, ticker):
    try:
        balance = upbit.get_balance(ticker)  # 'BTC', 'KRW'와 같은 단일 자산명 사용
        return float(balance) if balance is not None else 0.0
    except:
        return 0.0

def get_current_price_safe(ticker):
    try:
        price = pyupbit.get_current_price(ticker)
        return float(price) if price is not None else 0.0
    except:
        return 0.0

def check_manual_stop():
    return os.path.exists("stop.txt")

def calculate_profit_rate(current_price, avg_buy_price):
    # """
    # 수익률 계산 함수 (% 단위)
    # :param current_price: 현재 가격
    # :param avg_buy_price: 평균 매수가
    # :return: 수익률 (예: 5.0 -> 5%)
    # """
    if avg_buy_price == 0 or avg_buy_price is None:
        return 0.0
    return ((current_price - avg_buy_price) / avg_buy_price) * 100
