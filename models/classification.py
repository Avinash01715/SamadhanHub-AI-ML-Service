from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from data.training_data import CLASSIFICATION_DATA

# Flatten the {category: [examples]} dict into parallel text/label lists
texts, labels = [], []
for category, examples in CLASSIFICATION_DATA.items():
    texts.extend(examples)
    labels.extend([category] * len(examples))

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# NOTE: We tested XGBoost as a drop-in replacement here and it did NOT
# help -- leave-one-out cross-validation on this exact dataset showed
# XGBoost tying (8-class task) or losing (genuine/junk task) to plain
# LogisticRegression, because there are only ~7 examples per category.
# XGBoost needs more data to earn its extra complexity, so we kept
# the simpler, equally-accurate model.
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

# Below this confidence, the model is essentially guessing.
# Calibrated loosely on this small dataset -- revisit once you have
# more training examples per category (30-50+ each is a reasonable target).
LOW_CONFIDENCE_THRESHOLD = 0.30


def classify_text(text: str) -> dict:
    """
    Classifies text into one of the 8 domains and reports how
    confident the model actually is, instead of silently forcing
    every submission into a category.

    Returns:
        {
            "category": str,          # best-guess domain
            "confidence": float,      # probability of that guess (0-1)
            "low_confidence": bool,   # True if the guess is unreliable
        }
    """
    vec = vectorizer.transform([text])
    proba = model.predict_proba(vec)[0]
    best_idx = proba.argmax()

    return {
        "category": str(model.classes_[best_idx]),
        "confidence": round(float(proba[best_idx]), 3),
        "low_confidence": bool(proba[best_idx] < LOW_CONFIDENCE_THRESHOLD),
    }
