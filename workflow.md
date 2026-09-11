```

Submission arrives (text + ID from backend)
        │
        ▼
┌─────────────────┐
│ STAGE 0          │  Genuine or junk?
│ VALIDATION       │  ── If junk → STOP, return "invalid"
└────────┬─────────┘
         │ valid
         ▼
┌─────────────────┐
│ STAGE 1          │  Which of 8 domains?
│ CLASSIFICATION   │  (water, education, healthcare, agriculture,
└────────┬─────────┘   urban_infra, sanitation, environment, accessibility)
         │
         ▼
┌─────────────────┐
│ STAGE 2          │  Compare against past submissions
│ DEDUPLICATION    │  (cosine similarity > threshold = duplicate)
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ STAGE 3          │  Keyword-based urgency check
│ PRIORITY         │  HIGH / MEDIUM
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ STAGE 4          │  Category → Department lookup
│ UNIVERSITY MATCH │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ STAGE 5          │  Turns classification confidence + priority + text
│ SCORING          │  into 3 numbers: domain_match_score, urgency_score,
└────────┬─────────┘  feasibility_score (see pipeline.py: _calculate_scores)
         │
         ▼
   JSON response back to backend


   ```

   ```
     samadhan-ai-service/
├── data/
│ ├── __init__.py
│ └── training_data.py    ← all training examples
├── models/
│ ├── __init__.py
│ ├── validation.py       ← Stage 0
│ ├── classification.py   ← Stage 1 (+ shared vectorizer)
│ ├── deduplication.py    ← Stage 2
│ ├── priority.py         ← Stage 3
│ └── matching.py         ← Stage 4
├── pipeline.py           ← combines all 5 stages + scoring (Stage 5)
├── main.py               ← FastAPI app (real backend entrypoint)
├── streamlit_app.py      ← standalone demo UI, calls pipeline.py directly
└── requirements.txt

   ```

## A note on model quality

Both classifiers here (`validation.py` and `classification.py`) are trained on
synthetic, template-generated text (see the docstring at the top of
`data/training_data.py`). Reported numbers: classification ~86.9% 5-fold CV
accuracy (n=320); genuine-vs-junk validation 100% 5-fold CV accuracy (n=640).

The 100% number is misleading — template-generated junk and genuine text
share almost no vocabulary, which makes that split artificially easy.
Adversarial testing found short-but-real complaints (e.g. "the bridge has
some issue, not sure how serious") get misclassified as junk, because the
model learned "short/vague = junk" from the templates rather than a rule
that holds for real citizens. Treat the classification number as the more
trustworthy one, and treat both as a hackathon-scale starting point rather
than a production-grade benchmark.