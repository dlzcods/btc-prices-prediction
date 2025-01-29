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

        metrics_df = pd.read_csv('../data/evaluation_metrics.csv')
        
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

        # Display evaluation metrics
        st.header('Model Evaluation')
        mae = metrics_df.loc[metrics_df['Metric'] == 'MAE', 'Value'].values[0]

        # Create two columns
        col1, col2 = st.columns(2)

        # Explanation in the left column
        with col1:
            st.markdown("""
            <div style="text-align: justify;">
                <strong>Mean Absolute Error (MAE):</strong><br>
                The Mean Absolute Error (MAE) is a measure of the average magnitude of the errors in a set of predictions, without considering their direction. It gives you the average amount by which the predicted values deviate from the actual values. A lower MAE indicates better performance of the model.
            </div>
            """, unsafe_allow_html=True)

        # MAE value in the right column
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