import sys


from fastapi import FastAPI, HTTPException

sys.path.insert(0, "src")

from rag_service import ask_question
from app.schemas import AskRequest, AskResponse, HealthResponse


app = FastAPI(
    title="WayPoint RAG API",
    description="Visa Dispute & Chargeback Policy RAG API",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "healthy"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        return ask_question(request.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAG processing failed: {str(e)}",
        )