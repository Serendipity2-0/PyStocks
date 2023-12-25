import pandas as pd
import yfinance as yf

# Function to fetch stock symbols
def fetchCodes():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    return list(pd.read_csv(url)['SYMBOL'].values)

# Function to fetch stock data
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

# Function to apply Golden Crossover strategy
def golden_crossover_strategy(stock_symbols, period='1y', duration='1d'):
    selected_stocks = []
    for symbol in stock_symbols:
        stock_data = fetchStockData(symbol, period, duration)
        if stock_data is not None and len(stock_data) >= 26:  # Ensure sufficient data for EMA calculation
            stock_data['EMA5'] = stock_data['Close'].ewm(span=5, min_periods=0, adjust=False).mean()
            stock_data['EMA13'] = stock_data['Close'].ewm(span=13, min_periods=0, adjust=False).mean()
            stock_data['EMA26'] = stock_data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()

            # Check for Golden Crossover
            if stock_data['EMA5'].iloc[-2] < stock_data['EMA13'].iloc[-2] and \
               stock_data['EMA13'].iloc[-2] < stock_data['EMA26'].iloc[-2]:
                if stock_data['EMA5'].iloc[-1] > stock_data['EMA13'].iloc[-1] and \
                stock_data['EMA13'].iloc[-1] > stock_data['EMA26'].iloc[-1]:
                    selected_stocks.append({'Symbol': symbol})
                    df_selected_stocks = pd.DataFrame(selected_stocks)
                    df_selected_stocks.to_csv('golden_crossover_selected_stocks.csv', index=False)

# Fetch stock symbols
stock_symbols = fetchCodes()

# Apply Golden Crossover strategy and store selected stocks in CSV
golden_crossover_strategy(stock_symbols)
