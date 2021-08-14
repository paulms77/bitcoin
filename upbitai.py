import pandas as pd
import numpy as np
import pyupbit
import time
import datetime

# 실행 명령어
# python upbitai.py

# load upbit key
def load_upbit(name):
    if name == 'oocafe':
        access = "IYTto6mPJyFfB5TKvx6alYyrz5dJIWlx6BKm01xC" # Access key
        secret = "UHY6PxATONnXGnOLtGH3MHWs1JxNGdMsiWwLUg26" # Secret Key
        upbit = pyupbit.Upbit(access, secret) # key loading oocafe
    elif name == 'home':
        access = 'hy4DIPski3O70M0GcpZuAy1CZ2ZIdBciWCGcTYC1'
        secret = 'I2MGAWP4az34GdWjnA9FLUIr2F3S39HgTJapNXfk'
        upbit = pyupbit.Upbit(access,secret) # key loading home
    else:
        pass
    return upbit

# load ip account
upbit = load_upbit('oocafe')

# 변동성 돌파 전략으로 매수 목표가 조회
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=14) # 2주간 ohlcv 데이터 불러오기
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k # 목표가 지정
    return target_price

# 시작 시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# 5(단기매매전략) or 15일 이동 평균선 조회
def get_ma(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma = df['close'].rolling(5).mean().iloc[-1]
    return ma

#잔고 조회
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

#현재가 조회
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.32)
            ma15 = get_ma("KRW-BTC")
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = get_balance("BTC")
            if btc > 0.00009:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)