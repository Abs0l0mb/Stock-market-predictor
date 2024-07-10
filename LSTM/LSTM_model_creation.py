import math
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def add_target_column(data):
    data['target'] = (data['close'].shift(-1) < data['close']).astype(int)
    return data[:-1]

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length, -1])  # Assuming the label is the last column
    return np.array(X), np.array(y)

data = pd.read_csv('./AAPL.csv')

columns = ['datetime', 'open', 'high', 'low', 'volume', 'upper_band', 'middle_band', 'lower_band', 
           'ema', 'macd', 'macd_signal', 'macd_hist', 'rsi', 'sma', 'slow_k', 'slow_d', 'close']
data = data[columns]
data = add_target_column(data)
print(data)
data = data.iloc[::-1]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(data.drop(columns=['datetime', 'target']))
joblib.dump(scaler, 'scaler.pkl')

seq_length = 60
X, y = create_sequences(np.hstack((scaled_data, data[['target']].values)), seq_length)

split = int(0.8 * len(X))
X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]

model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))  # Sigmoid activation for binary classification

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

model.save('stock_price_predictor_classification_model.h5')

predictions = model.predict(X_val).flatten()

strong_confidence_indices = np.where((predictions <= 0.4) | (predictions >= 0.6))[0]
filtered_predictions = predictions[strong_confidence_indices]
filtered_y_val = y_val[strong_confidence_indices]

binary_predictions = (filtered_predictions > 0.5).astype(int)

accuracy = accuracy_score(filtered_y_val, binary_predictions)
#precision = precision_score(filtered_y_val, binary_predictions)

print(f'Number of confident predictions : {len(filtered_predictions)}')
print(f'Accuracy (with confidence filtering): {accuracy}')
#print(f'Precision (with confidence filtering): {precision}')