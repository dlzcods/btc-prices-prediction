import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objs as go
from datetime import datetime

def add_logo():
    logo_url = "src/btc_logo/image.png"  # URL logo BTC
    st.sidebar.image(logo_url, width=50)

def app():
    try:
        historical_df = pd.read_csv('./data/btc_historical_data.csv')
        historical_df['Date'] = pd.to_datetime(historical_df['date'])
        
        predictions_df = pd.read_csv('./data/combined_predictions.csv')
        predictions_df['Date'] = pd.to_datetime(predictions_df['Date'])

        metrics_df = pd.read_csv('./data/evaluation_metrics.csv')
        
        add_logo()
        st.title('Bitcoin Price Prediction Dashboard')

        st.sidebar.header("Filter Date Range")
        latest_date = predictions_df['Date'].max().date()
        start_date = st.sidebar.date_input("Start Date", datetime(2025, 1, 1))
        end_date = st.sidebar.date_input("End Date", latest_date)

        historical_df = historical_df[(historical_df['Date'] >= pd.to_datetime(start_date)) & (historical_df['Date'] <= pd.to_datetime(end_date))]
        predictions_df = predictions_df[(predictions_df['Date'] >= pd.to_datetime(start_date)) & (predictions_df['Date'] <= pd.to_datetime(end_date))]

        predictions_df = predictions_df.sort_values(by='Date')

        training_predictions = predictions_df[predictions_df['Type'] == 'Training']
        future_predictions = predictions_df[predictions_df['Type'] == 'Future']

        # Combine training and future predictions into a single DataFrame
        combined_predictions = pd.concat([training_predictions, future_predictions], ignore_index=True)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=historical_df['Date'],
            y=historical_df['close'],
            mode='lines',
            name='Actual Price',
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
            x=combined_predictions['Date'],
            y=combined_predictions['Predicted_Price'],
            mode='lines',
            name='Predicted Price',
            line=dict(
                color='green', 
                dash='solid'
            )
        ))

        if not future_predictions.empty:
            fig.add_trace(go.Scatter(
                x=future_predictions['Date'],
                y=future_predictions['Predicted_Price'],
                mode='lines',
                name='Future Predictions',
                line=dict(
                    color='red',  
                    dash='solid'
                )
            ))

        fig.update_layout(
            title='Bitcoin Price Prediction vs Actual',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='closest',
            xaxis=dict(
                tickformat='%b %d',  # Date format: Jan 25, Feb 1, Mar 4
                tickangle=-45,       
                showgrid=True      
            )
        )

        st.plotly_chart(fig)

        st.header('Model Evaluation')
        mae = metrics_df.loc[metrics_df['Metric'] == 'MAE', 'Value'].values[0]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="text-align: justify;">
                <strong>Mean Absolute Error (MAE):</strong><br>
                The Mean Absolute Error (MAE) is a measure of the average magnitude of the errors in a set of predictions, without considering their direction. It gives you the average amount by which the predicted values deviate from the actual values. A lower MAE indicates better performance of the model.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; font-weight: bold; margin: auto; height: 100px; display: ; align-items: center; justify-content: center;">
                Mean Absolute Error (MAE) 
                <div style= "font-size: 35px;">
                    ${mae:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(' ')
        st.caption('Copyright (c) Muhammad Abdiel Al Hafiz 2025')

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    app()