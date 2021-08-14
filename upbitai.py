import pandas as pd
import numpy as np
import pyupbit

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
upbit = load_upbit('home')

# 암호화폐 리스트 확인
tickers = pyupbit.get_tickers()
krw_tickers = pyupbit.get_tickers(fiat='KRW')
#print(tickers[:5])
#print('총 암호화폐 개수:',len(tickers))
#print(krw_tickers[:5])
#print('KRW 암호화폐 개수:',len(krw_tickers))

# 암호화폐 현재가 얻기
print(pyupbit.get_current_price(krw_tickers))