# Here is a reference snippet of code from backtesting\indicators.py:
def indicator_5EMA(stock_data):
    return stock_data['Close'].ewm(span=5, min_periods=0, adjust=False).mean()

def indicator_13EMA(stock_data):
    return stock_data['Close'].ewm(span=13, min_periods=0, adjust=False).mean()

def indicator_26EMA(stock_data):
    return stock_data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()

def indicator_50EMA(stock_data):
    return stock_data['Close'].ewm(span=50, min_periods=0, adjust=False).mean()
    
