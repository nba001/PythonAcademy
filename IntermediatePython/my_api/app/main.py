from fastapi import FastAPI, HTTPException
import json
from pydantic import ValidationError

from app.schemas import MetadataRequest, MetadataResponse
from app.ollama_client import OllamaClient
from app.prompt_service import build_prompt, safe_json_extract, DEFAULT_MODEL


app = FastAPI(title="LLM Metadata Service", version="1.0.0")

@app.get("/health")
def health():
    return {"status": 'ok'}


@app.post("/extract-metadata", response_model=MetadataResponse)
async def extract_metadata(req: MetadataRequest) -> MetadataResponse:
    ollama_url = app.state.ollama_url
    model_name = app.state.model_name

    client = OllamaClient(ollama_url)
    prompt = build_prompt(req.text)

    try: 
        result = await client.generate(model=model_name, prompt=prompt)
        response_text = result.get("response", "")
        data = safe_json_extract(response_text)

        validated = MetadataResponse(
            id = req.id
            language= data['language']
            keyword= data['language']
            summary= data['language']
            model= model_name
            confidence= float(data.get("confidence", 0.5))
        )

        return validated
    except (json.JSONDecodeError, KeyError, ValidationError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid model output: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.on_event("startup")
async def startup():
    import os
    app.state.ollama_url = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
    app.state.model_name = os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)

# POST /extract-metadata
#input {id, text}
# output {id, language, keywords, summary/intent, confidence}

#Script
# - reads sample record (text)
# - calls API
# - writes enriched file (enriched.json)