import json

DEFAULT_MODEL= "qwer2.5:3b"

def build_prompt(text:str) -> str:
    return f""" You are a metadata extraction engin for data ingestion.

    Return ONLY valid JSON (no markdwon, no commentary).
    Schema:
    {{
        "language": "es|en|pt|fr|de|it|other",
        "keywords": ["..."],    // 3 to 12, lowercase, no duplicates, no hashtags
        "summary": "...",        // 1 sentence, <= 280 chars
        "confidence": 0.0       // 0 to 1
    }}

    
    Rules:
    - language: choose the best ISO-like short code; if uncertain use "other".
    - keywords: nouns or noun phrases, normalized, lowercase.
    - summary: concise, 1 sentence, neutral tone.
    - confidence: reflect certainty about language + extracted metadata.

    Text:
    \"\"\"{text}\"\"\""
""".strip()

def safe_json_extract(raw: str) -> dict:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start:end+1])