import pandas as pd

# Load dataset
data = pd.read_csv("dataset/phishing_dataset.csv")

# Display first 5 rows
print("First 5 rows:")
print(data.head())

print("\n----------------------------")

# Display dataset information
print("Dataset Shape:", data.shape)

print("\n----------------------------")

# Display column names
print("Columns:")
print(data.columns)

print("\n----------------------------")

# Count Safe and Phishing URLs
print("Label Distribution:")
print(data["label"].value_counts())