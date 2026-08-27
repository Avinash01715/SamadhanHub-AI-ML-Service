from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.5
submission_history = []   # in-memory store (resets on restart)


def check_duplicate(text: str, submission_id: str):
    """
    Returns (is_duplicate: bool, original_id: str or None)
    """
    if not submission_history:
        submission_history.append({"submission_id": submission_id, "text": text})
        return False, None

    # Build a temporary corpus: all past texts + current text
    past_texts = [item["text"] for item in submission_history]
    corpus = past_texts + [text]

    # Fit a fresh vectorizer on this corpus (bigrams help catch phrases)
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus)

    new_vec = matrix[-1]
    past_vecs = matrix[:-1]

    similarities = cosine_similarity(new_vec, past_vecs)[0]
    best_idx = similarities.argmax()

    if similarities[best_idx] > SIMILARITY_THRESHOLD:
        # Still store it so future checks can see it
        submission_history.append({"submission_id": submission_id, "text": text})
        return True, submission_history[best_idx]["submission_id"]

    submission_history.append({"submission_id": submission_id, "text": text})
    return False, None