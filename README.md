# ⚡ AgentFlow Studio

> **Principal AI-Native Solution Architecture**: Multi-Agent ReAct Orchestration (Planner, Executor, Critic), Model Context Protocol (MCP) Tool Registry, In-Memory Mathematical Vector RAG (Exact Cosine Similarity), and Real-Time Server-Sent Events (SSE) Telemetry.

[![Node.js LTS](https://img.shields.io/badge/Node.js-LTS_v20+-339933?logo=node.js)](https://nodejs.org)
[![TypeScript Strict](https://img.shields.io/badge/TypeScript-Strict_Mode-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![License Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Zero Dummy Code](https://img.shields.io/badge/Implementation-100%25_Real_Math_%26_Code-emerald)](#)

---

## 🏛️ System Architecture

AgentFlow Studio eliminates hallucination cascades through decoupled reasoning, standardized MCP tool invocation, mathematical vector retrieval, and low-overhead server-sent event streaming.

```
+-----------------------------------------------------------------------------------+
|                        Zero-Build Native Vanilla Web GUI                          |
|   - EventSource (SSE Listener)       - Interactive Trace & Graph Visualizer       |
|   - Tokenomics & Latency Dashboard   - In-Memory Vector & MCP Management          |
+------------------------------------------^----------------------------------------+
                                           | HTTP / Server-Sent Events (text/event-stream)
+------------------------------------------v----------------------------------------+
|                                Express.js API Gateway                             |
|   - /api/execute (REST/Stream)       - /api/tools (MCP Discovery)                 |
|   - /api/rag/documents (Vector RAG)  - /api/interview-qa (Architect Vault)        |
+------------------------------------------^----------------------------------------+
                                           |
+------------------------------------------v----------------------------------------+
|                      Multi-Agent Orchestration State Machine                      |
|                                                                                   |
|    +-------------------+      +-------------------+      +-------------------+    |
|    |   Planner Node    | ---> |   Executor Node   | ---> |    Critic Node    |    |
|    | (Task DAG Decomp) |      |   (ReAct Loop)    |      | (Evals & Self-Cor)|    |
|    +-------------------+      +---------+---------+      +---------+---------+    |
|              ^                          |                          |              |
|              |                          v                          |              |
|              +--------------------------+--------------------------+              |
|                               Self-Correction Loop                                |
+-----------------------------------------+-----------------------------------------+
                                          |
          +-------------------------------+-------------------------------+
          |                                                               |
          v                                                               v
+------------------------------------+          +------------------------------------+
|    Model Context Protocol (MCP)    |          |       In-Memory Vector RAG         |
|   - JSON-Schema Parameter Validation|          |   - Deterministic 128-D Vectorizer |
|   - Sandboxed Execution Timeout    |          |   - Exact Mathematical Cosine Sim  |
|   - Calculator, DB, Metrics, RAG   |          |   - L2 Norm Dot Product Optimizer  |
+------------------------------------+          +------------------------------------+
```

---

## 🔬 Core Engineering Innovations

### 1. Multi-Agent ReAct State Machine
- **Planner Node**: Decomposes high-level objectives into dependency-ordered Directed Acyclic Graphs (`ExecutionPlan` / `PlanStep`).
- **Executor Node**: Iterates through the step DAG via the **Thought $\rightarrow$ Action $\rightarrow$ Observation** loop, querying MCP tools and passing grounded context.
- **Critic Node**: Evaluates plan fulfillment, verifies ground truth consistency, scores output quality (0–100), checks hallucination risks, and executes targeted self-correction loops when needed.

### 2. Model Context Protocol (MCP) Tool Registry
- Conforms to the open standard MCP specification for tool discovery (`listTools`), dynamic JSON Schema validation, and execution sandboxing with hard execution timeouts (8000ms).
- Built-in tools: `vector_knowledge_search`, `calculator` (safe mathematical parser), `database_lookup` (enterprise pricing & architecture benchmarks), and `system_metrics` (host memory RSS, CPU, and Node.js process runtime).

### 3. Exact Mathematical Cosine Vector RAG
- Implements exact mathematical Cosine Similarity in continuous real vector space $\mathbb{R}^{128}$:
  $$\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} = \frac{\sum_{i=1}^n u_i v_i}{\sqrt{\sum_{i=1}^n u_i^2} \sqrt{\sum_{i=1}^n v_i^2}}$$
- Pre-computes unit L2 Euclidean normalization ($\|\mathbf{u}\| = 1.0$) upon document ingestion to collapse search queries into hardware-accelerated SIMD dot products.
- Sliding-window text chunker and automatic seeding of enterprise architecture knowledge.

### 4. Real-time Server-Sent Events (SSE) Streaming
- Unidirectional, low-overhead HTTP `text/event-stream` dispatching real-time trace events (`plan_created`, `step_start`, `thought`, `action_call`, `observation`, `critique`, `token_update`, `final_answer`).
- Outperforms WebSockets in proxy traversal, TLS termination, and native browser `EventSource` automatic reconnection.

### 5. Zero-Build Native Vanilla Web GUI
- Clean, responsive dark-mode dashboard implemented in pure HTML5, modern CSS, and ES6 modules without bundling overhead.
- Live agent topology canvas with animated node highlights, telemetry ribbon (prompt, completion, cache hits, cost USD, latency), and collapsible trace viewer.

---

## 🚀 Quick Start & Setup

### Prerequisites
- Node.js (v20+ LTS recommended, v22 tested)
- npm (v10+)

### Installation
```bash
# Clone and enter workspace
cd P:\prabhu\projects\git_ai\ai_arch

# Install dependencies
npm install
```

### Available NPM Scripts
| Script | Command | Purpose |
| :--- | :--- | :--- |
| `npm run dev` | `tsx watch src/index.ts` | Starts development server with hot-reloading |
| `npm run build` | `tsc` | Compiles TypeScript into standard `dist/` JS |
| `npm start` | `node dist/index.js` | Runs production compiled server |
| `npm test` | `tsx test/verify.ts` | Runs the automated 23-point verification test suite |
| `npm run generate:pdf` | `tsx scripts/generate-pdf.ts` | Compiles the 6-page comprehensive project & interview PDF |

---

## 🧪 Testing & Verification

Run the automated test suite to verify mathematical precision, MCP schema enforcement, RAG retrieval, and the complete ReAct orchestration loop:

```bash
npm test
```

### Verified Criteria:
```text
[Suite 1: Vector Mathematics & Geometry]
  ✅ [PASS] Dot product of [1,2,3] and [2,4,6] equals 28
  ✅ [PASS] Euclidean norm calculation accurate
  ✅ [PASS] Cosine similarity of collinear vectors equals 1.0
  ✅ [PASS] Cosine similarity of orthogonal vectors equals 0.0

[Suite 2: Vector RAG & Deterministic Embeddings]
  ✅ [PASS] Vector store auto-seeds default knowledge (count: 6)
  ✅ [PASS] Embedding vector has exactly 128 dimensions
  ✅ [PASS] Semantic search retrieves relevant documents
  ✅ [PASS] Top match correctly identified target document by cosine score
  ✅ [PASS] Cosine similarity score is high (got: 0.4759)

[Suite 3: Model Context Protocol (MCP) Tool Registry]
  ✅ [PASS] Registered at least 4 MCP tools
  ✅ [PASS] Calculator executed without error
  ✅ [PASS] Calculator evaluated expression correctly (got: 2512)
  ✅ [PASS] Schema validator catches missing required parameter

[Suite 4: Token Counter & Cost Modeling]
  ✅ [PASS] Token estimation realistic
  ✅ [PASS] Recorded prompt tokens
  ✅ [PASS] Calculated estimated cost USD
  ✅ [PASS] Simulated cache hit token discount

[Suite 5: Multi-Agent ReAct Workflow (Planner, Executor, Critic)]
  ✅ [PASS] Workflow completed successfully
  ✅ [PASS] Planner generated multi-step DAG plan
  ✅ [PASS] Orchestration engine emitted trace events (count: 19)
  ✅ [PASS] Critic evaluated output and recorded critique
  ✅ [PASS] Critic validated solution quality
  ✅ [PASS] Synthesized detailed final architectural solution
```

---

## 📡 REST & SSE API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Service health, memory RSS/heap, active SSE client count, and RAG stats |
| `GET` | `/api/tools` | Discovers all registered MCP tools and JSON schemas |
| `POST` | `/api/tools/execute` | Directly executes an MCP tool with schema validation |
| `GET` | `/api/rag/documents` | Lists all indexed vector documents and metadata |
| `POST` | `/api/rag/documents` | Indexes a new document chunk into the 128-D vector space |
| `POST` | `/api/rag/search` | Performs mathematical cosine similarity search |
| `GET` | `/api/stream` | Server-Sent Events endpoint (`text/event-stream`) |
| `POST` | `/api/execute` | Executes an end-to-end multi-agent workflow |
| `GET` | `/api/interview-qa` | Catalog of Principal AI Solution Architect scenario Q&As |

---

## 📚 Documentation Vault (`docs/`)

Explore the exhaustive markdown learning tutorials detailing every method, interface, and design trade-off:

1. [01_ARCHITECTURE_OVERVIEW.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/01_ARCHITECTURE_OVERVIEW.md): System topology, ReAct paradigm, sequence diagrams, and design trade-offs.
2. [02_MULTI_AGENT_ORCHESTRATION.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/02_MULTI_AGENT_ORCHESTRATION.md): Planner, Executor, and Critic node mechanics, DAG decomposition, and self-correction loops.
3. [03_MCP_TOOL_INTEGRATION.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/03_MCP_TOOL_INTEGRATION.md): Model Context Protocol standard, tool schema validation, sandboxing, and execution.
4. [04_VECTOR_RAG_MATHEMATICS.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/04_VECTOR_RAG_MATHEMATICS.md): Exact Cosine Similarity formulation, L2 unit norm, and HNSW vs IVFFlat indexing trade-offs.
5. [05_STREAMING_SSE_TELEMETRY.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/05_STREAMING_SSE_TELEMETRY.md): Server-Sent Events protocol specification, backpressure, and client EventSource implementation.
6. [06_TOKENOMICS_AND_COST_OPTIMIZATION.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/06_TOKENOMICS_AND_COST_OPTIMIZATION.md): Token estimation algorithms, KV-cache prefix hits, prompt caching economics, and multi-model routing.
7. [07_FRONTEND_UI_UX_DESIGN.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/07_FRONTEND_UI_UX_DESIGN.md): Zero-build vanilla architecture, state management, and real-time visual telemetry.
8. [08_ENTERPRISE_PRODUCTION_PLAYBOOK.md](file:///P:/prabhu/projects/git_ai/ai_arch/docs/08_ENTERPRISE_PRODUCTION_PLAYBOOK.md): Distributed scaling (Redis/Postgres), security guardrails (prompt injection defense), and OpenTelemetry.

---

## 📄 AI Architect PDF Handbook & Interview Vault

The complete project specification and masterclass interview questions have been compiled into a standalone PDF:

- **File Path**: [`AgentFlow_Studio_AI_Architect_Handbook.pdf`](file:///P:/prabhu/projects/git_ai/ai_arch/AgentFlow_Studio_AI_Architect_Handbook.pdf)
- **Contents**:
  - Part 1: Executive Engineering Blueprint & Mathematical Foundations
  - Part 2: Project Implementation & Component Catalog
  - Part 3: 25+ Principal AI Solution Architect Interview Questions & In-Depth Technical Solutions (Multi-Agent Systems, RAG at Scale, MCP Security, KV-Cache Optimization, Latency, and Evals)

To regenerate the PDF at any time:
```bash
npm run generate:pdf
```

---

## 🛡️ License

Apache-2.0. Authored for Principal AI-Native Solution Architecture.
