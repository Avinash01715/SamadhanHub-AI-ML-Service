from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline import process_submission

app = FastAPI(title="SamadhanHub AI/ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubmissionInput(BaseModel):
    submission_id: str
    text: str

@app.get("/")
def health_check():
    return {"status": "AI/ML service is running", "version": "2.0"}

@app.post("/process")
def process(submission: SubmissionInput):
    return process_submission(submission.submission_id, submission.text)