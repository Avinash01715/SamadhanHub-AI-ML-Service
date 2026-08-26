
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from data.training_data import GENUINE_EXAMPLES, JUNK_EXAMPLES

# 1. Combine all examples
texts = GENUINE_EXAMPLES + JUNK_EXAMPLES
labels = ["genuine"] * len(GENUINE_EXAMPLES) + ["junk"] * len(JUNK_EXAMPLES)

# 2. Convert text → numbers (TF-IDF)
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# 3. Train a simple classifier
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)


def is_genuine(text: str) -> bool:
    """
    Returns True if the text looks like a real complaint.
    
    Extra safety: if the text shares ZERO words with anything
    we have ever seen, treat it as junk (avoids random guesses).
    """
    vec = vectorizer.transform([text])

    # Safety check: completely unknown vocabulary → junk
    if vec.nnz == 0:
        return False

    return model.predict(vec)[0] == "genuine"