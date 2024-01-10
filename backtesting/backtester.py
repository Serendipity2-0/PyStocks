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
            stop = entry_price-stop_loss
            target = entry_price+(stop*2)  # 3x the stop loss
            
            return {'Signal': 'Buy', 'Entry_price': entry_price, 'Stop_loss': stop_loss, 'Target': target}
        else:
            return {'Signal': 'No Signal'}
    else:
        return {'Signal': 'Insufficient Data'}


# Load historical stock data
data = pd.read_csv('RELIANCE.csv')  # Replace 'RELIANCE.csv' with the filename of Reliance historical data

# Backtesting and calculating Net PnL and Hit Ratio
capital = 1000000  # Initial capital
trades = 0
winning_trades = 0
net_pnl = 0

for i in range(len(data)):
    stock_data = data.iloc[:i + 1]  # Iterate through historical data from the beginning up to the current index
    
    # Apply strategy function to get signals
    strategy_result = strategy_VolumeBreakout(stock_data)
    
    if strategy_result['Signal'] == 'Buy':
        entry = strategy_result['Entry_price']
        trades += 1
        stop_loss = strategy_result['Stop_loss']
        target = strategy_result['Target']
        current_index = 0
        
        # Loop through stock data until stop loss or target is triggered
        while current_index < len(stock_data):
            current_price = stock_data['Close'].iloc[current_index]  # Get current price
            
            # Check if price hits stop loss or target
            if current_price <= stop_loss:
                net_pnl -= entry-stop_loss
                break  # Exit loop if stop loss is triggered
            elif current_price >= target:
                net_pnl += entry+target
                winning_trades += 1
                break  # Exit loop if target is triggered
            
            current_index += 1  # Move to the next day
        
# Calculate hit ratio
hit_ratio = (winning_trades / trades) * 100 if trades > 0 else 0

print(f"Net Profit/Loss: {net_pnl}")
print(f"Hit Ratio: {hit_ratio}%")
print(f"Winning Trades: {winning_trades}")
print(f"Total Trades: {trades}")
