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
        
        # Load combined predicted data (both training and future predictions)
        predictions_df = pd.read_csv('../data/combined_predictions.csv')
        predictions_df['Date'] = pd.to_datetime(predictions_df['Date'])
        
        # Add logo in the sidebar
        add_logo()

        # Display the title of the dashboard
        st.title('Bitcoin Price Prediction Dashboard')

        # Display date range picker in the sidebar
        st.sidebar.header("Filter Date Range")
        start_date = st.sidebar.date_input("Start Date", datetime(2025, 1, 1))
        end_date = st.sidebar.date_input("End Date", datetime(2025, 2, 1))

        # Filter data based on date
        historical_df = historical_df[(historical_df['Date'] >= pd.to_datetime(start_date)) & (historical_df['Date'] <= pd.to_datetime(end_date))]
        predictions_df = predictions_df[(predictions_df['Date'] >= pd.to_datetime(start_date)) & (predictions_df['Date'] <= pd.to_datetime(end_date))]

        # Sort the predictions DataFrame by Date
        predictions_df = predictions_df.sort_values(by='Date')

        # Separate training and future predictions
        training_predictions = predictions_df[predictions_df['Type'] == 'Training']
        future_predictions = predictions_df[predictions_df['Type'] == 'Future']

        # Combine training and future predictions into a single DataFrame
        combined_predictions = pd.concat([training_predictions, future_predictions], ignore_index=True)

        # Create Plotly figure
        fig = go.Figure()

        # Trace 1: Actual Prices
        fig.add_trace(go.Scatter(
            x=historical_df['Date'],
            y=historical_df['close'],
            mode='lines',
            name='Actual Price',
            line=dict(color='blue')
        ))

        # Trace 2: Combined Predictions with Color Transition
        fig.add_trace(go.Scatter(
            x=combined_predictions['Date'],
            y=combined_predictions['Predicted_Price'],
            mode='lines',
            name='Predicted Price',
            line=dict(
                color='green',  # Default color for training predictions
                dash='solid'
            )
        ))

        # Add color transition for future predictions
        if not future_predictions.empty:
            fig.add_trace(go.Scatter(
                x=future_predictions['Date'],
                y=future_predictions['Predicted_Price'],
                mode='lines',
                name='Future Predictions',
                line=dict(
                    color='red',  # Color for future predictions
                    dash='solid'
                )
            ))

        # Update layout with desired date format
        fig.update_layout(
            title='Bitcoin Price Prediction vs Actual',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='closest',
            xaxis=dict(
                tickformat='%b %d',  # Date format: Jan 25, Feb 1, Mar 4
                tickangle=-45,       # Tilt date labels to avoid overlap
                showgrid=True        # Show grid on x-axis
            )
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    app()