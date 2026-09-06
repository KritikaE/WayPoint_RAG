from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class Source(BaseModel):
    condition: str
    title: str
    pages: str


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class HealthResponse(BaseModel):
    status: str