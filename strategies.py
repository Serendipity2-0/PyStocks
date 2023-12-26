import pandas as pd
import yfinance as yf
import fetcher
import TA_indicators

def strategy_VolumeBreakout(stockSymbols, period='2d', duration='1d', volume_change_threshold=3):
    for symbol in stockSymbols:
        stock_data = fetcher.get_stock_data(symbol, period, duration)
        stock_data['Symbol'] = symbol
        if stock_data is not None and len(stock_data) >= 2:
            volume_changes = stock_data['Volume'].pct_change(periods=1).iloc[-2:]  # Calculate volume changes for last 2 days
            avg_volume_change = volume_changes.mean()
            if avg_volume_change > volume_change_threshold:
                stock_data.to_csv("significant_volume_changes.csv", mode='a', header=False)  
                print(f"Stock symbol {symbol} has a volume change more than 3x:\n{stock_data}\n")

def strategy_nr4(stock_symbols, period='5d', duration='1d'):
    selected_stocks = []
    for symbol in stock_symbols:
        stock_data = fetcher.get_stock_data(symbol, period, duration)
        if stock_data is not None and len(stock_data) >= 5:  # Ensure at least 5 days of data for calculation
            stock_data['HighLowRange'] = stock_data['High'] - stock_data['Low']
            min_range = stock_data['HighLowRange'].tail(4).min()  # Calculate the minimum range in the last 4 days
            today_range = stock_data['High'][-1] - stock_data['Low'][-1]  # Today's range
            if today_range <= min_range:
                selected_stocks.append({'Symbol': symbol, 'TodayRange': today_range})
                df_selected_stocks = pd.DataFrame(selected_stocks)
                df_selected_stocks.to_csv("nr4.csv", mode='a', header=False)

def strategy_golden_crossover(stock_symbols, period='1y', duration='1d'):
    selected_stocks = []
    for symbol in stock_symbols:
        stock_data = fetcher.get_stock_data(symbol, period, duration)
        if stock_data is not None and len(stock_data) >= 26:  # Ensure sufficient data for EMA calculation
            stock_data['EMA5'] = TA_indicators.indicator_5EMA(stock_data)
            stock_data['EMA13'] = TA_indicators.indicator_13EMA(stock_data)
            stock_data['EMA26'] = TA_indicators.indicator_26EMA(stock_data)

            # Check for Golden Crossover
            if stock_data['EMA5'].iloc[-2] < stock_data['EMA13'].iloc[-2] and \
               stock_data['EMA13'].iloc[-2] < stock_data['EMA26'].iloc[-2]:
                if stock_data['EMA5'].iloc[-1] > stock_data['EMA13'].iloc[-1] and \
                stock_data['EMA13'].iloc[-1] > stock_data['EMA26'].iloc[-1]:
                    selected_stocks.append({'Symbol': symbol})
                    df_selected_stocks = pd.DataFrame(selected_stocks)
                    df_selected_stocks.to_csv('golden_crossover_selected_stocks.csv', index=False)

def strategy_above_50EMA(stock_data):
    if stock_data is not None and not stock_data.empty:
        stock_data['EMA_50'] = TA_indicators.indicator_50EMA(stock_data)
        stock_data['Above_50_EMA'] = stock_data['Close'] > stock_data['EMA_50']
        return stock_data
    else:
        return None
    
def strategy_momentum(stock_symbols):
    selected_stocks = []
    
    for symbol in stock_symbols:
        stock_data = fetcher.get_stock_data(symbol, period="2y", duration="1d")
        
        if stock_data is not None and not stock_data.empty:
            # Calculate RSI
            rsi_length_input = 14
            rsi_source_input = 'Close'
            rsi_values = TA_indicators.indicator_RSI(stock_data, rsi_length_input, rsi_source_input)
            
            # Calculate Bollinger Bands
            bb_window = 20
            stock_data = TA_indicators.indicator_bollinger_bands(stock_data, bb_window)
            
            # Check if LTP is above 50 EMA
            stock_data = strategy_above_50EMA(stock_data)

            macd, signal_line = TA_indicators.indicator_MACD(stock_data)
            
            # Apply momentum Strategy conditions
            if rsi_values.iloc[-1] > 50 and stock_data['Above_50_EMA'].iloc[-1]:
                if stock_data['Upper_band'].iloc[-1] < stock_data['Close'].iloc[-1]:
                    if macd.iloc[-1] > signal_line.iloc[-1]:  # Condition 4
                        selected_stocks.append(symbol)
                        df_selected_stocks = pd.DataFrame(selected_stocks, columns=['Symbol'])
                        df_selected_stocks.to_csv("Momentum.csv", mode='a', header=False)  
  
def strategy_mean_reversion(stock_symbols):
    selected_stocks = []
    for symbol in stock_symbols:
        stock_data = fetcher.get_stock_data(symbol, period="2y", duration="1d")
        
        if stock_data is not None and not stock_data.empty:
            # Calculate RSI
            rsi_length_input = 14
            rsi_source_input = 'Close'
            rsi_values = TA_indicators.indicator_RSI(stock_data, rsi_length_input, rsi_source_input)
            # Calculate Bollinger Bands
            bb_window = 20
            stock_data = TA_indicators.indicator_bollinger_bands(stock_data, bb_window)
            # Check if LTP is above 50 EMA
            stock_data = strategy_above_50EMA(stock_data)
            # Apply Mean Reversion Strategy conditions
            if rsi_values.iloc[-1] < 40 and stock_data['Above_50_EMA'].iloc[-1]:
                if stock_data['Lower_band'].iloc[-2] < stock_data['Lower_band'].iloc[-3]:
                    if stock_data['Lower_band'].iloc[-1] > stock_data['Lower_band'].iloc[-2]:
                        selected_stocks.append(symbol)
                        df_selected_stocks = pd.DataFrame(selected_stocks, columns=['Symbol'])
                        df_selected_stocks.to_csv("MeanReversion.csv", mode='a', header=False)  
            