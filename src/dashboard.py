import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Fungsi untuk menambahkan logo di Streamlit
def add_logo():
    logo = "https://upload.wikimedia.org/wikipedia/commons/a/a5/Bitcoin_logo_2019.svg"  # URL logo BTC
    st.image(logo, width=100)

def app():
    # Mengambil data prediksi
    predictions_df = pd.read_csv('src/predictions.csv')
    
    # Menambahkan logo BTC di bagian atas
    add_logo()

    # Menampilkan judul dashboard
    st.title('Bitcoin Price Prediction')

    # Menampilkan dataframe sebagai tabel
    st.write(predictions_df)

    # Menampilkan kalender untuk memilih rentang tanggal
    st.sidebar.header("Filter Date Range")
    start_date = st.sidebar.date_input("Start Date", datetime(2024, 10, 19))
    end_date = st.sidebar.date_input("End Date", datetime(2024, 10, 24))

    # Memfilter data berdasarkan tanggal
    predictions_df['Date'] = pd.to_datetime(predictions_df['Date'])
    filtered_df = predictions_df[(predictions_df['Date'] >= pd.to_datetime(start_date)) & (predictions_df['Date'] <= pd.to_datetime(end_date))]

    # Menampilkan grafik
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot grafik harga aktual (dummy data, ganti sesuai kebutuhan Anda)
    ax.plot(filtered_df['Date'], filtered_df['Predicted (XGBoost)'], label='Predicted Price', color='orange', marker='o')
    
    # Plot grafik harga aktual (pastikan data harga aktual ada di dataframe)
    # Gantilah ini dengan data aktual Anda
    ax.plot(filtered_df['Date'], filtered_df['Predicted (XGBoost)'] * 1.05, label='Actual Price', color='blue', marker='x')  # Dummy actual data

    # Menambahkan label dan judul
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.set_title('Bitcoin Price Prediction vs Actual')

    # Format tanggal agar lebih mudah dibaca
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_tick_params(rotation=45)

    # Menambahkan legenda
    ax.legend()

    # Menampilkan grafik ke Streamlit
    st.pyplot(fig)

if __name__ == '__main__':
    app()
