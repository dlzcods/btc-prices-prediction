import pandas as pd

def preprocess_data():
    # Membaca dataset
    df = pd.read_csv('data/btc_historical_data.csv')
    
    # Menyimpan tanggal terakhir sebelum pelatihan
    last_date = pd.to_datetime(df['time_open'].iloc[-1])

    # Melakukan shifting pada data
    df['high_shifted'] = df['high'].shift(5)
    df['low_shifted'] = df['low'].shift(5)
    df['open_shifted'] = df['open'].shift(5)
    df['volume_shifted'] = df['volume'].shift(5)
    df['marketcap_shifted'] = df['marketcap'].shift(5)
    df['prediction_5D'] = df['close'].shift(5)
    
    # Menghapus data yang hilang setelah shifting
    df.dropna(inplace=True)

    # Menyimpan data preprocessing dan tanggal terakhir untuk digunakan nanti
    df.to_csv('data/preprocessed_data.csv', index=False)
    
    # Menyimpan tanggal terakhir untuk acuan prediksi 5 hari ke depan
    with open('src/last_date.txt', 'w') as f:
        f.write(str(last_date))

    return df, last_date

# Memanggil fungsi preprocessing
preprocess_data()
