import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load datasets
train_data = pd.read_csv("dataset/train_dataset.csv")
test_data = pd.read_csv("dataset/test_dataset.csv")

print("Datasets loaded successfully!")
print("Training samples:", len(train_data))
print("Testing samples:", len(test_data))

# Separate URLs and labels
X_train = train_data["url"].astype(str)
y_train = train_data["label"]

X_test = test_data["url"].astype(str)
y_test = test_data["label"]

# TF-IDF
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    min_df=2
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

print("TF-IDF conversion successful!")
print("Number of features:", X_train_tfidf.shape[1])

# Train Logistic Regression
model = LogisticRegression(
    max_iter=1000,
    solver="liblinear"
)

model.fit(X_train_tfidf, y_train)

# Save Logistic Regression model and TF-IDF vectorizer
joblib.dump(model, "model/logistic_phishing_model.pkl")
joblib.dump(vectorizer, "model/logistic_tfidf_vectorizer.pkl")

print("Logistic Regression training successful!")
print("Logistic Regression model saved successfully!")

# Predict
y_pred = model.predict(X_test_tfidf)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)

print("\nCyberShield AI - Logistic Regression")
print("------------------------------------")
print("Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Safe", "Phishing"]
))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))