# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 21:12:51 2023

@author: sai kumar
"""

import streamlit as st
import yfinance as yf
import plotly.express as px

# Function to fetch financial data with error handling
def fetch_financial_data(symbol, start_date, end_date):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        # Handle the error (provide default data, log the issue, or exit gracefully)
        return pd.DataFrame()

# Download stock price data
symbol = "AAPL"
data = fetch_financial_data(symbol, start_date="2023-10-01", end_date="2023-11-30")

# Plot stock price evolution using Plotly
fig = px.line(data, x=data.index, y="Close", title="Stock Price Evolution", labels={"Close": "Closing Price", "index": "Date"})
st.plotly_chart(fig)

# Print the first few rows of the data
st.write("First few rows of the data:")
st.write(data.head())
