import pandas as pd

# Load CyberShield AI dataset
file_path = "dataset/cybershield_dataset.csv"

df = pd.read_csv(file_path)

# Verified legitimate URLs
legitimate_urls = [
    "https://google.com",
    "https://www.google.com",
    "https://microsoft.com",
    "https://www.microsoft.com",
    "https://github.com",
    "https://www.github.com",
    "https://amazon.com",
    "https://www.amazon.com"
]

# Create legitimate records
new_data = pd.DataFrame({
    "url": legitimate_urls,
    "label": [0] * len(legitimate_urls)
})

# Add only URLs that don't already exist
existing_urls = set(df["url"].astype(str))

new_data = new_data[
    ~new_data["url"].isin(existing_urls)
]

# Add to dataset
df = pd.concat([df, new_data], ignore_index=True)

# Save updated dataset
df.to_csv(file_path, index=False)

print("Legitimate URLs added successfully!")
print("Added URLs:", len(new_data))
print("Total URLs:", len(df))

print("\nAdded URLs:")
print(new_data.to_string(index=False))