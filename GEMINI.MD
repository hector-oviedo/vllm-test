# 🧠 GEMINI MEMORY & ORCHESTRATION LOG

## 📊 Project Status
**Phase:** Phase 5: The Interface (Agnostic Layer)
**Current Task:** Implementing MCP Host for Tooling.
**Health:** Green - MCP Host Integrated

## 🗺️ Master Plan
- [x] **Phase 1: Architecture & Knowledge Integration**
    - [x] Analyze Context Files (MIAA & Unified Protocol).
    - [x] Define Directory Structure (Capsules, Middleware, Isolation Runtimes).
    - [x] Initialize `README.md` and Documentation.
- [x] **Phase 2: The Foundation (Isolation Layer)**
    - [x] Setup Hardware-Agnostic Docker Compose (CUDA vs ROCm profiles).
    - [x] Implement Abstract Runtime Interface (gRPC/REST).
    - [x] **Refinement:** Remove vendor lock-in (OpenAI Key Bypass) & Update ROCm to v7+.
- [x] **Phase 3: The Middleware (Abstraction Layer)**
    - [x] **Step 1:** Define Unified Schemas (Pydantic models for Protocol).
    - [x] **Step 2:** Implement Auth Middleware (Bearer/API Key).
    - [x] **Step 3:** Build FastAPI Gateway logic (Routing & Normalization).
    - [x] **Step 4:** Containerize Middleware & Fix Compose Dependencies.
- [x] **Phase 4: The Intelligence (Modularity Layer)**
    - [x] **Step 1:** Implement Capsule Manifest Schema (`capsule.py`).
    - [x] **Step 2:** Define Base Capsules (`ministral`, `gpt-oss`, `deepseek`).
    - [x] **Step 3:** Update Docker Compose with Profiles for each model.
    - [x] **Step 4:** **Fix:** Correct Ministral ID and add HF_TOKEN support.
    - [x] **Step 5:** **Fix:** Enable `bitsandbytes` quantization for 14B/20B models to fit in 24GB VRAM.
    - [x] **Step 6:** **Refinement:** Switch Ministral to AWQ (`cyankiwi/...`) to resolve architecture and availability issues.
    - [x] **Step 7:** **Fix:** Set `--quantization compressed-tensors` to match AWQ model config.
    - [x] **Step 8:** **Fix:** Remove explicit quantization for `gpt-oss-20b` (Native `mxfp4` detected).
    - [x] **Step 9:** **Testing:** Verified `ministral-cuda`, `gpt-cuda`, `deepseek-cuda` profiles.
- [ ] **Phase 5: The Interface (Agnostic Layer)**
    - [x] **Step 1:** Install `mcp` SDK in Middleware.
    - [x] **Step 2:** Implement MCP Client/Host logic in FastAPI.
    - [ ] **Step 3:** Configure a sample MCP Server (e.g., Filesystem or Web Search) for testing.
    - [ ] **Step 4:** Add OpenLLMetry Observability.
- [ ] **Phase 6: Documentation & Finalization**
    - [ ] Generate `openapi.json`.
    - [ ] Generate `llm.txt` (Standardized Agent Discovery file).
    - [ ] Generate `MIAA_ARCH.md` (Explaining the isolation/modularity).
    - [ ] Generate Static HTML Docs (Bootstrap).

## 📝 Activity Log
| Timestamp | Action | Result/Outcome |
|-----------|--------|----------------|
| 2026-01-19 | Git Config | Set user to Hector Oviedo |
| 2026-01-19 | Directory Setup | Created MIAA folders: isolation, middleware, capsules, interface |
| 2026-01-19 | Memory Init | Initialized GEMINI.MD |
| 2026-01-19 | Isolation Setup | Created Dockerfiles for CUDA/ROCm and docker-compose.yml with profiles |
| 2026-01-19 | Refinement | Removed author name/copyright from README, updated ROCm req to 7+, set VLLM_API_KEY="EMPTY" |
| 2026-01-19 | Phase Start | Began Phase 3 (Middleware) |
| 2026-01-19 | Middleware Code | Implemented schemas.py, auth.py, main.py (FastAPI), and requirements.txt |
| 2026-01-19 | Compose Fix | Removed invalid `depends_on` from docker-compose.yml |
| 2026-01-19 | Docs Update | Updated README with Middleware Access info |
| 2026-01-19 | Modularity | Configured 3 Capsules: Ministral 3 14B, GPT-OSS 20B, DeepSeek Distill 8B |
| 2026-01-19 | Compose Update | Created `ministral`, `gpt`, `deepseek` docker profiles for isolated testing |
| 2026-01-19 | Fix Auth/ID | Updated Ministral ID to `...2512-BF16` and added `HF_TOKEN` to compose |
| 2026-01-19 | Fix OOM | Added `--quantization bitsandbytes` to Ministral and GPT-OSS profiles |
| 2026-01-19 | Fix Arch | Switched Ministral to AWQ (`MaziyarPanahi/...`) as vLLM bitsandbytes fails on Pixtral |
| 2026-01-19 | Fix 404 | Updated AWQ ID to `cyankiwi/Ministral-3-14B-Instruct-2512-AWQ-4bit` (Verified Repo) |
| 2026-01-19 | Fix Config | Updated quantization flag to `compressed-tensors` to match model metadata |
| 2026-01-19 | Fix GPT-OSS | Removed manual quantization flags to allow native `mxfp4` loading |
| 2026-01-19 | Verified | Confirmed all 3 model profiles are operational |
| 2026-01-19 | Phase Start | Began Phase 5 (MCP Interface) |
| 2026-01-19 | MCP Host | Implemented `mcp_client.py` and integrated into `main.py` |

## 💡 Architectural Decision Records (ADR)
- **Decision:** Docker Profiles for Models -> **Reason:** Enables "Cold Swapping" of distinct base models (different encoders) while keeping the Middleware layer constant. Fits MIAA "Isolation" by abstracting the model choice into the runtime config.
- **Decision:** GPT-OSS 20B as CoT -> **Reason:** Designated as the primary "Thinking" model for testing reasoning capabilities.
- **Decision:** Pass HF_TOKEN -> **Reason:** Required for gated models (Ministral 3). Token is passed via env var to maintain security and allow CI/CD integration.
- **Decision:** On-the-fly Quantization -> **Reason:** 14B+ models in BF16 exceed 24GB VRAM. Using `bitsandbytes` (4-bit) allows them to run locally without downloading separate quantized weights, maintaining "Base Model" purity in definitions.
- **Decision:** Pre-Quantized AWQ for Pixtral -> **Reason:** `bitsandbytes` dynamic quantization is not yet supported for Pixtral (Ministral 3) architecture in vLLM. Switching to verified AWQ weights ensures stability.
- **Decision:** Compressed-Tensors Flag -> **Reason:** The specific AWQ model uses `compressed-tensors` format metadata, requiring explicit flag matching in vLLM.
- **Decision:** Native MXFP4 for GPT-OSS -> **Reason:** The model is already quantized in a specific format (`mxfp4`), so generic flags like `bitsandbytes` cause conflicts.
- **Decision:** Use official MCP SDK -> **Reason:** Ensures full compliance with the Agnostic Interface pillar, allowing the middleware to act as a "Host" for any standard MCP server.
- **Decision:** Tool Injection -> **Reason:** Middleware automatically queries connected MCP servers and injects their tools into the OpenAI-compatible `tools` parameter, making tools available to any model transparently.