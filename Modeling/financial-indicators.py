from twelvedata import TDClient
import matplotlib.pyplot as plt
import datetime
import time 
import csv


companies = ['AAPL', 'AMZN', 'FB', 'GOOGL', 'MSFT']
data = object

for company in companies:

    td = TDClient(apikey="215dcdd9e46c4c6187ac843cc2573779")
    ts = td.time_series(
        symbol="AAPL",
        interval="1day",
        outputsize=3000,
        timezone="America/New_York",
    )

    data = ts.with_bbands().with_ema().with_macd().with_rsi().with_sma().with_stoch().as_json()

    csv_file = company + '.csv'

    # Get the keys from the first dictionary (to use as headers)
    headers = data[0].keys()

    # Open the file in write mode
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the header
        writer.writeheader()
        
        # Write the data
        for row in data:
            writer.writerow(row)

    time.sleep(61)

#print(data)

#dates = [datetime.datetime.strptime(record['datetime'], '%Y-%m-%d') for record in data]
#closing_prices = [float(record['close']) for record in data]

# Plotting
#plt.figure(figsize=(10, 5))
#plt.plot(dates, closing_prices, marker='o', linestyle='-', color='b')
#plt.xlabel('Date')
#plt.ylabel('Closing Price')
#plt.title('Closing Prices Over Time')
#plt.grid(True)
#plt.xticks(rotation=45)
#plt.tight_layout()

# Show the plot.
#plt.show()