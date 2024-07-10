import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import precision_score, accuracy_score
import numpy as np

data = pd.read_csv('./AAPL_with_articles.csv')
data['target'] = (data['close'].shift(1) > data['close']).astype(int)
data = data.dropna()

# Encode non numeric variables
label_encoder_category = LabelEncoder()
label_encoder_sentiment = LabelEncoder()
data['dominant_category'] = label_encoder_category.fit_transform(data['dominant_category'].astype(str))
data['dominant_sentiment'] = label_encoder_sentiment.fit_transform(data['dominant_sentiment'].astype(str))

#data = data.drop(index=0).reset_index(drop=True)

X = data.drop(columns=['datetime', 'target'])
y = data['target']

scaler = StandardScaler()
X = scaler.fit_transform(X)

accuracies = []
precisions = []

kernel = 'sigmoid'

for _ in range(100):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=None)

    svm_model = SVC(kernel=kernel, verbose=False)
    svm_model.fit(X_train, y_train)
    
    y_pred = svm_model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    
    accuracies.append(accuracy)
    precisions.append(precision)

average_accuracy = np.mean(accuracies)
average_precision = np.mean(precisions)

print("kernel : ", kernel)
print("Av. Accuracy :", average_accuracy)
print("Av. Precision :", average_precision)

