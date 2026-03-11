import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset (DO NOT MODIFY COLUMNS)
df = pd.read_csv("TestingHistory.csv")

# Extract columns by position
sites = df.iloc[:, 0]          # URL column
time_spent = df.iloc[:, -1]    # Time spent column

# Rule-based labels (training labels)
def label_site(url):
    url = str(url).lower()
    if any(x in url for x in ["youtube", "instagram", "facebook", "twitter", "netflix"]):
        return "distracting"
    return "productive"

labels = sites.apply(label_site)

# Train ML model
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(sites)

model = LogisticRegression()
model.fit(X_vec, labels)

# Save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved successfully!")
