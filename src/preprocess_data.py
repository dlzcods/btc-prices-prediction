import pandas as pd
import os

def preprocess_data():
    os.makedirs('data', exist_ok=True)
    os.makedirs('src', exist_ok=True)

    try:
        df = pd.read_csv('data/btc_historical_data.csv')
    except FileNotFoundError:
        print("Error: The file 'data/btc_historical_data.csv' does not exist.")
        return

    if df.empty:
        print("Error: The DataFrame is empty. Check the 'data/btc_historical_data.csv' file.")
        return

    required_columns = ['date', 'high', 'low', 'open', 'volume', 'marketcap', 'close']
    if not all(column in df.columns for column in required_columns):
        print(f"Error: Missing required columns in the DataFrame. Required columns: {required_columns}")
        return

    df['date'] = pd.to_datetime(df['date'])
    last_date = df['date'].iloc[-1]

    # Perform shifting on the data
    df['high_shifted'] = df['high'].shift(5)
    df['low_shifted'] = df['low'].shift(5)
    df['open_shifted'] = df['open'].shift(5)
    df['volume_shifted'] = df['volume'].shift(5)
    df['marketcap_shifted'] = df['marketcap'].shift(5)
    df['prediction_5D'] = df['close'].shift(5)

    df.dropna(subset=['high_shifted', 'low_shifted', 'open_shifted', 'volume_shifted', 'marketcap_shifted', 'prediction_5D', 'time_close', 'market_cap'], inplace=True)

    if df.empty:
        print("Error: The DataFrame is empty after dropping NaN values. Check the 'data/btc_historical_data.csv' file.")
        return

    try:
        df.to_csv('data/preprocessed_data.csv', index=False)
        print("Preprocessed data saved to 'data/preprocessed_data.csv'.")
    except Exception as e:
        print(f"Error saving preprocessed data: {e}")

    try:
        with open('data/last_date.txt', 'w') as f:
            f.write(str(last_date))
        print("Last date saved to 'data/last_date.txt'.")
    except Exception as e:
        print(f"Error saving last date: {e}")

    return df, last_date

preprocess_data()
