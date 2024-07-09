import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score

label_encoder_category = LabelEncoder()
label_encoder_sentiment = LabelEncoder()

data = pd.read_csv('./AAPL_with_articles.csv')
data = data.dropna()
data['dominant_category'] = label_encoder_category.fit_transform(data['dominant_category'].astype(str))
data['dominant_sentiment'] = label_encoder_sentiment.fit_transform(data['dominant_sentiment'].astype(str))
data['target'] = (data['close'].shift(1) > data['close']).astype(int)
#data = data.drop(index=0).reset_index(drop=True)

X = data.drop(columns=['datetime', 'target'])
y = data['target']

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

svm_model = SVC(kernel='poly', verbose=True)
svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

classification_report_output = classification_report(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

print("Classification Report:\n", classification_report_output)
print("Accuracy:", accuracy)
