import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model
import joblib

# Load the saved model
model = load_model('stock_price_predictor_model.h5')

# Load the saved scaler
scaler = joblib.load('scaler.pkl')

# Load the inference data
inference_data = pd.read_csv('inference.csv')
inference_data = inference_data.iloc[::-1]
print(inference_data)

# Ensure the columns are in the correct order
columns = ['datetime', 'open', 'high', 'low', 'volume', 'upper_band', 'middle_band', 'lower_band', 
           'ema', 'macd', 'macd_signal', 'macd_hist', 'rsi', 'sma', 'slow_k', 'slow_d', 'close']
inference_data = inference_data[columns]
inference_data = inference_data.head(60)

# Drop datetime column and scale the data
scaled_inference_data = scaler.transform(inference_data.drop(columns=['datetime']))

# Prepare the input sequence
seq_length = 60  # The sequence length used during training
X_inference = np.array([scaled_inference_data])  # Wrap in a list to create a batch with a single sequence

# Perform inference
predictions = model.predict(X_inference)

# Inverse transform the prediction to get the actual closing price
predicted_closing_price_scaled = np.zeros((1, len(columns) - 1))
predicted_closing_price_scaled[:, -1] = predictions[0]
predicted_closing_price = scaler.inverse_transform(predicted_closing_price_scaled)[:, -1][0]

# Output the predicted closing price for the next day
print(f'Predicted Closing Price: {predicted_closing_price}')