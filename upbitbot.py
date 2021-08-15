import pandas as pd
import numpy as np
import pyupbit
import time
import datetime

def load_upbit(name):
    if name == 'aws':
        access = "IYTto6mPJyFfB5TKvx6alYyrz5dJIWlx6BKm01xC" # Access key
        secret = "UHY6PxATONnXGnOLtGH3MHWs1JxNGdMsiWwLUg26" # Secret Key
        upbit = pyupbit.Upbit(access, secret) # key loading aws
    elif name == 'home':
        access = 'hy4DIPski3O70M0GcpZuAy1CZ2ZIdBciWCGcTYC1'
        secret = 'I2MGAWP4az34GdWjnA9FLUIr2F3S39HgTJapNXfk'
        upbit = pyupbit.Upbit(access,secret) # key loading home
    else:
        pass
    return upbit

# 업비트 로그인
upbit = load_upbit('aws')
upbit

# 변동성 돌파 전략 - 목표가 조회
def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    k = 1 - abs(df.iloc[0]['open'] - df.iloc[0]['close']) / (df.iloc[0]['high'] - df.iloc[0]['low'])
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    print('목표가:',target_price)
    return target_price

# 시작 시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute1', count=1)
    start_time = df.index[0]
    return start_time

# 20일 이동 평균선 조회
def ma20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='day',count=20)
    ma20 = df['close'].rolling(window=20, min_periods=1).mean().iloc[-1]
    print(ma20)
    return ma20

def ma5(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='day',count=20)
    ma5 = df['close'].rolling(window=5, min_periods=1).mean().iloc[-1]
    print(ma5)
    return ma5

def rsi(ohlc: pd.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0
    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD
    return pd.Series(100 - (100/(1 + RS)), name = "RSI")

# 잔고 조회
def get_balance(ticker):
    balances = upbit.get_balances()
    for bal in balances:
        if bal['currency'] == ticker:
            if bal['balance'] is not None:
                return float(bal['balance'])
            else:
                return 0

# 현재가 조회
def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers = ticker)[0]['orderbook_units'][0]['ask_price']   

# 자동매매 시작
while True:
    data = rsi(ticker='KRW-BTC', interval='minute5')
    now_rsi = rsi(data,14).iloc[-1]
    try:
        now = datetime.datetime.now()
        start_time = get_start_time('KRW-BTC')
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price('KRW-BTC')
            ma20 = ma20('KRW-BTC')
            current_price = get_current_price('KRW-BTC')
            if target_price < current_price and ma20 < current_price and now_rsi <= 28:
                krw = get_balance('KRW')
                if krw > 5000:
                    upbit.buy_market_order('KRW-BTC',krw*0.9995)

        else:
            btc = get_balance('BTC')
            if btc > 0.00009 and now_rsi >= 70:
                upbit.sell_market_order('KRW-BTC',btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
