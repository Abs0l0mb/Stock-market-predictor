import math
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Create target column
def add_target_column(data):
    data['target'] = (data['close'].shift(-1) < data['close']).astype(int)
    # Drop the last row as it will have a NaN target value
    return data[:-1]

# Prepare input sequences
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length, -1])  # Assuming the target is the last column
    return np.array(X), np.array(y)

# Load the data
data = pd.read_csv('./AAPL.csv')

# Ensure the correct column order and add the target column
columns = ['datetime', 'open', 'high', 'low', 'volume', 'upper_band', 'middle_band', 'lower_band', 
           'ema', 'macd', 'macd_signal', 'macd_hist', 'rsi', 'sma', 'slow_k', 'slow_d', 'close']
data = data[columns]
data = add_target_column(data)
print(data)
# Reverse the DataFrame so the most recent data is at the bottom
data = data.iloc[::-1]

# Drop datetime column and scale the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(data.drop(columns=['datetime', 'target']))
joblib.dump(scaler, 'scaler.pkl')

# Prepare input sequences
seq_length = 60
X, y = create_sequences(np.hstack((scaled_data, data[['target']].values)), seq_length)

# Split into training and validation sets
split = int(0.8 * len(X))
X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]

# Build the LSTM model
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))  # Sigmoid activation for binary classification

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

# Save the model
model.save('stock_price_predictor_classification_model.h5')

# Predicting the direction
predictions = model.predict(X_val).flatten()

# Filter predictions: only consider those with strong confidence
strong_confidence_indices = np.where((predictions <= 0.4) | (predictions >= 0.6))[0]
filtered_predictions = predictions[strong_confidence_indices]
filtered_y_val = y_val[strong_confidence_indices]

# Convert predictions to binary: 0 for predictions <= 0.4, 1 for predictions >= 0.6
binary_predictions = (filtered_predictions > 0.5).astype(int)

# Calculate accuracy and precision
accuracy = accuracy_score(filtered_y_val, binary_predictions)
#precision = precision_score(filtered_y_val, binary_predictions)

print(f'Number of confident predictions : {len(filtered_predictions)}')
print(f'Accuracy (with confidence filtering): {accuracy}')
#print(f'Precision (with confidence filtering): {precision}')