import robin_stocks.robinhood as rh
import talib
import numpy as np
import time

# Login to Robinhood
rh.login(username='username', password='people')

rh.build_holdings()

# Define the symbols and time period for analysis
stocks = ['AAPL', 'TSLA', 'NFLX', 'UNH', 'JNJ', 'NVO', 'PFE', 'ABT', 'CVS', 'DIS', 'BABA', 'F', 'META', 'SNAP', 'TECK',
          'MSFT', 'GOOG', 'GOOGL', 'AMZN', 'NVDA', 'TSM', 'AVGO', 'ORCL', 'ADBE', 'AMD', 'QCOM', 'IBM', 'SONY', 'SPGI']
cryptos = ['BTC', 'ETH', 'LTC', 'BCH', 'SOL', 'ETC', 'MATIC', 'DOGE', 'SHIB', 'ADA', 'UNI', 'LINK', 'COMP', 'AAVE', 'XTZ']
interval = 'day'