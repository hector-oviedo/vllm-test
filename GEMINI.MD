# 🧠 GEMINI MEMORY & ORCHESTRATION LOG

## 📊 Project Status
**Phase:** Phase 6: Documentation & Finalization
**Current Task:** Final Delivery.
**Health:** Green - Ready for Production

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
- [x] **Phase 5: The Interface (Agnostic Layer)**
    - [x] **Step 1:** Install `mcp` SDK in Middleware.
    - [x] **Step 2:** Implement MCP Client/Host logic in FastAPI.
    - [x] **Step 3:** Add Native Web Search Tool.
    - [x] **Step 4:** Integrate Tools into API response.
- [x] **Phase 6: Documentation & Finalization**
    - [x] Generate `openapi.json` (Automated via Docker).
    - [x] Generate `llm.txt`.
    - [x] Generate Static HTML Docs (Bootstrap).

## 📝 Activity Log
| Timestamp | Action | Result/Outcome |
|-----------|--------|----------------|
| 2026-01-19 | Git Config | Set user to Hector Oviedo |
| 2026-01-19 | Directory Setup | Created MIAA folders: isolation, middleware, capsules, interface |
| 2026-01-19 | Phase 2-4 | Completed Isolation, Middleware, Modularity layers |
| 2026-01-19 | Verified | Confirmed all 3 model profiles (Ministral, GPT-OSS, DeepSeek) work |
| 2026-01-19 | Phase 5 | Implemented MCP Host and Native Tools |
| 2026-01-19 | Documentation | Created HTML Docs and Automated OpenAPI Generator |
| 2026-01-19 | Maintenance | Fixed Docker networking and silenced variable warnings |

## 💡 Architectural Decision Records (ADR)
- **Decision:** Docker Profiles for Models -> **Reason:** Enables "Cold Swapping" of distinct base models (different encoders) while keeping the Middleware layer constant. Fits MIAA "Isolation" by abstracting the model choice into the runtime config.
- **Decision:** Native MXFP4 for GPT-OSS -> **Reason:** The model is already quantized in a specific format (`mxfp4`), so generic flags like `bitsandbytes` cause conflicts.
- **Decision:** Tool Injection -> **Reason:** Middleware automatically queries connected MCP servers and injects their tools into the OpenAI-compatible `tools` parameter, making tools available to any model transparently.
- **Decision:** Tool Control -> **Reason:** Respects standard `tool_choice` parameter. If `tool_choice="none"`, tools are stripped to save tokens. Default is "auto".
- **Decision:** Docs Automation -> **Reason:** Created a `docs` profile in docker-compose to run a script that generates `openapi.json` from the living code, ensuring docs never drift from implementation.
