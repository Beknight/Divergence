import urllib.request 
import json
import numpy as np
import datetime as dt
import rsi as crypt
import collections
import pendulum
import time
import sendEmail as em
import notify as ntfy
from collections import namedtuple

def buildSigValleyList(valleyList):
    sigValley = []
    length = len(valleyList)
    
    #add the first valley
    for i,valley in enumerate(valleyList): 
        # first valley is always significant
        if i == 0:
            sigValley.append(valley)
        else:
            #if the valley right valley and prev valley are > then sig valley 
            if i < (length-1):
                left = valleyList[i - 1]
                right = valleyList[i + 1]
                if (left.rsi > valley.rsi) and (right.rsi > valley.rsi):
                    sigValley.append(valley)
                    utctime = valley.time//1000
                    pendulum.from_timestamp(utctime).to_datetime_string()
                    newtime = pendulum.from_timestamp(utctime, 'Australia/Sydney').to_datetime_string()
                    printText = "significant valley @" + str(valley.rsi) + " time: " + str(newtime)

    return sigValley

def grabData(url):
    resp = ""
    data = []
    try:
        resp = urllib.request.urlopen(url).read()
    except: 
        data=[]
        print("failed data grab")
    
    data = json.loads(resp.decode('utf-8'))
    #data = resp.json()
    return data 

CandleAux = namedtuple("CandleAux", "rsi price time")
OPENTIME = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
RSIEP = 8
VALLEYS_TO_CHECK = 3
candleAuxList = []
valleyList = []

root_url = 'https://api.binance.com/api/v1/klines'
interval = '5m'
intervalList = ['5m','30m']
divDict = {"XRPUSDT5m": "", "XRPUSDT30m":"", "TRXUSDT5m":"","TRXUSDT30m":"", "NEOUSDT5m":"", "NEOUSDT30m":"", "ADAUSDT5m":"", "ADAUSDT30m":""}
symbolList = ['XRPUSDT', 'TRXUSDT', 'NEOUSDT', 'ADAUSDT']

while(1):
    for interval in intervalList:
        for symbol in symbolList:
            url = root_url + '?symbol=' + symbol + '&interval=' + interval
            data = grabData(url)
            candleAuxList = []
            valleyList = []

            for index,candle in enumerate(data): 
                openP = candle[OPEN]
                closeP = candle[CLOSE]
                if (index > RSIEP):
                    rsi = crypt.calcRsi(index,data,RSIEP)
                    tempCandleAux = CandleAux(float(rsi), float(closeP), float(candle[OPENTIME]))
                    candleAuxList.append(tempCandleAux)

            for index,auxCandle in enumerate(candleAuxList):
                if((index >= 1) and (len(candleAuxList) > 3) and (index < (len(candleAuxList)-1))):
                    prevAux = candleAuxList[index-1]
                    curAux = candleAuxList[index]
                    nextAux = candleAuxList[index + 1]
                    if((prevAux.rsi > curAux.rsi) and (nextAux.rsi > curAux.rsi)):
                            valleyList.append(curAux)

            reversedValleys = valleyList[::-1]
            divFound = False
           
            reversedValleys = buildSigValleyList(reversedValleys)

            for index,auxCandle in enumerate(reversedValleys):
                if index < (len(reversedValleys) - 1):
                    count = 0; 
                    while (((index + count) < (len(reversedValleys)-1)) and (count < VALLEYS_TO_CHECK)): 
                        nextCandle = reversedValleys[index + count]
                        ncPrice = nextCandle.price
                        ncRsi = nextCandle.rsi
                        curPrice = auxCandle.price
                        curRsi = auxCandle.rsi
                        if (curRsi > ncRsi) and (curPrice <= ncPrice):
                            utctime = auxCandle.time//1000
                            pendulum.from_timestamp(utctime).to_datetime_string()
                            newtime = pendulum.from_timestamp(utctime, 'Australia/Sydney').to_datetime_string()
                            count = VALLEYS_TO_CHECK
                            tempString = "bullish div@ rsi: " + str(auxCandle.rsi) + " price: " + str(auxCandle.price) + " time: " + newtime + " interval: " + interval
                            key = symbol + interval
                            if divDict[key] != tempString:
                                print(key)
                                print(tempString)
                                divDict[key] = tempString
                                ntfy.sendMessage(key + tempString)
                            divFound = True
                            break
                        count += 1
                if (divFound):
                    break
    time.sleep(25)
