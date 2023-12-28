import strategies
import fetcher
import pandas as pd
# Fetch stock symbols
stock_symbols = fetcher.get_stock_codes()

#initializing variables
momentum_stocks =[]
mean_reversion_stocks =[]
ema_bb_confluence_stocks = []
volume_breakout =[]
golden_crossover_stocks = []
def shortTerm_pick(stock_symbols):
    global momentum_stocks
    global mean_reversion_stocks
    global ema_bb_confluence_stocks
    momentum_stocks = strategies.strategy_momentum(stock_symbols)  
    mean_reversion_stocks = strategies.strategy_mean_reversion(stock_symbols)
    ema_bb_confluence_stocks = strategies.strategy_EMA_BB_Confluence(stock_symbols)

    # Combine selected stocks from all strategies
    shortTerm_stocks = momentum_stocks + mean_reversion_stocks + ema_bb_confluence_stocks

    # Sort the combined list based on ATH to LTP ratio in ascending order
    shortTerm_stocks.sort(key=lambda x: x[1])

    # Store the sorted list in a CSV file
    df_short_selected_stocks = pd.DataFrame(shortTerm_stocks, columns=['Symbol', 'ATH_to_LTP_Ratio'])
    df_short_selected_stocks.to_csv("shortterm_combined_selected_stocks.csv", index=False)
    return shortTerm_stocks

def midTerm_pick(stock_symbols):
    global volume_breakout
    volume_breakout = strategies.strategy_VolumeBreakout(stock_symbols)
    # Combine selected stocks from all strategies
    midTerm_stocks = momentum_stocks + volume_breakout

    # Sort the combined list based on ATH to LTP ratio in ascending order
    midTerm_stocks.sort(key=lambda x: x[1])

    df_mid_selected_stocks = pd.DataFrame(midTerm_stocks, columns=['Symbol', 'ATH_to_LTP_Ratio'])
    df_mid_selected_stocks.to_csv("midterm_combined_selected_stocks.csv", index=False)
    return midTerm_stocks
def longTerm_pick(stock_symbols):
    global golden_crossover_stocks
    golden_crossover_stocks = strategies.strategy_golden_crossover(stock_symbols)
    # Combine selected stocks from all strategies
    longTerm_stocks = golden_crossover_stocks

    # Sort the combined list based on ATH to LTP ratio in ascending order
    longTerm_stocks.sort(key=lambda x: x[1])

    df_long_selected_stocks = pd.DataFrame(longTerm_stocks, columns=['Symbol', 'Stoploss'])
    df_long_selected_stocks.to_csv("longterm_combined_selected_stocks.csv", index=False)
    return longTerm_stocks


shortterm_top5 = shortTerm_pick(stock_symbols)[1:6]
midterm_top5 = midTerm_pick(stock_symbols)[1:6]
longterm_top5 = longTerm_pick(stock_symbols)[1:6]
#converting to Dataframe Object
df_shortterm_top5 = pd.DataFrame(shortterm_top5, columns=['Symbol', 'ATH_to_LTP_Ratio'])
df_midterm_top5 = pd.DataFrame(midterm_top5, columns=['Symbol', 'ATH_to_LTP_Ratio'])
df_longterm_top5 = pd.DataFrame(longterm_top5, columns=['Symbol', 'Stoploss'])

#converting to CSV file
df_shortterm_top5.to_csv("shortterm best 5.csv", index=False)
df_midterm_top5.to_csv("midterm best 5.csv", index=False)
df_longterm_top5.to_csv("longterm best 5.csv", index=False)