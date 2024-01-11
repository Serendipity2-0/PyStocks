import pandas as pd
import strategy

# Load historical stock data
data = pd.read_csv('C:\\Users\\phchi\\Desktop\\python - Serebdipity\\PyStocks\\RELIANCE.csv')  # Replace 'RELIANCE.csv' with the filename of Reliance historical data

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
        trailing_stop_loss = stop_loss
        stop = entry - trailing_stop_loss
        
        # Loop through stock data until stop loss or target is triggered
        while current_index < len(data):
            current_price_close = data['Close'].iloc[current_index]  # Get current price
            current_price_high = data['High'].iloc[current_index] 
            current_price_low = data['Low'].iloc[current_index]
            
            if current_price_close >= entry + (stop * 0.5):
                trailing_stop_loss = trailing_stop_loss + (trailing_stop_loss * 0.5)  # Update trailing stop loss
                stop = entry - trailing_stop_loss
            
            if current_price_close <= trailing_stop_loss or current_price_high <= trailing_stop_loss or current_price_low <= trailing_stop_loss:
                if trailing_stop_loss > entry:
                    net_pnl += trailing_stop_loss - entry
                    winning_trades += 1
                    break  # Exit loop if stop loss is triggered
                else:
                    net_pnl -= entry - trailing_stop_loss
                    break  # Exit loop if stop loss is triggered
            current_index += 1  # Move to the next day

# Calculate hit ratio
hit_ratio = (winning_trades / trades) * 100 if trades > 0 else 0

print(f"Net Profit/Loss: {net_pnl}")
print(f"Hit Ratio: {hit_ratio}%")
print(f"Winning Trades: {winning_trades}")
print(f"Total Trades: {trades}")
