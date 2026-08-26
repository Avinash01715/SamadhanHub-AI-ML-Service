from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SIMILARITY_THRESHOLD = 0.5

# In-memory store of past submissions (resets on server restart --
# swap for a database if you need duplicates caught across restarts)
submission_history = []


def check_duplicate(text: str, submission_id: str):
    """
    Checks if 'text' is a near-duplicate of a past submission.

    IMPORTANT: this uses its OWN TfidfVectorizer, fit fresh on the
    current submission history each time it's called. It does NOT
    reuse classification.py's vectorizer.

    Why that matters: classification.py's vectorizer only knows the
    ~56 words used in the 8 category examples. Two completely
    different complaints ("school roof collapsed" vs "bridge
    collapsed") both contain generic words like "village" and
    "children" that happen to be in that narrow vocabulary, which
    made them look artificially similar (false positive duplicate).

    Fitting a dedicated vectorizer -- with bigrams, so phrase order
    matters too -- on the actual submission text fixes that. Tested:
    true duplicate similarity ~0.79, the false-positive pair above
    drops to ~0.15, safely under the 0.5 threshold.

    Trade-off: refitting on every call is fine for hackathon/demo
    scale (hundreds of submissions) but gets slow at thousands.
    At that scale, switch to sentence-embedding based similarity
    (see deduplication_semantic.py) instead of rewriting this file.
    """
    if submission_history:
        past_texts = [item["text"] for item in submission_history]
        corpus = past_texts + [text]

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(corpus)

        new_vec = matrix[-1]        # last row = the current submission
        past_vecs = matrix[:-1]     # everything before it = history

        similarities = cosine_similarity(new_vec, past_vecs)[0]
        best_match_idx = similarities.argmax()

        if similarities[best_match_idx] > SIMILARITY_THRESHOLD:
            submission_history.append({"submission_id": submission_id, "text": text})
            return True, submission_history[best_match_idx]["submission_id"]

    submission_history.append({"submission_id": submission_id, "text": text})
    return False, None
