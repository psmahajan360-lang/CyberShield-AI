import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load test dataset
test_data = pd.read_csv("dataset/test_dataset.csv")

# Load trained model and TF-IDF vectorizer
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

print("Test dataset loaded successfully!")
print("Testing samples:", len(test_data))

# Prepare test data
X_test = test_data["url"].astype(str)
y_test = test_data["label"]

# Convert test URLs using the SAME vectorizer
X_test_tfidf = vectorizer.transform(X_test)

print("Test URLs converted to TF-IDF features!")

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nCyberShield AI Model Evaluation")
print("--------------------------------")
print("Accuracy:", accuracy)

# Classification report
print("\nClassification Report:")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Safe", "Phishing"]
))

# Confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))