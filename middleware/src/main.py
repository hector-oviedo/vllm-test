import os
import json
import httpx
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from .schemas import ChatCompletionRequest
from .auth import get_api_key

app = FastAPI(title="MIAA Unified Inference API", version="1.0.0")

# Configuration
INFERENCE_URL = os.getenv("INFERENCE_URL", "http://inference:8000/v1")
TIMEOUT = 600.0 # Extended timeout for reasoning models

client = httpx.AsyncClient(timeout=TIMEOUT)

@app.on_event("startup")
async def startup_event():
    print(f"MIAA Middleware initialized. Upstream: {INFERENCE_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()

async def stream_generator(response):
    """
    Protocol 4.2: Streaming Response (SSE).
    Forwards the upstream stream to the client.
    """
    async for chunk in response.aiter_bytes():
        yield chunk

@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Unified Endpoint: POST /v1/chat/completions
    - Normalizes input (via Pydantic schema).
    - Routes to isolated inference engine.
    - Handles Streaming.
    """
    
    # 1. Input Normalization (Handled by Pydantic)
    # Convert back to dict for upstream forwarding
    payload = request.model_dump(exclude_none=True)

    # Handle Top-Level System (Protocol 3.1.1)
    if request.system:
        # Prepend system message if it exists as top-level
        system_msg = {"role": "system", "content": request.system}
        payload["messages"].insert(0, system_msg)
        # Remove top-level system from payload sent to OpenAI-compatible upstream
        payload.pop("system", None)

    # 2. Engine Dispatch
    upstream_url = f"{INFERENCE_URL}/chat/completions"
    
    # Forward Auth Headers (or use internal key if needed)
    headers = {
        "Authorization": f"Bearer {os.getenv('UPSTREAM_KEY', 'EMPTY')}",
        "Content-Type": "application/json"
    }

    try:
        req = client.build_request("POST", upstream_url, json=payload, headers=headers)
        r = await client.send(req, stream=True)
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Inference Engine unavailable (Isolation Layer unreachable)")

    if r.status_code != 200:
        await r.aclose()
        raise HTTPException(status_code=r.status_code, detail="Upstream error")

    # 3. Response Protocol
    if request.stream:
        return StreamingResponse(
            stream_generator(r),
            media_type="text/event-stream"
        )
    else:
        # For non-streaming, read the whole response
        content = await r.read()
        await r.aclose()
        return JSONResponse(content=json.loads(content))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "layer": "middleware"}
