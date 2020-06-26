OPEN = 1
CLOSE = 4

def rma(prevRma, delta, epoch):
    #retRma = ((epoch - 1) * prevRma + delta) / epoch
    retRma = (delta - prevRma) * (1/epoch) + prevRma
    return retRma



def calcRsi (index, data, epoch):
    rsi = 0.0
    gain = 0.0
    loss = 0.0
    rmaLoss = 0
    rmaGain = 0
    
    if index >= epoch:
        for i in range(1, index+1):
            ##previous close
            prevClose = data[i-1][CLOSE]
            curClose = data[i][CLOSE]
            prevCloseF = float(prevClose)
            curCloseF = float(curClose)
            if (curCloseF > prevCloseF):
                rmaGain = rma(rmaGain, curCloseF - prevCloseF, epoch)
                rmaLoss = rma(rmaLoss, 0, epoch)
            else:
                rmaGain = rma(rmaGain, 0, epoch)
                rmaLoss = rma(rmaLoss, prevCloseF - curCloseF, epoch)

    averageGain = rmaGain
    averageLoss = rmaLoss
    if averageLoss != 0:
        rs = (averageGain)/(averageLoss)
        rsi = 100.0 - 100/(1.0 + rs)
    else: 
        rsi = 100
    return rsi

