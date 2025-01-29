import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objs as go
from datetime import datetime

def add_logo():
    logo_url = "./btc logo/image.png"  # URL logo BTC
    st.sidebar.image(logo_url, width=50)

def app():
    try:
        # Load historical data
        historical_df = pd.read_csv('../data/btc_historical_data.csv')
        historical_df['Date'] = pd.to_datetime(historical_df['date'])
        
        # Load predicted data
        predictions_df = pd.read_csv('predictions.csv')
        predictions_df['Date'] = pd.to_datetime(predictions_df['Date'])
        
        # Merge historical and predicted data based on date
        merged_df = pd.merge(historical_df, predictions_df, on='Date', how='outer', suffixes=('_actual', '_predicted'))
        
        # Add logo in the sidebar
        add_logo()

        # Display the title of the dashboard
        st.title('Bitcoin Price Prediction Dashboard')

        # Display date range picker in the sidebar
        st.sidebar.header("Filter Date Range")
        start_date = st.sidebar.date_input("Start Date", datetime(2025, 1, 1))
        end_date = st.sidebar.date_input("End Date", datetime(2025, 2, 1))

        # Filter data based on date
        filtered_df = merged_df[(merged_df['Date'] >= pd.to_datetime(start_date)) & (merged_df['Date'] <= pd.to_datetime(end_date))]

        # Split data into actual and predicted
        actual_data = filtered_df[filtered_df['close'].notna()]
        predicted_data = filtered_df[filtered_df['Predicted_Price'].notna()]

        # Create Plotly figure
        fig = go.Figure()

        # Trace 1: Actual Prices
        trace1 = go.Scatter(
            x=actual_data['Date'],
            y=actual_data['close'],
            mode='lines',
            name='Actual Price',
            line=dict(color='blue')
        )

        # Trace 2: Predicted Prices
        trace2 = go.Scatter(
            x=predicted_data['Date'],
            y=predicted_data['Predicted_Price'],
            mode='lines',
            name='Predicted Price',
            line=dict(color='orange')
        )

        # Add traces to the figure
        fig.add_trace(trace1)
        fig.add_trace(trace2)

        # Jika data aktual dan prediksi tidak bertemu, tambahkan garis putus-putus
        if not actual_data.empty and not predicted_data.empty:
            last_actual_point = actual_data.iloc[-1]  # Titik terakhir data aktual
            first_predicted_point = predicted_data.iloc[0]  # Titik pertama data prediksi

            # Jika tanggal tidak sama, tambahkan garis putus-putus
            if last_actual_point['Date'] != first_predicted_point['Date']:
                fig.add_trace(go.Scatter(
                    x=[last_actual_point['Date'], first_predicted_point['Date']],
                    y=[last_actual_point['close'], first_predicted_point['Predicted_Price']],
                    mode='lines',
                    line=dict(dash='dash', color='black'),
                    name='Connection',
                    showlegend=False
                ))

        # Update layout dengan format tanggal yang diinginkan
        fig.update_layout(
            title='Bitcoin Price Prediction vs Actual',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='closest',
            xaxis=dict(
                tickformat='%b %d',  # Format tanggal: Jan 25, Feb 1, Mar 4
                tickangle=-45,       # Miringkan label tanggal agar tidak bertumpuk
                showgrid=True        # Tampilkan grid pada sumbu x
            )
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    app()