import pandas as pd
import os

def preprocess_data():
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('src', exist_ok=True)

    # Load the dataset
    try:
        df = pd.read_csv('data/btc_historical_data.csv')
    except FileNotFoundError:
        print("Error: The file 'data/btc_historical_data.csv' does not exist.")
        return

    # Ensure the DataFrame is not empty
    if df.empty:
        print("Error: The DataFrame is empty. Check the 'data/btc_historical_data.csv' file.")
        return

    # Ensure required columns exist
    required_columns = ['date', 'high', 'low', 'open', 'volume', 'marketcap', 'close']
    if not all(column in df.columns for column in required_columns):
        print(f"Error: Missing required columns in the DataFrame. Required columns: {required_columns}")
        return

    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Save the last date
    last_date = df['date'].iloc[-1]

    # Perform shifting on the data
    df['high_shifted'] = df['high'].shift(5)
    df['low_shifted'] = df['low'].shift(5)
    df['open_shifted'] = df['open'].shift(5)
    df['volume_shifted'] = df['volume'].shift(5)
    df['marketcap_shifted'] = df['marketcap'].shift(5)
    df['prediction_5D'] = df['close'].shift(5)

    # Drop rows with NaN values only in the specified subset of columns
    df.dropna(subset=['high_shifted', 'low_shifted', 'open_shifted', 'volume_shifted', 'marketcap_shifted', 'prediction_5D'], inplace=True)

    # Ensure the DataFrame is not empty after dropping NaN values
    if df.empty:
        print("Error: The DataFrame is empty after dropping NaN values. Check the 'data/btc_historical_data.csv' file.")
        return

    # Save the preprocessed data
    try:
        df.to_csv('data/preprocessed_data.csv', index=False)
        print("Preprocessed data saved to 'data/preprocessed_data.csv'.")
    except Exception as e:
        print(f"Error saving preprocessed data: {e}")

    # Save the last date to a text file
    try:
        with open('data/last_date.txt', 'w') as f:
            f.write(str(last_date))
        print("Last date saved to 'data/last_date.txt'.")
    except Exception as e:
        print(f"Error saving last date: {e}")

    return df, last_date

# Call the preprocessing function
preprocess_data()