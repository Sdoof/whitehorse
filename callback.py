#API
# SYM = FrankiesSystem(symbol, getHistory)
# SYM.save()

def getHistory(symbol, maxlookback):
    #richie you do this
    #return pd.DataFrame(history)
    return

class FrankiesSystem(symbol, getHistory):
    def __init__(self):
        maxlookback = 20
        symbol = self.symbol
        history = self.getHistory(symbol, maxlookback)


    def save(self):
        history = self.getHistory(symbol, maxlookback)
        calcsignal(history)
        #write to db.
        pass