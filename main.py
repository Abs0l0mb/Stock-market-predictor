from twelvedata import TDClient

td = TDClient(apikey="215dcdd9e46c4c6187ac843cc2573779")
ts = td.time_series(
    symbol="AAPL, AMZN",
    interval="1day",
    outputsize=365,
    timezone="America/New_York",
)

content = ts.with_bbands(ma_type="EMA").with_plus_di().with_wma(time_period=20).with_wma(time_period=40).as_json()

print(content)
