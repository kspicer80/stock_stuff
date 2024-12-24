import talib

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    close_prices = df['Close'].values.flatten()  # Ensure 'Close' column is a 1D array
    macd, macd_signal, macd_hist = talib.MACD(close_prices, fastperiod=short_period, slowperiod=long_period, signalperiod=signal_period)
    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal
    df['MACD_Hist'] = macd_hist
    return df

def calculate_rsi(df, period=14):
    close_prices = df['Close'].values.flatten()  # Ensure 'Close' column is a 1D array
    df['RSI'] = talib.RSI(close_prices, timeperiod=period)
    return df

def calculate_bollinger_bands(df, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0):
    close_prices = df['Close'].values.flatten()  # Ensure 'Close' column is a 1D array
    upperband, middleband, lowerband = talib.BBANDS(close_prices, timeperiod, nbdevup, nbdevdn, matype)
    df['UpperBand'] = upperband
    df['MiddleBand'] = middleband
    df['LowerBand'] = lowerband
    return df

def calculate_stochastic(df, fastk_period=14, slowk_period=3, slowd_period=3):
    high_prices = df['High'].values.flatten()  # Ensure 'High' column is a 1D array
    low_prices = df['Low'].values.flatten()    # Ensure 'Low' column is a 1D array
    close_prices = df['Close'].values.flatten()  # Ensure 'Close' column is a 1D array
    slowk, slowd = talib.STOCH(high_prices, low_prices, close_prices, fastk_period, slowk_period, slowd_period)
    df['SlowK'] = slowk
    df['SlowD'] = slowd
    return df

def calculate_atr(df, timeperiod=14):
    high_prices = df['High'].values.flatten()  # Ensure 'High' column is a 1D array
    low_prices = df['Low'].values.flatten()    # Ensure 'Low' column is a 1D array
    close_prices = df['Close'].values.flatten()  # Ensure 'Close' column is a 1D array
    df['ATR'] = talib.ATR(high_prices, low_prices, close_prices, timeperiod)
    return df