import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Load the data from the uploaded file
file_path = 'C:/Users/Colli/Documents/myvenvs/grayscale_unlocks/data/raw/LTCN722.xlsx'
ltcn_data = pd.read_excel(file_path)

# Calculate the difference in shares outstanding to find the amount of shares subscribed
ltcn_data['Shares Subscribed'] = ltcn_data['Shares Outstanding'].diff(periods=-1).fillna(0).abs()

# Add a column to calculate the unlock date which is 6 months after the subscription date
ltcn_data['Date'] = pd.to_datetime(ltcn_data['Date'])
ltcn_data['Unlock Date'] = ltcn_data['Date'] + pd.DateOffset(months=6)

# Reverse the dataframe to maintain the chronological order of shares subscription
ltcn_data = ltcn_data.iloc[::-1]

# Pull daily OHLC data for LTCN from Yahoo Finance
ltcn_ohlc = yf.download('LTCN', start=ltcn_data['Date'].min(), end=pd.Timestamp.today())

# Reset index to have the date as a column
ltcn_ohlc.reset_index(inplace=True)

# Rename columns to match the expected format
ltcn_ohlc.rename(columns={'Date': 'OHLC Date'}, inplace=True)

# Merge the OHLC data with the existing DataFrame
ltcn_data = pd.merge(ltcn_data, ltcn_ohlc, left_on='Date', right_on='OHLC Date', how='left')

# Drop the OHLC Date column as it's redundant after the merge
ltcn_data.drop(columns=['OHLC Date'], inplace=True)

# Display the updated DataFrame
print(ltcn_data.head())

# Group the data by unlock date and sum the shares subscribed for each unlock date
unlock_data = ltcn_data.groupby('Unlock Date')['Shares Subscribed'].sum().reset_index()

# Plot the unlock data
plt.figure(figsize=(10, 6))
plt.bar(unlock_data['Unlock Date'], unlock_data['Shares Subscribed'], color='blue')
plt.xlabel('Unlock Date')
plt.ylabel('Shares Unlocked')
plt.title('LTCN Shares Unlock Schedule')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
