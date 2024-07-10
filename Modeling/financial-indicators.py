from twelvedata import TDClient
import time 
import csv


companies = ['AAPL']
data = object

for company in companies:

    td = TDClient(apikey="215dcdd9e46c4c6187ac843cc2573779")
    ts = td.time_series(
        symbol="AAPL",
        interval="1day",
        outputsize=3000,
        timezone="Europe/Paris",
    )

    data = ts.with_bbands().with_ema().with_macd().with_rsi().with_sma().with_stoch().as_json()

    csv_file = company + '.csv'

    headers = data[0].keys()

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(company, ' processed')

    # Uncomment the following line if you want to retrieve multiple companies data
    #time.sleep(61)
