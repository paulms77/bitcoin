import pandas as pd
import numpy as np
import pyupbit
import time
import datetime

def load_upbit(name):
    if name == 'aws':
        access = "oWHsAxrj7wb7YawB78LQFsySKjhdCDd86Ami3dpO" # Access key
        secret = "Pzpr1nNE7XhfMYnfBmHkPndoCYy10H3ycFzjFMvW" # Secret Key
        upbit = pyupbit.Upbit(access, secret) # key loading aws
    else:
        pass
    return upbit

upbit = load_upbit('aws')
upbit

def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5")
    #k = 1 - abs(df.iloc[0]['open'] - df.iloc[0]['close']) / (df.iloc[0]['high'] - df.iloc[0]['low'])
    k = 0.5
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    print('목표가:',target_price)
    return target_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute1', count=1)
    start_time = df.index[0]
    return start_time

def ma20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute1')
    ma20 = df['close'].rolling(window=20, min_periods=1).mean()
    return ma20

def ma5(ticker):
    df = pyupbit.get_ohlcv(ticker, interval='minute1')
    ma5 = df['close'].rolling(window=5, min_periods=1).mean()
    return ma5

def macd1(ticker):
    data = pyupbit.get_ohlcv(ticker, interval='minute10')
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()
    test1=exp3[0]-macd[0]
    return test1

def macd2(ticker):
    data = pyupbit.get_ohlcv(ticker, interval='minute10')
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()
    test2=exp3[1]-macd[1]
    return test2

# RSI
def rsi(ticker, period: int = 14):
    data = pyupbit.get_ohlcv(ticker, interval='minute5') # 기본 5분봉 # 이클 -> 10분봉
    delta = data["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0
    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD
    return pd.Series(100 - (100/(1 + RS)), name = "RSI")
    
def get_balance(ticker):
    balances = upbit.get_balances()
    for bal in balances:
        if bal['currency'] == ticker:
            if bal['balance'] is not None:
                return float(bal['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(tickers = ticker)[0]['orderbook_units'][0]['ask_price']   

print('upbitbot start')

# Start
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time('KRW-ETC')
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            print('='*10 +'[PAUL_v1(notice)]'+ '='*10)
            print('시작시간',start_time,'현재시간',now,'종료시간',end_time)
            target_price = get_target_price('KRW-ETC')
            current_price = get_current_price('KRW-ETC')
            print('현재가:',current_price)
            now_rsi = rsi('KRW-ETC',14).iloc[-1]
            print('rsi:',now_rsi)
            if (target_price < current_price) & (now_rsi < 28):
                krw = get_balance('KRW')
                if krw > 5000:
                    upbit.buy_market_order('KRW-ETC',krw)
        else:
            etc = get_balance('ETC')
            if (etc > 0.00008) & (now_rsi > 60):
                upbit.sell_market_order('KRW-ETC',etc)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

#test1 = macd1('KRW-ETC')
#print('macd1',test1)
#test2 = macd2('KRW-ETC')
#print('macd2',test2)
#ma5 = ma5('KRW-ETC').iloc[-1]
#print('ma5:',ma5)
#ma20 = ma20('KRW-ETC').iloc[-1]
#print('ma20:',ma20)