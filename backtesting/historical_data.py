import pandas as pd
import yfinance as yf

def get_stock_codes():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    return list(pd.read_csv(url)['SYMBOL'].values)

def get_stock_data(stockCode, period, duration):
    try:
        append_exchange = ".NS"
        data = yf.download(
            tickers=stockCode + append_exchange,
            period=period,
            interval=duration)
        return data
    except Exception as e:
        return str(e)

def fetch_nse_stock_data(start_date, end_date):
    stock_codes = get_stock_codes()
    error_stocks = []
    for code in stock_codes:
        data_dict = {}
        stock_data = get_stock_data(code, start_date, end_date)
        if isinstance(stock_data, pd.DataFrame) and not stock_data.empty:
            stock_data.reset_index(inplace=True)
            stock_data['Symbol'] = code
            data_dict[code] = stock_data
        else:
            error_stocks.append(code)
        if data_dict:
            combined_data = pd.concat(data_dict.values())
            combined_data = combined_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            combined_data.to_csv(f'{code}.csv', index=False)
    if error_stocks:
        print(f"Error fetching data for these stocks: {error_stocks}")


period='1y'
duration='1d'
# Fetch NSE stock data and save it to CSV
fetch_nse_stock_data(period, duration)
