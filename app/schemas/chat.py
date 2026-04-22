from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)
    system: str | None = Field(default=None, max_length=4000)
    max_history: int = Field(default=10, ge=0, le=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    answer: str


class ChatMessagePublic(BaseModel):
    role: str
    content: str
    created_at: str


class ClearHistoryResponse(BaseModel):
    status: str = "ok"
