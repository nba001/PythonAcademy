from pydantic import BaseModel, Field
from typing import List

class MetadataRequest(BaseModel):
    id: str
    text: str = Field(min_length=1)

class MetadataResponse(BaseModel):
    id: str
    language: str = Field(description="'English', 'Spanish', 'Tamil'")
    keyword: List[str] = Field(min_length=3, max_length=12)
    summary: str = Field(min_length=10, max_length=280)
    model: str
    confidence: float = Field(ge=0.0, le=1.0)