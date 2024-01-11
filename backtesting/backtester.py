import pandas as pd
import strategy

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
    strategy_result = strategy.strategy_EMA_Crossover(stock_data)
    
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
            if current_price_close <= stop_loss or current_price_high <= stop_loss or current_price_low <= stop_loss:
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
