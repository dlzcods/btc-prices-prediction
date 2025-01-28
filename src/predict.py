import pandas as pd
import xgboost as xgb
from datetime import timedelta

def predict():
    # Membaca data yang telah diproses
    df = pd.read_csv('data/preprocessed_data.csv')

    # Load model
    model = xgb.XGBRegressor()
    model.load_model('src/model.pkl')

    # Load scaler
    scaler_X = joblib.load('src/scaler_X.pkl')
    scaler_y = joblib.load('src/scaler_y.pkl')

    # Membaca tanggal terakhir yang disimpan sebelumnya
    with open('src/last_date.txt', 'r') as f:
        last_date = pd.to_datetime(f.read().strip())

    # Mengambil 5 data terakhir untuk prediksi
    last_features = df[['high_shifted', 'low_shifted', 'open_shifted', 'volume_shifted', 'marketcap_shifted']].iloc[-5:]
    last_features_scaled = scaler_X.transform(last_features)

    # Melakukan prediksi
    pred_xgb_scaled = model.predict(last_features_scaled)
    pred_xgb = scaler_y.inverse_transform(pred_xgb_scaled.reshape(-1, 1))

    # Menghitung tanggal prediksi (5 hari ke depan)
    predicted_dates = [last_date + timedelta(days=i) for i in range(1, 6)]

    predictions_df = pd.DataFrame({
        'Date': predicted_dates,
        'Predicted (XGBoost)': pred_xgb.flatten()
    })

    # Menyimpan hasil prediksi
    predictions_df.to_csv('src/predictions.csv', index=False)

predict()
