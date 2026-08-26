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
   JSON response back to backend


   ```

   ```
     samadhan-ai-service/
├── data/
│ ├── __init__.py
│ └── training_data.py   ← all training examples
├── models/
│ ├── __init__.py
│ ├── validation.py       ← Stage 0
│ ├── classification.py ← Stage 1 (+ shared vectorizer)
│ ├── deduplication.py  ← Stage 2
│ ├── priority.py       ← Stage 3
│ └── matching.py       ← Stage 4
├── pipeline.py         ← combines all 5 stages
├── main.py             ← FastAPI app
└── requirements.txt

   ```