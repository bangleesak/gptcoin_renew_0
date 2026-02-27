import json
import os
import logging
from openai import OpenAI
from config import *
from indicators import *

# def ai_decision(df):
#     try:
#         client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a Bitcoin trading expert. "
#                         "Based on the 10-minute candlestick data, decide whether to 'buy', 'sell', or 'hold'. "
#                         "Respond only in JSON format like this: {\"decision\": \"buy\", \"reason\": \"...\"}"
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": json.dumps(df.to_dict(orient="records"))
#                 }
#             ]
#         )

#         result = response.choices[0].message.content
#         return json.loads(result)

#     except Exception as e:
#         print(f"AI decision error: {e}")
#         return {"decision": "hold", "reason": "AI error"}

# ai.py
def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

# def ai_decision(df, ticker):
#     rsi = calculate_rsi(df)
#     ma = df['close'].rolling(window=20).mean().iloc[-1]
#     price = df['close'].iloc[-1]

#     if price > ma and rsi < 5:
#         return {"decision": "buy"}
#     elif price < ma and  rsi > 95:
#         return {"decision": "sell"}
#     else:
#         return {"decision": "hold"}

# def ai_decision(df, ticker=None):
#     try:
#         # OpenAI 클라이언트 초기화
#         client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         # 최근 30개 캔들 데이터만 AI에게 전달
#         recent_data = df.tail(30).to_dict(orient="records")

#         # AI에게 판단 요청
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a crypto trading expert. "
#                         "Based on the candlestick data, return only JSON: "
#                         "{\"decision\": \"buy\"|\"sell\"|\"hold\", \"reason\": \"short explanation\"}."
#                         "Do not include explanations or extra words."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": json.dumps(recent_data)
#                 }
#             ]
#         )

#         result = response.choices[0].message.content
#         return json.loads(result)

#     except Exception as e:
#         print(f"AI decision error: {e}")
#         return {"decision": "hold", "reason": "AI error"}

# Setting up logging for better error tracking
# logging.basicConfig(level=logging.ERROR)

# def calculate_ma(df, period):
#     return df['close'].rolling(window=period).mean()

# def enrich_with_indicators(df):
#     df["rsi"] = calculate_rsi(df)
#     df["ma"] = calculate_ma(df, period=20)  # 20캔들 기준 MA
#     return df

# def ai_decision(df, ticker=None):
#     try:
#         # Check if API key exists
#         api_key = os.getenv("OPENAI_API_KEY")
#         if not api_key:
#             raise ValueError("OPENAI_API_KEY is not set")

#         # OpenAI 클라이언트 초기화
#         client = OpenAI(api_key=api_key)

#         # 최근 30개 캔들 데이터만 AI에게 전달
#         recent_data = df.tail(30).to_dict(orient="records")

#         # AI에게 판단 요청
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a crypto trading expert. "
#                         "Based on the candlestick data (including RSI, MA5, MA20), return only JSON: "
#                         "{\"decision\": \"buy\"|\"sell\"|\"hold\", \"reason\": \"short explanation\"}."
#                         # "If RSI < 10 and close > MA5 > MA20, return \"buy\". "
#                         # "If RSI > 90 and close < MA5 < MA20, return \"sell\". "
#                         "Use rules like: RSI < 10 → buy, RSI > 90 → sell. "
#                         "Also consider moving average: if price crosses above MA → buy, below → sell. "
#                         "Do not include explanations or extra words."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": json.dumps(recent_data)
#                 }
#             ]
#         )

#         # Get response and return parsed result
#         result = response.choices[0].message.content
#         return json.loads(result)

#     except Exception as e:
#         logging.error(f"AI decision error: {e}", exc_info=True)
#         return {"decision": "hold", "reason": "AI error"}

def ai_decision(df, ticker):                                # 수동처리리
    # rsi = calculate_rsi(df)
    # short_ma = df['close'].rolling(window=10).mean().iloc[-1]
    # mid_ma = df['close'].rolling(window=30).mean().iloc[-1]    
    # price = df['close'].iloc[-1]

    # if price > short_ma and rsi < 10:
    #     return {"decision": "buy"}
    # elif price < mid_ma and rsi > 90:
    #     return {"decision": "sell"}
    # else:
    #     return {"decision": "hold"}

    price = df['close'].iloc[-1]
    rsi = calculate_rsi(df)

    short_ma = df['close'].rolling(window=10).mean().iloc[-1]
    mid_ma = df['close'].rolling(window=30).mean().iloc[-1]
    long_ma = df['close'].rolling(window=60).mean().iloc[-1]

    prev_long_ma = df['close'].rolling(window=60).mean().iloc[-2]

    if rsi < 10 and price > short_ma and price < mid_ma:
        return {"decision": "buy", "reason": "과매도 + 단기MA 상회"}
    elif rsi > 90 and price < mid_ma and long_ma < prev_long_ma:
        return {"decision": "sell", "reason": "과매수 + 장기MA 하락"}
    else:
        return {"decision": "hold", "reason": "조건 불충족"}