#!/usr/bin/env python3

from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
from_file = __import__('2-from_file').from_file

# Load data from file into DataFrame
df = from_file('coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv', ',')

# Remove 'Weighted_Price' column
df.drop(columns=['Weighted_Price'], inplace=True)

# Rename 'Timestamp' column to 'Date' and convert to datetime
df.rename(columns={'Timestamp': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'], unit='s')

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Fill missing values
df['Close'] = df['Close'].fillna(method='ffill')
df['High'] = df['High'].fillna(df['Close'])
df['Low'] = df['Low'].fillna(df['Close'])
df['Open'] = df['Open'].fillna(df['Close'])
df['Volume_(BTC)'] = df['Volume_(BTC)'].fillna(0)
df['Volume_(Currency)'] = df['Volume_(Currency)'].fillna(0)

# Ensure 'Date' index is in datetime format and filter from 2017 onwards
df = df[df.index >= '2017-01-01']

# Aggregate data to daily intervals
df = df.resample('D').agg({
    'High': 'max',
    'Low': 'min',
    'Open': 'mean',
    'Close': 'mean',
    'Volume_(BTC)': 'sum',
    'Volume_(Currency)': 'sum'
})

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['High'], label='High', marker='o')
plt.plot(df.index, df['Low'], label='Low', marker='o')
plt.plot(df.index, df['Open'], label='Open', marker='o')
plt.plot(df.index, df['Close'], label='Close', marker='o')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('OHLC and Volume (BTC) from 2017 onwards')
plt.legend()
plt.grid(True)
plt.show()

