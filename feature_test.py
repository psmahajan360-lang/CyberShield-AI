import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
data = pd.read_csv("dataset/phishing_dataset.csv")

# Separate URLs and labels
urls = data["url"]
labels = data["label"]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 5)
)

# Convert URLs into numerical features
X = vectorizer.fit_transform(urls)

print("TF-IDF conversion successful!")
print("Number of URLs:", X.shape[0])
print("Number of Features:", X.shape[1])