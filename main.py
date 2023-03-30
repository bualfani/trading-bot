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

# Set the initial capital and risk management parameters
capital = 100
risk_per_trade = 0.02
stop_loss_pct = 0.03

# Define the indicators to use for the strategy
bb_period = 20
rsi_period = 14
macd_fast_period = 12
macd_slow_period = 26
macd_signal_period = 9

# Calculate the maximum amount of capital to risk per trade
risk_amount = capital * risk_per_trade
max_position_size = risk_amount / stop_loss_pct

while True:
    for symbol in stocks + cryptos:
        # Retrieve the historical prices for the symbol
        if symbol in stocks:
            prices = rh.stocks.get_stock_historicals(symbol, interval=interval, span='5year', bounds='regular')
        elif symbol in cryptos:
            prices = rh.crypto.get_crypto_historicals(symbol, interval=interval)

        # Extract the closing prices from the API response
        close_prices = np.array([float(price['close_price']) for price in prices])

        # Calculate the Bollinger Bands for the past bb_period periods
        bb_upper, bb_middle, bb_lower = talib.BBANDS(close_prices, timeperiod=bb_period, nbdevup=2, nbdevdn=2)

        # Calculate the RSI for the past rsi_period periods
        rsi = talib.RSI(close_prices, timeperiod=rsi_period)

        # Calculate the MACD indicator for the past macd_fast_period, macd_slow_period, and macd_signal_period periods
        macd, macdsignal, macdhist = talib.MACD(close_prices, fastperiod=macd_fast_period, slowperiod=macd_slow_period,
                                                signalperiod=macd_signal_period)

        # Check if the price has touched or crossed the upper Bollinger Band and the RSI is overbought (above 70) and
        # the MACD histogram is positive
        if close_prices[-1] >= bb_upper[-1] and rsi[-1] > 70 and macdhist[-1] > 0:
            # Calculate the number of shares to buy based on the available capital and risk management parameters
            price = float(prices[-1]['close_price'])
            if symbol in stocks:
                position_size = min(max_position_size, capital / price)
            elif symbol in cryptos:
                position_size = min(max_position_size * price, capital)
            position_size = round(position_size, 3)

            # Place a buy order for the asset
            if symbol in stocks:
                order = rh.orders.order_sell_limit(symbol, position_size, price)
            elif symbol in cryptos:
                order = rh.orders.order_buy_crypto_by_price(symbol, position_size, price)
            print(f'Bought {position_size} {symbol} at ${price:.2f}')