from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from data.training_data import GENUINE_EXAMPLES, JUNK_EXAMPLES

# Build one training set: genuine complaints + junk/spam text
texts = GENUINE_EXAMPLES + JUNK_EXAMPLES
labels = ["genuine"] * len(GENUINE_EXAMPLES) + ["junk"] * len(JUNK_EXAMPLES)

# TF-IDF turns each sentence into a vector of word importance scores
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(texts)

# Simple, fast binary classifier: genuine vs junk
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)


def is_genuine(text: str) -> bool:
    """
    Returns True if the text looks like a real complaint, False if junk.

    Two checks run together, because the ML model alone is weak on
    this little training data (only 22 examples):

    1. Vocabulary overlap check (cheap, very reliable):
       If the submitted text shares ZERO words with anything the
       model has ever seen, its vector is all zeros (vec.nnz == 0).
       LogisticRegression can't make a real decision on an all-zero
       vector -- it just falls back to whichever class it slightly
       favors overall. That's how nonsense like "lorem ipsum dolor
       sit amet" was previously marked "genuine". Treat a total
       vocabulary mismatch as junk instead of trusting a guess.

    2. ML model (for text that DOES overlap with known vocabulary):
       Lets real complaints worded differently from the training
       examples still pass through.
    """
    vec = vectorizer.transform([text])

    if vec.nnz == 0:
        return False  # no recognizable words at all -> treat as junk

    return model.predict(vec)[0] == "genuine"
