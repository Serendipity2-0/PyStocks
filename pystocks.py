import strategies
import fetcher
import pandas as pd
# Fetch stock symbols
stock_symbols = fetcher.get_stock_codes()
def shortTerm_pick(stock_symbols):
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

def midTerm_pick(stock_symbols):
    momentum_stocks = strategies.strategy_momentum(stock_symbols)
    volume_breakout = strategies.strategy_VolumeBreakout(stock_symbols)
    # Combine selected stocks from all strategies
    midTerm_stocks = momentum_stocks + volume_breakout

    # Sort the combined list based on ATH to LTP ratio in ascending order
    midTerm_stocks.sort(key=lambda x: x[1])

    df_mid_selected_stocks = pd.DataFrame(midTerm_stocks, columns=['Symbol', 'ATH_to_LTP_Ratio'])
    df_mid_selected_stocks.to_csv("midterm_combined_selected_stocks.csv", index=False)

def longTerm_pick(stock_symbols):
    golden_crossover_stocks = strategies.strategy_golden_crossover(stock_symbols)
    # Combine selected stocks from all strategies
    longTerm_stocks = golden_crossover_stocks

    # Sort the combined list based on ATH to LTP ratio in ascending order
    longTerm_stocks.sort(key=lambda x: x[1])

    df_long_selected_stocks = pd.DataFrame(longTerm_stocks, columns=['Symbol', 'Stoploss'])
    df_long_selected_stocks.to_csv("longterm_combined_selected_stocks.csv", index=False)


shortTerm_pick(stock_symbols)
midTerm_pick(stock_symbols)
longTerm_pick(stock_symbols)
