import httpx
from typing import Any, Dict

"""
curl http://localhost:11434/api/chat -d '{
    "model":qwen2.5:3b

}'

"""


class OllamaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.strip("/")

    async def generate(self, model: str, prompt: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.15,
                "top_p": 1.0,
                "num_predict": 256,
            }
        }

        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            return r.json()