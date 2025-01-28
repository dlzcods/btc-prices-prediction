import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

def train_model():
    # Membaca dataset yang telah diproses
    df = pd.read_csv('data/preprocessed_data.csv')

    # Memilih fitur dan target
    X = df[['high_shifted', 'low_shifted', 'open_shifted', 'volume_shifted', 'marketcap_shifted']]
    y = df['Prediction_5D']

    # Membagi data menjadi train dan test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalisasi data
    scaler_X = MinMaxScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)

    scaler_y = MinMaxScaler()
    y_train_scaled = scaler_y.fit_transform(y_train.values.reshape(-1, 1))
    y_test_scaled = scaler_y.transform(y_test.values.reshape(-1, 1))

    # Hyperparameter tuning menggunakan GridSearchCV
    param_grid = {
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [100, 200, 300],
        'subsample': [0.8, 1.0]
    }

    model = xgb.XGBRegressor()

    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
    grid_search.fit(X_train_scaled, y_train_scaled)

    # Menampilkan parameter terbaik
    best_params = grid_search.best_params_
    print(f'Best Parameters: {best_params}')

    # Melatih model dengan parameter terbaik
    best_model = xgb.XGBRegressor(**best_params)
    best_model.fit(X_train_scaled, y_train_scaled)

    # Melakukan prediksi
    y_pred_scaled = best_model.predict(X_test_scaled)

    # Menghitung MSE dan MAE
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1))
    best_mse = mean_squared_error(y_test, y_pred)
    best_mae = mean_absolute_error(y_test, y_pred)

    print(f'Mean Squared Error: {best_mse}')
    print(f'Mean Absolute Error: {best_mae}')

    # Menyimpan model yang sudah dilatih
    best_model.save_model('src/model.pkl')

# Memanggil fungsi pelatihan model
train_model()
