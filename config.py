import os
from dotenv import load_dotenv
import pyupbit
load_dotenv()

# 업비트 API 키
UPBIT_ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
UPBIT_SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

upbit = pyupbit.Upbit(UPBIT_ACCESS_KEY,UPBIT_SECRET_KEY)

# 매매 설정
MIN_ORDER_KRW = 5000        # 최소 거래 금액
RSI_THRESHOLD = 30          # RSI 기준값
STOP_LOSS = 0.95            # 손절 비율
TAKE_PROFIT = 1.10          # 익절 비율
INTERVAL_SECONDS = 1       # 반복 주기 (초)
