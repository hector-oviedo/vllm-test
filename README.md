# MIAA Inference Engine
### Modularity, Isolation, Abstraction, Agnostic

**Status:** Production / Active Development

## Executive Summary
The MIAA Inference Engine is a production-grade, high-performance API system designed for the composable AI era. It abandons the monolithic architecture of legacy inference servers in favor of a strictly decoupled framework that separates Intelligence (Modularity), Execution (Isolation), Logic (Abstraction), and Interfaces (Agnostic).

This system provides a "Universal Interface" compatible with modern reasoning workflows, agentic tool use (MCP), and dynamic model composition, ensuring that infrastructure remains robust while intelligence becomes fluid.

## Architecture

### 1. Modularity (The Intelligence Layer)
*   **Dynamic Capsules:** Models are treated as interchangeable components.
*   **Hot-Swappable Adapters:** Runtime injection of Low-Rank Adapters (LoRA) for task-specific capabilities without service interruption.

### 2. Isolation (The Execution Layer)
*   **Hardware Agnosticism:** The runtime environment is strictly isolated via containerization, abstracting the underlying silicon (CUDA/ROCm) from the application logic.
*   **Resilience:** Fault domains are contained; a model failure does not crash the gateway.

### 3. Abstraction (The Middleware Layer)
*   **Universal Gateway:** A unified API surface that normalizes requests, handles embedding adaptation, and manages context windows transparently.
*   **Protocol Normalization:** Translates disparate model inputs/outputs into a standardized schema.

### 4. Agnostic (The Interface Layer)
*   **Model Context Protocol (MCP):** Native client support for standardized tool connectivity.
*   **Open Observability:** Vendor-neutral telemetry via OpenTelemetry standards.

## Deployment

### Prerequisites
*   Docker & Docker Compose
*   NVIDIA GPU (CUDA 12+) OR AMD GPU (ROCm 7+)

### Configuration
Some models (like Ministral 3) are gated and require a Hugging Face token.
1.  Create a `.env` file in the root directory:
    ```bash
    cp .env.example .env
    ```
2.  Edit `.env` and add your token:
    ```
    HF_TOKEN=hf_your_token_here
    ```

### Quick Start
```bash
# Clone the repository
git clone <repo_url>

# Option A: Start Ministral 3 14B (Default Edge Model)
# Uses 4-bit AWQ Quantization (cyankiwi/Ministral-3-14B-Instruct-2512-AWQ-4bit)
# Fits in 24GB VRAM.
docker-compose --profile ministral up -d

# Option B: Start GPT-OSS 20B (Reasoning/CoT Model)
# Uses Native MXFP4 Quantization (openai/gpt-oss-20b)
# Fits in 24GB VRAM.
docker-compose --profile gpt up -d

# Option C: Start DeepSeek Distill 8B (Fast Reasoning)
# Runs in native BF16/FP16 (TeichAI/Qwen3-8B-DeepSeek-v3.2-Speciale-Distill)
# Fits in 24GB VRAM.
docker-compose --profile deepseek up -d

# Note: All profiles automatically start the Middleware on port 8080.
# Only one inference profile can run at a time on the same GPU port (8000).
```

### Usage Guide & Expectations

The MIAA Engine exposes a standardized API on port **8080**.

#### 1. Authentication
All requests require a valid API token. In local mode, you can use any non-empty string.
*   Header: `Authorization: Bearer my-secret-key` OR `x-api-key: my-secret-key`

#### 2. Chat Completions (Standard)
**Endpoint:** `POST http://localhost:8080/v1/chat/completions`

**Request:**
```json
{
  "model": "ministral-3-14b-instruct",
  "messages": [
    {"role": "user", "content": "What is the capital of France?"}
  ],
  "stream": true
}
```

#### 3. Using Tools (Agentic Workflow)
By default, the middleware injects available tools (like `web_search`) into your request.
1.  **Request:** Send a standard chat prompt (e.g., "Search for MIAA architecture").
2.  **Response:** The model will return a `finish_reason: tool_calls` response with the tool name and arguments.
3.  **Execution:** You (the client) must execute the tool. You can use our helper endpoint:
    *   **Endpoint:** `POST http://localhost:8080/v1/tools/execute`
    *   **Body:** `{"name": "web_search", "arguments": {"query": "MIAA architecture"}}`
4.  **Loop:** Feed the tool output back to the model as a `tool` role message.

To **disable** tools, send `"tool_choice": "none"` in your request.

#### 4. Model Capabilities
*   **Ministral 3 14B (Profile: `ministral`):** Best for general instruction following, coding, and tool use. Supports 32k context.
*   **GPT-OSS 20B (Profile: `gpt`):** Optimized for complex reasoning and Chain-of-Thought (CoT). Slower but deeper.
*   **DeepSeek Distill 8B (Profile: `deepseek`):** Fast, efficient reasoning model. Great for high-throughput tasks.

## Documentation
Full technical documentation is available in the `docs/` directory.
- [API Reference](https://hector-oviedo.github.io/vllm-test/index.html)
- [Architecture Deep Dive](https://hector-oviedo.github.io/vllm-test/architecture.html)
