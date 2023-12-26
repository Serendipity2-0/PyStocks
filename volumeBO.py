
import pandas as pd
import yfinance as yf
import schedule
import time
import fetcher

# Function to check volume change and store in CSV
def storeStocksWithVolumeChange(stockSymbols, period='2d', duration='1d', volume_change_threshold=3):
    for symbol in stockSymbols:
        stock_data = fetcher.get_stock_data(symbol, period, duration)
        stock_data['Symbol'] = symbol
        if stock_data is not None and len(stock_data) >= 2:
            volume_changes = stock_data['Volume'].pct_change(periods=1).iloc[-2:]  # Calculate volume changes for last 2 days
            avg_volume_change = volume_changes.mean()
            if avg_volume_change > volume_change_threshold:
                stock_data.to_csv("significant_volume_changes.csv", mode='a', header=False)  
                print(f"Stock symbol {symbol} has a volume change more than 3x:\n{stock_data}\n")

# Function to run the script at 9 AM daily
def run_script():
    print("Running script at 9 AM...")
    stockSymbols = fetcher.get_stock_codes()
    storeStocksWithVolumeChange(stockSymbols)

# Schedule the script to run daily at 9 AM
schedule.every().day.at("09:00").do(run_script)

# Keep the script running to allow schedule to execute
while True:
    schedule.run_pending()
    time.sleep(60)  # Check schedule every minute
