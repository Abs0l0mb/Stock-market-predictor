import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.svm import SVC

data = pd.read_csv('./AAPL.csv')
data['target'] = (data['close'].shift(1) > data['close']).astype(int)
data = data.drop(index=0).reset_index(drop=True)

#print(data)

X = data.drop(columns=['datetime', 'target'])
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

classification_report_output = classification_report(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

print("Classification Report:\n", classification_report_output)
print("Accuracy:", accuracy)
