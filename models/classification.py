from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from data.training_data import CLASSIFICATION_DATA

# Flatten the dictionary into two lists
texts, labels = [], []
for category, examples in CLASSIFICATION_DATA.items():
    texts.extend(examples)
    labels.extend([category] * len(examples))

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

# Confidence below this → model is basically guessing
LOW_CONFIDENCE_THRESHOLD = 0.30


def classify_text(text: str) -> dict:
    """
    Returns:
        - category
        - confidence (0 to 1)
        - low_confidence flag
    """
    vec = vectorizer.transform([text])
    probabilities = model.predict_proba(vec)[0]
    best_index = probabilities.argmax()

    return {
        "category": str(model.classes_[best_index]),
        "confidence": round(float(probabilities[best_index]), 3),
        "low_confidence": bool(probabilities[best_index] < LOW_CONFIDENCE_THRESHOLD),
    }