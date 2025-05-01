import requests
import pandas as pd
from datetime import datetime

def fetch_data():
    url = "https://api.coinpaprika.com/v1/coins/btc-bitcoin/ohlcv/latest"
    params = {
        'quote': 'usd',
        'interval': '1h'
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        df['date'] = pd.to_datetime(df['time_open']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df.drop(columns=['time_open'], inplace=True)

        df['volume'] = df['volume'].astype(float)
        df['market_cap'] = df['market_cap'].astype(float)

        df['marketcap'] = df['market_cap']
        df.drop(columns=['market_cap'], inplace=True)
        df.drop(columns=['time_close'], inplace=True)

        try:
            existing_data = pd.read_csv('data/btc_historical_data.csv')
            existing_data['date'] = pd.to_datetime(existing_data['date'])  # Convert to datetime
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=df.columns)

        df['date'] = pd.to_datetime(df['date'])

        new_data = df[~df['date'].isin(existing_data['date'])]

        if not new_data.empty:
            print(f"New dates added: {new_data['date'].unique().tolist()}")

            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            combined_data.sort_values(by='date', inplace=True)
            combined_data.drop(columns=['market_cap'], inplace=True)
            combined_data.drop(columns=['time_close'], inplace=True)
            
            combined_data.to_csv('data/btc_historical_data.csv', index=False)
            print("Data successfully fetched, merged, and saved.")
        else:
            print("No new data to add. All data is already in the CSV file.")
    else:
        print(f"Error: {response.status_code}")

# Retry mechanism
for _ in range(3):
    try:
        fetch_data()
        break
    except Exception as e:
        print(f"Error occurred: {e}")
