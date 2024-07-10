import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, precision_score
import matplotlib.pyplot as plt


label_encoder_category = LabelEncoder()
label_encoder_sentiment = LabelEncoder()

data = pd.read_csv('./AAPL_with_articles.csv')
data['target'] = (data['close'].shift(1) > data['close']).astype(int)
data = data.dropna()

data['dominant_category'] = label_encoder_category.fit_transform(data['dominant_category'].astype(str))
data['dominant_sentiment'] = label_encoder_sentiment.fit_transform(data['dominant_sentiment'].astype(str))
#data = data.drop(index=0).reset_index(drop=True)

X = data.drop(columns=['datetime', 'target'])
y = data['target']


precision_scores = []
accuracy_scores = []
classification_reports = []

for i in range(0, 100):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    rf_model = RandomForestClassifier(n_estimators=180, random_state=42)
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)

    classification_reports.append(classification_report(y_test, y_pred, output_dict=True))
    accuracy_scores.append(accuracy_score(y_test, y_pred))
    precision_scores.append(precision_score(y_test, y_pred))

total_precision = np.mean(precision_scores)
total_accuracy = np.mean(accuracy_scores)

print("Av. precision : ", total_precision)
print("Av. accuracy : ", total_accuracy)