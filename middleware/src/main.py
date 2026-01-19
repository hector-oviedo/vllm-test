import os
import json
import httpx
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from .schemas import ChatCompletionRequest
from .auth import get_api_key
from .mcp_client import McpHost
from .native_tools import WEB_SEARCH_TOOL

app = FastAPI(title="MIAA Unified Inference API", version="1.0.0")

# Configuration
INFERENCE_URL = os.getenv("INFERENCE_URL", "http://inference:8000/v1")
TIMEOUT = 600.0 # Extended timeout for reasoning models
MCP_COMMAND = os.getenv("MCP_SERVER_COMMAND")
MCP_ARGS = json.loads(os.getenv("MCP_SERVER_ARGS", "[]"))

client = httpx.AsyncClient(timeout=TIMEOUT)
mcp_host = None

@app.on_event("startup")
async def startup_event():
    global mcp_host
    print(f"MIAA Middleware initialized. Upstream: {INFERENCE_URL}")
    
    if MCP_COMMAND:
        print(f"🚀 Initializing MCP Host with: {MCP_COMMAND} {MCP_ARGS}")
        mcp_host = McpHost(MCP_COMMAND, MCP_ARGS, os.environ.copy())
        await mcp_host.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()
    if mcp_host:
        await mcp_host.disconnect()

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
    - Injects MCP Tools (Agnostic Layer).
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

    # 1.5 MCP Tool Injection (Agnostic Layer)
    # Check if client explicitly disabled tools via tool_choice="none"
    client_tool_choice = payload.get("tool_choice")
    
    if client_tool_choice != "none":
        current_tools = payload.get("tools", [])
        
        # Add Native Web Search
        current_tools.append(WEB_SEARCH_TOOL)
        
        # Add MCP Tools if available
        if mcp_host:
            mcp_tools = await mcp_host.list_tools()
            if mcp_tools:
                current_tools.extend(mcp_tools)
        
        if current_tools:
            payload["tools"] = current_tools
            # Default to 'auto' if not specified
            if not client_tool_choice:
                payload["tool_choice"] = "auto"
    else:
        # If tool_choice is explicitly "none", ensure no tools are sent to save tokens/confusion
        payload.pop("tools", None)

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
        # Try to read error body
        try:
            error_detail = await r.read()
            print(f"Upstream Error: {error_detail}")
        except: 
            pass
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
    mcp_status = "disabled"
    if mcp_host:
        mcp_status = "connected" if mcp_host.session else "error"
    return {"status": "healthy", "layer": "middleware", "mcp": mcp_status}
