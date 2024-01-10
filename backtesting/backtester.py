import pandas as pd

# Function to implement the backtesting strategy
def strategy_VolumeBreakout(stock_data, volume_change_threshold=3):
    if stock_data is not None and len(stock_data) >= 2:
        volume_changes = stock_data['Volume'].pct_change(periods=1).iloc[-2:]  # Calculate volume changes for last 2 days
        avg_volume_change = volume_changes.mean()
        
        if avg_volume_change > volume_change_threshold:
            # Calculate stop loss and target based on strategy rules
            entry_price = stock_data['Close'].iloc[-1]  # Entry price
            stop_loss = 0.10 * entry_price
            stop = entry_price - stop_loss
            target = entry_price + (stop * 3)  # 3x the stop loss
            
            return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
        else:
            return {'Signal': 'No Signal'}
    else:
        return {'Signal': 'Insufficient Data'}

def strategy_EMA_Crossover(stock_data):
    if stock_data is not None and len(stock_data) >= 53:  # Ensure sufficient data for EMA calculation
        stock_data = stock_data.copy()  # Create a copy to avoid modifying the original DataFrame
        
        stock_data['EMA5'] = stock_data['Close'].ewm(span=5, min_periods=0, adjust=False).mean()
        stock_data['EMA13'] = stock_data['Close'].ewm(span=13, min_periods=0, adjust=False).mean()
        stock_data['EMA26'] = stock_data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()

        # Check for Golden Crossover
        if (stock_data['EMA5'].iloc[-2] < stock_data['EMA13'].iloc[-2] and
            stock_data['EMA13'].iloc[-2] < stock_data['EMA26'].iloc[-2]):
            # Check if the crossover occurred in the last day
            if (stock_data['EMA5'].iloc[-1] > stock_data['EMA13'].iloc[-1] and
                stock_data['EMA13'].iloc[-1] > stock_data['EMA26'].iloc[-1]):
                entry_price = stock_data['Close'].iloc[-1]  # Entry price
                stop_loss = 0.05 * entry_price
                stop = entry_price - stop_loss
                target = entry_price + (stop * 3)  # 3x the stop loss
                return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
    return {'Signal': 'No Signal'}

# Load historical stock data
data = pd.read_csv('RELIANCE.csv')  # Replace 'RELIANCE.csv' with the filename of Reliance historical data

# Backtesting and calculating Net PnL and Hit Ratio
capital = 1000000  # Initial capital
trades = 0
winning_trades = 0
net_pnl = 0

for i in range(len(data)):
    stock_data = data.iloc[:i + 1].copy()  # Iterate through historical data from the beginning up to the current index
    
    # Apply strategy function to get signals
    strategy_result = strategy_VolumeBreakout(stock_data)
    
    if strategy_result['Signal'] == 'Buy':
        entry = strategy_result['Entry_price']
        trades += 1
        stop_loss = strategy_result['Stop_loss']
        target = strategy_result['Target']
        current_index = i
        
        # Loop through stock data until stop loss or target is triggered
        while current_index < len(data):
            current_price_close = data['Close'].iloc[current_index]  # Get current price
            current_price_high = data['High'].iloc[current_index] 
            current_price_low = data['Low'].iloc[current_index] 
            
            # Check if price hits stop loss or target
            if current_price_close <= stop_loss:
                net_pnl -= entry - stop_loss
                break  # Exit loop if stop loss is triggered
            elif current_price_close >= target or current_price_high >= target or current_price_low >= target:
                net_pnl += entry + target
                winning_trades += 1
                break  # Exit loop if target is triggered
            
            current_index += 1  # Move to the next day

# Calculate hit ratio
hit_ratio = (winning_trades / trades) * 100 if trades > 0 else 0

print(f"Net Profit/Loss: {net_pnl}")
print(f"Hit Ratio: {hit_ratio}%")
print(f"Winning Trades: {winning_trades}")
print(f"Total Trades: {trades}")
