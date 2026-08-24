import os
import json
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# ==========================================
# CyberShield AI - Model Visualization
# ==========================================

print("===================================")
print(" CyberShield AI Model Visualization")
print("===================================")

# ==========================================
# Create Required Folders
# ==========================================

os.makedirs("screenshots", exist_ok=True)
os.makedirs("model", exist_ok=True)

# ==========================================
# Load Test Dataset
# ==========================================

print("\nLoading test dataset...")

df = pd.read_csv("dataset/test_dataset.csv")

X_test = df["url"]
y_test = df["label"]

print("Test samples:", len(df))

# ==========================================
# Load Logistic Regression Model
# ==========================================

print("Loading Logistic Regression model...")

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
# TF-IDF Conversion
# ==========================================

print("\nConverting URLs to TF-IDF features...")

X_test_features = vectorizer.transform(X_test)

# ==========================================
# Generate Predictions
# ==========================================

print("Generating predictions...")

y_pred = model.predict(X_test_features)

# ==========================================
# Calculate Model Metrics
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
# Calculate Confusion Matrix
# ==========================================

cm = confusion_matrix(
    y_test,
    y_pred
)

# ==========================================
# Print Model Performance
# ==========================================

print("\n===================================")
print("       MODEL PERFORMANCE")
print("===================================")

print(f"Accuracy  : {accuracy * 100:.2f}%")
print(f"Precision : {precision * 100:.2f}%")
print(f"Recall    : {recall * 100:.2f}%")
print(f"F1-Score  : {f1 * 100:.2f}%")

print("\nConfusion Matrix:")
print(cm)

# ==========================================
# Save Metrics for Web Application
# ==========================================

metrics_data = {
    "accuracy": round(accuracy * 100, 2),
    "precision": round(precision * 100, 2),
    "recall": round(recall * 100, 2),
    "f1_score": round(f1 * 100, 2)
}

with open(
    "model/model_metrics.json",
    "w"
) as file:

    json.dump(
        metrics_data,
        file,
        indent=4
    )

print("\nModel metrics saved successfully!")
print("Saved to: model/model_metrics.json")

# ==========================================
# Model Performance Chart
# ==========================================

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1-Score"
]

values = [
    accuracy * 100,
    precision * 100,
    recall * 100,
    f1 * 100
]

plt.figure(figsize=(8, 5))

bars = plt.bar(
    metrics,
    values
)

plt.title(
    "CyberShield AI - Model Performance"
)

plt.ylabel(
    "Score (%)"
)

plt.ylim(
    0,
    105
)

# Add percentage values above bars

for bar, value in zip(
    bars,
    values
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "screenshots/model_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\nModel performance chart saved successfully!"
)

# ==========================================
# Confusion Matrix Visualization
# ==========================================

plt.figure(figsize=(7, 5))

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    "CyberShield AI - Confusion Matrix"
)

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "Actual Label"
)

plt.xticks(
    [0, 1],
    ["Safe", "Phishing"]
)

plt.yticks(
    [0, 1],
    ["Safe", "Phishing"]
)

# Add confusion matrix values

for i in range(cm.shape[0]):

    for j in range(cm.shape[1]):

        plt.text(
            j,
            i,
            str(cm[i, j]),
            ha="center",
            va="center"
        )

plt.colorbar()

plt.tight_layout()

plt.savefig(
    "screenshots/confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Confusion matrix saved successfully!"
)

# ==========================================
# Completion
# ==========================================

print("\n===================================")
print(" Visualization Completed Successfully")
print("===================================")

print("\nGenerated files:")

print("1. screenshots/model_performance.png")
print("2. screenshots/confusion_matrix.png")
print("3. model/model_metrics.json")

print("\n===================================")