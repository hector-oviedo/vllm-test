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
docker-compose --profile ministral up -d

# Option B: Start GPT-OSS 20B (Reasoning/CoT Model)
docker-compose --profile gpt up -d

# Option C: Start DeepSeek Distill 8B (Fast Reasoning)
docker-compose --profile deepseek up -d

# Note: All profiles automatically start the Middleware on port 8080.
# Only one inference profile can run at a time on the same GPU port (8000).
```

### Accessing the API
The Middleware Gateway ("The Universal Translator") listens on port **8080**.

*   **Endpoint:** `POST http://localhost:8080/v1/chat/completions`
*   **Health Check:** `GET http://localhost:8080/health`
*   **Authentication:** Requires a non-empty token (Local Mode).
    *   Header: `Authorization: Bearer my-secret-key`
    *   Header: `x-api-key: my-secret-key`

## Documentation
Full technical documentation is available in the `docs/` directory.
- [API Reference](docs/api_reference.html)
- [Architecture Deep Dive](docs/architecture.html)