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
        
        # Konversi kolom waktu dan ubah nama kolom
        df['date'] = pd.to_datetime(df['time_open']).dt.strftime('%Y-%m-%d %H:%M:%S')
        df.drop(columns=['time_open'], inplace=True)  # Hapus kolom time_open yang lama
        
        # Ubah volume dan marketcap menjadi float
        df['volume'] = df['volume'].astype(float)
        df['market_cap'] = df['market_cap'].astype(float)

        # Baca data yang sudah ada
        try:
            existing_data = pd.read_csv('data/btc_historical_data.csv')
            existing_data['date'] = pd.to_datetime(existing_data['date'])
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=df.columns)

        # Merge data baru dengan data yang sudah ada
        combined_data = pd.concat([existing_data, df], ignore_index=True)
        
        # Urutkan data berdasarkan tanggal
        combined_data.sort_values(by='date', inplace=True)
        
        # Simpan data ke file CSV
        combined_data.to_csv('data/btc_historical_data.csv', index=False)
        print("Data berhasil diambil, dimerge, dan disimpan.")
    else:
        print(f"Error: {response.status_code}")

# Retry mechanism
for _ in range(3):  # Retry up to 3 times
    try:
        fetch_data()
        break
    except Exception as e:
        print(f"Error occurred: {e}")