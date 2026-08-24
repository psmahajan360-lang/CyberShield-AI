import pandas as pd
from sklearn.model_selection import train_test_split

# Load prepared dataset
data = pd.read_csv("dataset/cybershield_dataset.csv")

print("Dataset loaded successfully!")
print("Total URLs:", len(data))

# Split dataset into training and testing sets
train_data, test_data = train_test_split(
    data,
    test_size=0.20,
    random_state=42,
    stratify=data["label"]
)

# Save training and testing datasets
train_data.to_csv("dataset/train_dataset.csv", index=False)
test_data.to_csv("dataset/test_dataset.csv", index=False)

print("\nDataset split successful!")
print("Training URLs:", len(train_data))
print("Testing URLs:", len(test_data))

print("\nTraining Label Distribution:")
print(train_data["label"].value_counts())

print("\nTesting Label Distribution:")
print(test_data["label"].value_counts())

print("\nFiles created successfully:")
print("dataset/train_dataset.csv")
print("dataset/test_dataset.csv")