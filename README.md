## Bitcoin automatic trading program

## Stretegy
- BTC의 경우 5분봉
- ETC의 경우 10분봉
  
10초마다 목표가 계산, 보조지표 RSI를 계산

BTC
- RSI < 29
  (매수 타이밍, 소량 매수)
- RSI > 62
  (매도 타이밍)

ETC
- RSI < 26
  (매수 타이밍, 소량 매수)
- RSI > 65
  (매도 타이밍)
 
## Environment
AWS-EC2, Linux
