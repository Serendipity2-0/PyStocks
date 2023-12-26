import pandas as pd
import yfinance as yf

def fetchCodes():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    return list(pd.read_csv(url)['SYMBOL'].values)

def fetchStockData(stockCode, period, duration):
    try:
        append_exchange = ".NS"
        data = yf.download(
            tickers=stockCode + append_exchange,
            period=period,
            interval=duration)
        return data
    except Exception as e:
        print(f"Error fetching data for {stockCode}: {e}")
        return None

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

# Function to calculate MACD
def calculate_macd(data, fast_length=12, slow_length=26, signal_length=9):
    data['EMA_fast'] = data['Close'].ewm(span=fast_length, adjust=False).mean()
    data['EMA_slow'] = data['Close'].ewm(span=slow_length, adjust=False).mean()
    data['MACD'] = data['EMA_fast'] - data['EMA_slow']
    data['Signal_line'] = data['MACD'].ewm(span=signal_length, adjust=False).mean()
    return data['MACD'], data['Signal_line']

def Momentum_strategy(stock_symbols):
    selected_stocks = []
    
    for symbol in stock_symbols:
        stock_data = fetchStockData(symbol, period="2y", duration="1d")
        
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
            
            # Apply momentum Strategy conditions
            if rsi_values.iloc[-1] > 50 and stock_data['Above_50_EMA'].iloc[-1]:
                if stock_data['Upper_band'].iloc[-1] < stock_data['Close'].iloc[-1]:
                    macd, signal_line = calculate_macd(stock_data)
                    if macd.iloc[-1] > signal_line.iloc[-1]:  # Condition 4
                        selected_stocks.append(symbol)
                        df_selected_stocks = pd.DataFrame(selected_stocks, columns=['Symbol'])
                        df_selected_stocks.to_csv("Momentum.csv", mode='a', header=False)  
                

# Fetch stock symbols
stock_symbols = fetchCodes()
# Apply Momentum Strategy and store selected stocks
Momentum_strategy(stock_symbols)

