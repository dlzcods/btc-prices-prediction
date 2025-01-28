import pandas as pd

def preprocess_data():
    df = pd.read_csv('data/btc_historical_data.csv')

    # Mengonversi format tanggal menjadi datetime
    df['time_open'] = pd.to_datetime(df['time_open'])

    # Menambahkan kolom shifted untuk prediksi 5 hari ke depan
    df['Prediction_5D'] = df['close'].shift(-5)
    df['high_shifted'] = df['high'].shift(5)
    df['low_shifted'] = df['low'].shift(5)
    df['open_shifted'] = df['open'].shift(5)
    df['volume_shifted'] = df['volume'].shift(5)
    df['marketcap_shifted'] = df['marketcap'].shift(5)

    # Menghapus data yang missing
    df.dropna(inplace=True)

    df.to_csv('data/btc_historical_data.csv', index=False)

preprocess_data()
