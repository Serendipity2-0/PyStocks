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

# Function to apply NR4 strategy
def narrow_range_4_strategy(stock_symbols, period='5d', duration='1d'):
    selected_stocks = []
    for symbol in stock_symbols:
        stock_data = fetchStockData(symbol, period, duration)
        if stock_data is not None and len(stock_data) >= 5:  # Ensure at least 5 days of data for calculation
            stock_data['HighLowRange'] = stock_data['High'] - stock_data['Low']
            min_range = stock_data['HighLowRange'].tail(4).min()  # Calculate the minimum range in the last 4 days
            today_range = stock_data['High'][-1] - stock_data['Low'][-1]  # Today's range
            if today_range <= min_range:
                selected_stocks.append({'Symbol': symbol, 'TodayRange': today_range})
                df_selected_stocks = pd.DataFrame(selected_stocks)
                df_selected_stocks.to_csv("nr4.csv", mode='a', header=False)

# Fetch stock symbols
stock_symbols = fetchCodes()

# Apply NR4 strategy and store selected stocks in Excel
narrow_range_4_strategy(stock_symbols)
