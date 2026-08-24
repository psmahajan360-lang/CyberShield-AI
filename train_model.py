import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load training dataset
train_data = pd.read_csv("dataset/train_dataset.csv")

print("Training dataset loaded successfully!")
print("Training samples:", len(train_data))

# Separate URLs and labels
X_train = train_data["url"].astype(str)
y_train = train_data["label"]

# Convert URLs into TF-IDF features
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    min_df=2
)

X_train_tfidf = vectorizer.fit_transform(X_train)

print("TF-IDF conversion successful!")
print("Number of training samples:", X_train_tfidf.shape[0])
print("Number of features:", X_train_tfidf.shape[1])

# Train Naive Bayes model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Save model and vectorizer
joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("\nML model training successful! ✅")
print("Model saved to: model/phishing_model.pkl")
print("Vectorizer saved to: model/tfidf_vectorizer.pkl")