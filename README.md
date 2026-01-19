# MIAA Inference Engine
### Modularity, Isolation, Abstraction, Agnostic

**Author:** Hector Oviedo  
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
*   NVIDIA GPU (CUDA 12+) OR AMD GPU (ROCm 6+)

### Quick Start
```bash
# Clone the repository
git clone <repo_url>

# Start MIAA on NVIDIA GPU (CUDA)
docker-compose --profile cuda up -d

# OR Start MIAA on AMD GPU (ROCm)
docker-compose --profile rocm up -d
```

## Documentation
Full technical documentation is available in the `docs/` directory.
- [API Reference](docs/api_reference.html)
- [Architecture Deep Dive](docs/architecture.html)

---
© 2026 Hector Oviedo. All Rights Reserved.
