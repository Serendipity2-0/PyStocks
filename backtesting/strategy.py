import Backtesting_Utils

def strategy_VolumeBreakout(stock_data, volume_change_threshold=3):
    if stock_data is not None and len(stock_data) >= 2:
        volume_changes = stock_data['Volume'].pct_change(periods=1).iloc[-2:]  # Calculate volume changes for last 2 days
        avg_volume_change = volume_changes.mean()
        
        if avg_volume_change > volume_change_threshold:
            # Calculate stop loss and target based on strategy rules
            entry_price = stock_data['Close'].iloc[-1]  # Entry price
            stop_loss = entry_price-(0.10 * entry_price)
            target = entry_price + (0.10 * entry_price * 3)  # 3x the stop loss
            
            return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
        else:
            return {'Signal': 'No Signal'}
    else:
        return {'Signal': 'Insufficient Data'}

def strategy_EMA_Crossover(stock_data):
    if stock_data is not None and len(stock_data) >= 53:  # Ensure sufficient data for EMA calculation
        stock_data = stock_data.copy()  # Create a copy to avoid modifying the original DataFrame
        
        stock_data['EMA5'] = Backtesting_Utils.indicator_5EMA(stock_data)
        stock_data['EMA13'] = Backtesting_Utils.indicator_13EMA(stock_data)
        stock_data['EMA26'] = Backtesting_Utils.indicator_26EMA(stock_data)

        # Check for Golden Crossover
        if (stock_data['EMA5'].iloc[-2] < stock_data['EMA13'].iloc[-2] and
            stock_data['EMA13'].iloc[-2] < stock_data['EMA26'].iloc[-2]):
            # Check if the crossover occurred in the last day
            if (stock_data['EMA5'].iloc[-1] > stock_data['EMA13'].iloc[-1] and
                stock_data['EMA13'].iloc[-1] > stock_data['EMA26'].iloc[-1]):
                entry_price = stock_data['Close'].iloc[-1]  # Entry price
                stop_loss = entry_price-(0.10 * entry_price)
                target = entry_price + (0.10 * entry_price * 3) 
                return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
    return {'Signal': 'No Signal'}

def strategy_momentum(stock_data):
    if stock_data is not None and not stock_data.empty:
        # Calculate RSI
        rsi_length_input = 14
        rsi_source_input = 'Close'
        rsi_values = Backtesting_Utils.indicator_RSI(stock_data, rsi_length_input, rsi_source_input)
        
        # Calculate Bollinger Bands
        bb_window = 20
        stock_data = Backtesting_Utils.indicator_bollinger_bands(stock_data, bb_window)
        
        # Check if LTP is above 50 EMA
        stock_data = Backtesting_Utils.strategy_above_50EMA(stock_data)

        macd, signal_line = Backtesting_Utils.indicator_MACD(stock_data)
        
        # Apply momentum Strategy conditions
        if rsi_values.iloc[-1] > 50 and stock_data['Above_50_EMA'].iloc[-1]:
            if stock_data['Upper_band'].iloc[-1] < stock_data['Close'].iloc[-1]:
                if macd.iloc[-1] > signal_line.iloc[-1]:  
                    if stock_data['Volume'].iloc[-1] > stock_data['Volume'].rolling(window=20).mean().iloc[-1]:
                        entry_price = stock_data['Close'].iloc[-1]  # Entry price
                        stop_loss = entry_price-(0.10 * entry_price)
                        target = entry_price + (0.10 * entry_price * 3) 
                        return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
    return {'Signal': 'No Signal'} 

def strategy_vwap(stock_data):
    if stock_data is not None and len(stock_data) >= 103:
            stock_data['EMA5'] = Backtesting_Utils.indicator_5EMA(stock_data)
            stock_data['EMA13'] = Backtesting_Utils.indicator_13EMA(stock_data)
            stock_data['EMA26'] = Backtesting_Utils.indicator_26EMA(stock_data)
            stock_data['EMA50'] = Backtesting_Utils.indicator_50EMA(stock_data)
            stock_data['VWAP'] = Backtesting_Utils.indicator_vwap(stock_data)

            if (
                stock_data['Close'].iloc[-2] < stock_data['EMA5'].iloc[-2] and
                stock_data['Close'].iloc[-2] < stock_data['EMA13'].iloc[-2] and
                stock_data['Close'].iloc[-2] < stock_data['EMA26'].iloc[-2] and
                stock_data['Close'].iloc[-2] < stock_data['EMA50'].iloc[-2] and
                stock_data['Close'].iloc[-2] < stock_data['VWAP'].iloc[-2]
            ):
                if (
                    stock_data['Close'].iloc[-1] > stock_data['EMA5'].iloc[-1] and
                    stock_data['Close'].iloc[-1] > stock_data['EMA13'].iloc[-1] and
                    stock_data['Close'].iloc[-1] > stock_data['EMA26'].iloc[-1] and
                    stock_data['Close'].iloc[-1] > stock_data['EMA50'].iloc[-1] and
                    stock_data['Close'].iloc[-1] > stock_data['VWAP'].iloc[-1]
                ):
                    entry_price = stock_data['Close'].iloc[-1]  # Entry price
                    stop_loss = entry_price-(0.10 * entry_price)
                    target = entry_price + (0.10 * entry_price * 3) 
                    return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
    return {'Signal': 'No Signal'} 

def strategy_ema_bb_confluence(stock_data):
    if stock_data is not None and not stock_data.empty:
        bb_window = 20
        stock_data = Backtesting_Utils.indicator_bollinger_bands(stock_data, bb_window)
        stock_data['EMA_50'] = Backtesting_Utils.indicator_50EMA(stock_data)
        if stock_data['EMA_50'].iloc[-1] <= stock_data['Lower_band'].iloc[-1]:
            if stock_data['Close'].iloc[-1] < stock_data['MA'].iloc[-1]:
                if stock_data['Lower_band'].iloc[-2] < stock_data['Lower_band'].iloc[-3]:
                    if stock_data['Lower_band'].iloc[-1] > stock_data['Lower_band'].iloc[-2]:
                        bollinger_close_to_ema = abs(stock_data['Lower_band'].iloc[-1] - stock_data['EMA_50'].iloc[-1]) < 0.05 * stock_data['Close'].iloc[-1]
                        if bollinger_close_to_ema and stock_data['Volume'].iloc[-1] > stock_data['Volume'].rolling(window=20).mean().iloc[-1]:
                            entry_price = stock_data['Close'].iloc[-1]  # Entry price
                            stop_loss = entry_price-(0.10 * entry_price)
                            target = entry_price + (0.10 * entry_price * 3) 
                            return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
    return {'Signal': 'No Signal'} 
    
def strategy_5_50_EMA_Crossover(stock_data):
    if stock_data is not None and len(stock_data) >= 102:  # Ensure sufficient data for EMA calculation
        stock_data = stock_data.copy()  # Create a copy to avoid modifying the original DataFrame
        
        stock_data['EMA5'] = Backtesting_Utils.indicator_5EMA(stock_data)
        stock_data['EMA50'] = Backtesting_Utils.indicator_50EMA(stock_data)
        stock_data['VWAP'] = Backtesting_Utils.indicator_vwap(stock_data)
        if (stock_data['EMA5'].iloc[-2] < stock_data['EMA50'].iloc[-2] and
            stock_data['EMA5'].iloc[-1] > stock_data['EMA50'].iloc[-1]):
            if stock_data['Close'].iloc[-1] > stock_data['VWAP'].iloc[-1]:
                if stock_data['Volume'].iloc[-1] > stock_data['Volume'].rolling(window=20).mean().iloc[-1]:
                    entry_price = stock_data['Close'].iloc[-1]  # Entry price
                    stop_loss = entry_price-(0.10 * entry_price)
                    target = entry_price + (0.10 * entry_price * 3) 
                    return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
    return {'Signal': 'No Signal'} 
                