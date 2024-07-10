import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import joblib

model = load_model('stock_price_predictor_model.h5')

scaler = joblib.load('scaler.pkl')

inference_data = pd.read_csv('inference.csv')
inference_data = inference_data.iloc[::-1]
print(inference_data)

columns = ['datetime', 'open', 'high', 'low', 'volume', 'upper_band', 'middle_band', 'lower_band', 
           'ema', 'macd', 'macd_signal', 'macd_hist', 'rsi', 'sma', 'slow_k', 'slow_d', 'close']
inference_data = inference_data[columns]
inference_data = inference_data.head(60)

scaled_inference_data = scaler.transform(inference_data.drop(columns=['datetime']))

seq_length = 60 
X_inference = np.array([scaled_inference_data])

predictions = model.predict(X_inference)

predicted_closing_price_scaled = np.zeros((1, len(columns) - 1))
predicted_closing_price_scaled[:, -1] = predictions[0]
predicted_closing_price = scaler.inverse_transform(predicted_closing_price_scaled)[:, -1][0]

print(f'Predicted Closing Price: {predicted_closing_price}')