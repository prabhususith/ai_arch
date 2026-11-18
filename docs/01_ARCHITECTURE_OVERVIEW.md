# Module 01: System Architecture & ReAct Paradigm Overview

## 1. Executive Architectural Blueprint

**AgentFlow Studio** is an enterprise-grade AI-native agentic execution platform engineered for deterministic multi-agent orchestration, standardized tool calling, low-latency semantic retrieval, and real-time trace telemetry.

```
+-----------------------------------------------------------------------------------+
|                                Client Layer (Vanilla Web GUI)                     |
|   - EventSource (SSE Listener)       - Interactive Trace & Graph Visualizer       |
|   - Tokenomics & Latency Dashboard   - In-Memory Vector & MCP Management          |
+------------------------------------------^----------------------------------------+
                                           | HTTP / Server-Sent Events (text/event-stream)
+------------------------------------------v----------------------------------------+
|                                  Express.js API Gateway                           |
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

## 2. The Multi-Agent ReAct Paradigm

Direct single-prompt LLM generation suffers from **hallucination cascading**, wherein probabilistic errors in early sentences compound into entirely invalid conclusions. 

AgentFlow Studio implements the **ReAct (Reasoning and Acting)** framework through three specialized agent nodes:

1. **Planner Node**:
   - Takes arbitrary user goals and decomposes them into a discrete **Directed Acyclic Graph (DAG)** of execution steps.
   - Evaluates tool availability from the MCP catalog and assigns the most appropriate tool to each step with parameter hints.
2. **Executor Node**:
   - Runs through each planned step following the strict **Thought $\rightarrow$ Action $\rightarrow$ Observation** loop.
   - Ensures observations from tool execution are formatted and injected into contextual memory before progressing to dependent steps.
3. **Critic Node**:
   - Analyzes execution outputs against user constraints, verifies ground-truth consistency, scores result quality (0-100), and inspects for hallucination risks.
   - If quality falls below the threshold (75/100), the Critic triggers a **Self-Correction Loop**, generating revision instructions for the Planner.

---

## 3. Decoupled Model Context Protocol (MCP) Architecture

Rather than embedding bespoke function-calling logic inside prompt strings, AgentFlow Studio adopts the **Model Context Protocol (MCP)** specification:
- **Contract Standardization**: Tools publish their input requirements using standard JSON Schema definitions.
- **Runtime Sandboxing**: Tool executions are isolated, bound by configurable timeouts (default: 8000ms), and shielded by schema validation guards.
- **Extensibility**: Third-party or enterprise tools can be registered into `MCPRegistry` at runtime without altering core agent logic.

---

## 4. Key Design Trade-Offs

| Decision | Selected Approach | Alternative Rejected | Architectural Rationale |
| :--- | :--- | :--- | :--- |
| **Streaming Protocol** | Server-Sent Events (SSE) | WebSockets (WS) | Unidirectional streaming fits agent token telemetry; SSE requires no custom handshake, traverses HTTP proxies effortlessly, and features native browser reconnection. |
| **Vector Engine** | In-Memory Dense Cosine Store | External Vector DB (Pinecone/Milvus) | Zero external cloud dependencies, deterministic execution, and ultra-low latency for local development and edge deployments. |
| **Frontend Strategy** | Zero-Build Vanilla ES6 | React / Vite / Next.js Bundler | Eliminates build pipelines, dependencies, node-gyp native compilation friction, and yields instant deployment. |
