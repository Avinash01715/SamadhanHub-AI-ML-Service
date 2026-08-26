"""
OPTIONAL upgrade to deduplication.py -- not wired into the pipeline
by default. Swap this in once submission volume is too large for
TF-IDF to refit on every request.

WHY THIS IS BETTER AT SCALE:
TF-IDF only matches exact/similar WORDS. Sentence embeddings (from
sentence-transformers) capture MEANING, so "the pipe is leaking" and
"water is spilling from the pipeline" can be recognized as the same
issue even with almost no shared vocabulary -- something TF-IDF
cannot do.

WHY IT'S SEPARATE FROM deduplication.py:
It requires downloading a pretrained model (~80MB) the first time it
runs, which needs internet access to huggingface.co. That could not
be tested in this sandboxed environment, so review this file before
trusting it -- it has not been run end-to-end like the other files.

Install: pip install sentence-transformers
"""

from sentence_transformers import SentenceTransformer, util

SIMILARITY_THRESHOLD = 0.6  # embeddings tend to score "somewhat related"
                            # text higher than TF-IDF does -- re-tune this
                            # against your own real submissions before trusting it

# Small, fast, general-purpose embedding model (downloaded once, then cached)
_model = SentenceTransformer("all-MiniLM-L6-v2")

# Store both the raw text and its precomputed embedding, so we don't
# re-embed the entire history on every single new submission
submission_history = []  # [{"submission_id": ..., "text": ..., "embedding": ...}]


def check_duplicate(text: str, submission_id: str):
    new_embedding = _model.encode(text, convert_to_tensor=True)

    for past in submission_history:
        similarity = util.cos_sim(new_embedding, past["embedding"]).item()
        if similarity > SIMILARITY_THRESHOLD:
            submission_history.append({
                "submission_id": submission_id,
                "text": text,
                "embedding": new_embedding,
            })
            return True, past["submission_id"]

    submission_history.append({
        "submission_id": submission_id,
        "text": text,
        "embedding": new_embedding,
    })
    return False, None
