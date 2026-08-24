import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# CyberShield AI - Model Evaluation
# ==========================================

print("===================================")
print("   CyberShield AI Model Evaluation")
print("===================================")


# ==========================================
# Load Test Dataset
# ==========================================

print("\nLoading test dataset...")

df = pd.read_csv("dataset/test_dataset.csv")

print("Test samples:", len(df))


# ==========================================
# Prepare Data
# ==========================================

X_test = df["url"]
y_test = df["label"]


# ==========================================
# Load Trained Model
# ==========================================

print("Loading trained Logistic Regression model...")

model = joblib.load(
    "model/logistic_phishing_model.pkl"
)


# ==========================================
# Load TF-IDF Vectorizer
# ==========================================

print("Loading TF-IDF vectorizer...")

vectorizer = joblib.load(
    "model/logistic_tfidf_vectorizer.pkl"
)


# ==========================================
# Convert URLs into TF-IDF Features
# ==========================================

print("\nConverting URLs into TF-IDF features...")

X_test_features = vectorizer.transform(X_test)

print("TF-IDF conversion completed.")


# ==========================================
# Generate Predictions
# ==========================================

print("Generating model predictions...")

y_pred = model.predict(X_test_features)

print("Predictions completed.")


# ==========================================
# Calculate Metrics
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


# ==========================================
# Display Performance
# ==========================================

print("\n===================================")
print("       MODEL PERFORMANCE")
print("===================================")

print(
    f"Accuracy  : {accuracy * 100:.2f}%"
)

print(
    f"Precision : {precision * 100:.2f}%"
)

print(
    f"Recall    : {recall * 100:.2f}%"
)

print(
    f"F1-Score  : {f1 * 100:.2f}%"
)


# ==========================================
# Confusion Matrix
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred
)


print("\n===================================")
print("       CONFUSION MATRIX")
print("===================================")

print(
    "                 Predicted"
)

print(
    "                 Safe  Phishing"
)

print(
    f"Actual Safe      {cm[0][0]:4d}  {cm[0][1]:8d}"
)

print(
    f"Actual Phishing  {cm[1][0]:4d}  {cm[1][1]:8d}"
)


# ==========================================
# Classification Report
# ==========================================

print("\n===================================")
print("      CLASSIFICATION REPORT")
print("===================================")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Safe",
            "Phishing"
        ],
        zero_division=0
    )
)


# ==========================================
# Completion
# ==========================================

print("===================================")
print("   Evaluation Completed Successfully")
print("===================================")