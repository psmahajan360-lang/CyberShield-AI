import pandas as pd

# Load original PhiUSIIL dataset
input_file = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(input_file)

# Keep only the columns required by CyberShield AI
clean_df = df[["URL", "label"]].copy()

# Rename URL column
clean_df.rename(columns={"URL": "url"}, inplace=True)

# Convert labels to CyberShield AI format
# Original PhiUSIIL:
# 1 = Legitimate
# 0 = Phishing
#
# CyberShield AI:
# 0 = Safe
# 1 = Phishing

clean_df["label"] = 1 - clean_df["label"]

# Remove missing URLs
clean_df.dropna(subset=["url"], inplace=True)

# Save cleaned dataset
output_file = "dataset/cybershield_dataset.csv"
clean_df.to_csv(output_file, index=False)

print("Dataset preparation successful!")
print("Total URLs:", len(clean_df))
print("\nLabel Distribution:")
print(clean_df["label"].value_counts())
print("\nSaved to:", output_file)