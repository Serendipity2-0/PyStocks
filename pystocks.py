import strategies
import fetcher

# Fetch stock symbols
stock_symbols = fetcher.get_stock_codes()

print("Select the Strategy you want to run:\n1. Momentum\n2. Mean Reversion\n3. NR4\n4. Volume Breakout\n5. Golden Crossover\n6. Bollinger Band Fail\n7. EMA and BB Confluence")
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
    strategies.strategy_golden_crossover(stock_symbols)
elif execute_option == 6:
    strategies.strategy_BollingerBand_Fail(stock_symbols)
elif execute_option == 7:
    stock_symbols = ['LT', 'RELIANCE', 'BAJFINANCE', 'HEROMOTOCO', 'HCLTECH', 'TCS', 'TITAN', 'APOLLOHOSP', 'ADANIENT', 'TECHM']
    timeframe = int(input("Enter timeframe: \n 1. Hourly \n 2. 15 mins"))
    if timeframe == 1:#Hourly
        strategies.strategy_EMA_BB_Confluence(stock_symbols, '20d', '1h')
    elif timeframe == 2:#15mins
        strategies.strategy_EMA_BB_Confluence(stock_symbols, '10d', '15m')
else:
    print("Invalid Option")
    pass