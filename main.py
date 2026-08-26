from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import process_submission

app = FastAPI(title="SamadhanHub AI/ML Service")


class SubmissionInput(BaseModel):
    submission_id: str
    text: str


@app.get("/")
def health_check():
    return {"status": "AI/ML service is running"}


@app.post("/process")
def process(submission: SubmissionInput):
    return process_submission(submission.submission_id, submission.text)
