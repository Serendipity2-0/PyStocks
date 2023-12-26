import strategies
import fetcher

# Fetch stock symbols
stock_symbols = fetcher.get_stock_codes()

print("Select the Strategy you want to run:\n1. Momentum\n2. Mean Reversion\n3. NR4\n4. Volume Breakout\n5. Golden Crossover")
execute_option = int(input("Enter your option: "))
if execute_option == 1:
    strategies.strategy_momentum(stock_symbols)
elif execute_option == 2:
    strategies.strategy_mean_reversion(stock_symbols)
elif execute_option == 3:
    strategies.strategy_nr4(stock_symbols)
elif execute_option == 4: 
    strategies.strategy_VolumeBreakout(stock_symbols)
elif execute_option == 5:
    strategies.strategy_golden_crossover(stock_symbols, period='1y', duration='1d')
else:
    print("Invalid Option")
    pass