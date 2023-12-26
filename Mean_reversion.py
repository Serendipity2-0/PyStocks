import pandas as pd
import yfinance as yf
import fetcher

def calculate_rsi(data, rsi_length, rsi_source):
    try:
        delta = data[rsi_source].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=rsi_length).mean()
        avg_loss = loss.rolling(window=rsi_length).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    except:
        pass

# Example function to calculate Bollinger Bands
def calculate_bollinger_bands(data, window):
    data['MA'] = data['Close'].rolling(window=window).mean()
    data['Std_dev'] = data['Close'].rolling(window=window).std()
    data['Upper_band'] = data['MA'] + (data['Std_dev'] * 2)
    data['Lower_band'] = data['MA'] - (data['Std_dev'] * 2)
    return data

# Function to check if Last Traded Price (LTP) is above 50 EMA
def check_50_ema(stock_data):
    if stock_data is not None and not stock_data.empty:
        stock_data['EMA_50'] = stock_data['Close'].ewm(span=50, adjust=False).mean()
        stock_data['Above_50_EMA'] = stock_data['Close'] > stock_data['EMA_50']
        return stock_data
    else:
        return None

# Function to apply Mean Reversion Strategy
def mean_reversion_strategy(stock_symbols):
    selected_stocks = []
    
    for symbol in stock_symbols:
        stock_data = fetcher.get_stock_data(symbol, period="2y", duration="1d")
        
        if stock_data is not None and not stock_data.empty:
            # Calculate RSI
            rsi_length_input = 14
            rsi_source_input = 'Close'
            rsi_values = calculate_rsi(stock_data, rsi_length_input, rsi_source_input)
            
            # Calculate Bollinger Bands
            bb_window = 20
            stock_data = calculate_bollinger_bands(stock_data, bb_window)
            
            # Check if LTP is above 50 EMA
            stock_data = check_50_ema(stock_data)
            
            # Apply Mean Reversion Strategy conditions
            if rsi_values.iloc[-1] < 40 and stock_data['Above_50_EMA'].iloc[-1]:
                if stock_data['Lower_band'].iloc[-2] < stock_data['Lower_band'].iloc[-3]:
                    if stock_data['Lower_band'].iloc[-1] > stock_data['Lower_band'].iloc[-2]:
                        selected_stocks.append(symbol)
                        df_selected_stocks = pd.DataFrame(selected_stocks, columns=['Symbol'])
                        df_selected_stocks.to_csv("MeanReversion.csv", mode='a', header=False)  
                

# Fetch stock symbols
stock_symbols = fetcher.get_stock_codes()
# Apply Mean Reversion Strategy and store selected stocks
mean_reversion_strategy(stock_symbols)

