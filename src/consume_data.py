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
        
        # Konversi kolom waktu
        df['time_open'] = pd.to_datetime(df['time_open']).dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Ubah volume dan marketcap menjadi float dengan format scientific
        df['volume'] = df['volume'].astype(float)
        df['market_cap'] = df['market_cap'].astype(float)

        # Simpan data ke file CSV
        df.to_csv('data/btc_historical_data.csv', mode='a', header=False, index=False)
        print("Data berhasil diambil dan disimpan.")
    else:
        print(f"Error: {response.status_code}")

# Retry mechanism
for _ in range(3):  # Retry up to 3 times
    try:
        fetch_data()
        break
    except Exception as e:
        print(f"Error occurred: {e}")
