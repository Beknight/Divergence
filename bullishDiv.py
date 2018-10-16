import urllib.request 
import json
import numpy as np
import datetime as dt
import rsi as crypt
import collections
from collections import namedtuple

CandleAux = namedtuple("CandleAux", "rsi price time")
OPENTIME = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
RSIEP = 8
candleAuxList = []
valleyList = []

root_url = 'https://api.binance.com/api/v1/klines'
interval = '5m'
symbol = 'XRPUSDT'
url = root_url + '?symbol=' + symbol + '&interval=' + interval 
print(url)
resp = urllib.request.urlopen(url).read()
data = json.loads(resp)
index = 0
print(len(data))

for candle in data: 
    openP = candle[OPEN]
    closeP = candle[CLOSE]
    if (index > RSIEP):
        rsi = crypt.calcRsi(index,data,RSIEP)
        tempCandleAux = CandleAux(float(rsi), float(closeP), float(candle[OPENTIME]))
        candleAuxList.append(tempCandleAux)
    index += 1

index = 0
for auxCandle in candleAuxList:
    if((index >= 1) and (len(candleAuxList) > 3) and (index < (len(candleAuxList)-1))):
        prevAux = candleAuxList[index-1]
        curAux = candleAuxList[index]
        nextAux = candleAuxList[index + 1]
        if((prevAux.rsi > curAux.rsi) and (nextAux.rsi > curAux.rsi)):
                valleyList.append(curAux)

    index += 1

reversedValleys = valleyList[::-1]
index = 0
for auxCandle in reversedValleys:
#    print("valley @ rsi: %f price: %f  time: %f" %((auxCandle.rsi), (auxCandle.price), (auxCandle.time)))\
    if((index) < (len(reversedValleys) - 1)):
        nextCandle = reversedValleys[index + 1]
        ncPrice = nextCandle.price
        ncRsi = nextCandle.rsi
        curPrice = auxCandle.price
        curRsi = auxCandle.rsi
        if ((curRsi > ncRsi) and (curPrice <= ncPrice)):
            print("bullish div@ rsi: %f price: %f  time: %f" %((auxCandle.rsi), (auxCandle.price), (auxCandle.time)))\

    index += 1
