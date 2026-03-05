# Add the correct path for the file! 
# Update app.py to enforce: text min length = 20 # App with Validation

import re
from typing import Tuple
from collections import Counter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="Module 1 - Session 1 API", version="1.0.0")


# -----------------------------
# Schemas (Pydantic models)
# -----------------------------

class KeywordsRequest(BaseModel):
    text: str
    top_k: int = 5


class KeywordsResponse(BaseModel):
    keywords: list[str]


class NormalizeTextRequest(BaseModel):
    # Contract-level constraint: reject short inputs early
    text: str = Field(..., min_length=20)
    lowercase: bool = False


class NormalizeTextResponse(BaseModel):
    normalized_text: str
    char_count: int
    word_count: int


# -----------------------------
# Services (business logic)
# -----------------------------

def extract_keywords_simple(text: str, top_k: int) -> list[str]:
    text = re.sub(r"[^\w\s]","",text).lower()
    words = text.split()
    words_count = Counter(words)
    words_tuple = words_count.most_common(top_k)

    return [i for i,j in words_tuple]


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_text(text: str, lowercase: bool = False) -> Tuple[str, int, int]:
    """Deterministic text normalization."""
    if lowercase:
        text = text.lower()

    normalized = _collapse_whitespace(text)
    char_count = len(normalized)
    word_count = 0 if not normalized else len(normalized.split(" "))
    return normalized, char_count, word_count


# -----------------------------
# Routes (API boundary)
# -----------------------------

@app.post("/normalize-text",tags=["strings"], response_model=NormalizeTextResponse)
def post_normalize_text(payload: NormalizeTextRequest) -> NormalizeTextResponse:
    normalized, char_count, word_count = normalize_text(
        text = payload.text,
        lowercase = payload.lowercase,
    )
    return NormalizeTextResponse(
        normalized_text = normalized,
        char_count = char_count,
        word_count = word_count,
    )

@app.post("/keywords-simple", tags=["strings"], response_model=KeywordsResponse)
def post_keywords_simple(payload: KeywordsRequest):
    if payload.top_k < 1 or payload.top_k >20:
        raise HTTPException(status_code=400, detail="top_k should be between 1 and 20.")

    top_k_list = extract_keywords_simple(
        text = payload.text,
        top_k = payload.top_k
    )

    return KeywordsResponse(
        keywords = top_k_list
    )
