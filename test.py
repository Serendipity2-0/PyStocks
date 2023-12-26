import pandas as pd
import numpy as np

def ma(source, length, type):
    if type == "SMA" or type == "Bollinger Bands":
        return source.rolling(window=length).mean()
    elif type == "EMA":
        return source.ewm(span=length, adjust=False).mean()
    elif type == "SMMA (RMA)":
        return source.rolling(window=length).apply(lambda x: (x * (2 / (length + 1))).sum() / (2 / (length + 1)), raw=True)
    elif type == "WMA":
        weights = np.arange(1, length + 1)
        wma = source.rolling(window=length).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)
        return wma
    elif type == "VWMA":
        volume = pd.Series(data=[1000, 1200, 1500, 800, 950])  # Replace this with actual volume data
        vwma = (source * volume).rolling(window=length).sum() / volume.rolling(window=length).sum()
        return vwma
    else:
        return None

def calculate_rsi(data, rsi_length, rsi_source):
    delta = data[rsi_source].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=rsi_length).mean()
    avg_loss = loss.rolling(window=rsi_length).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Example usage
data = pd.DataFrame({
    'Close': [100, 110, 90, 95, 105, 115, 120, 125, 130, 120,110,120,200,239,140,100],
    'Volume': [1000, 1200, 1500, 800, 950, 1100, 900, 850, 1000, 950, 500, 620, 1000,450,2300,4500]  # Replace this with actual volume data
})

rsi_length_input = 14
rsi_source_input = 'Close'
ma_type_input = 'SMA'
ma_length_input = 14
bb_mult_input = 2.0

rsi_values = calculate_rsi(data, rsi_length_input, rsi_source_input)

# Printing RSI values and Bollinger Bands (if applicable)
print("RSI Values:")
print(rsi_values)
