import requests
import pandas as pd
from datetime import datetime
import pytz

def get_exchange_rate(crypto, timestamp):
    url = f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={crypto}&tsym=INR&toTs={timestamp}&limit=1"
    response = requests.get(url)
    data = response.json()
    return data['Data']['Data'][0]['close']

cryptocurrencies = ['XRP', 'BNB', 'USDT', 'BTC', 'LTC', 'ETH', 'ADA']

data = []

# Prompt user for the desired date
date = input("Enter the desired date (YYYY-MM-DD): ")

# Get the datetime object for 4:00 AM IST on the given date
ist = pytz.timezone('Asia/Kolkata')
desired_datetime = datetime.strptime(f"{date} 04:00:00", '%Y-%m-%d %H:%M:%S').replace(tzinfo=ist)

# Convert the IST datetime to UTC
utc_datetime = desired_datetime.astimezone(pytz.utc)

# Get the timestamp for the UTC datetime
timestamp = int(utc_datetime.timestamp())

for crypto in cryptocurrencies:
    exchange_rate = get_exchange_rate(crypto, timestamp)
    data.append({'Cryptocurrency': crypto, 'Exchange Rate (INR)': exchange_rate})

df = pd.DataFrame(data)

# Save data to an Excel file with the provided date
filename = f'cryptocurrency_data_{date}.xlsx'
df.to_excel(filename, index=False)
