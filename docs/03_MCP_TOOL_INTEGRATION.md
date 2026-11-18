# Module 03: Model Context Protocol (MCP) Tool Integration

## 1. What is Model Context Protocol (MCP)?

The **Model Context Protocol (MCP)** is an open architectural contract standard that formalizes how AI agents discover, invoke, and inspect tools and contextual data sources.

### Core Problems Solved by MCP
1. **Schema Non-Uniformity**: Replaces vendor-specific tool declaration formats with standard JSON Schema.
2. **Brittle Prompt Injection**: Eliminates raw string parsing by delivering structured arguments and structured responses.
3. **Security Boundaries**: Enforces strict parameter boundary validation before invocation reaches host runtimes.

---

## 2. MCP Tool Registry Specification

In AgentFlow Studio, the `MCPRegistry` provides the backbone for tool operations:

```typescript
export interface MCPToolDefinition {
  name: string;
  description: string;
  inputSchema: MCPToolParameterSchema;
  category?: 'computation' | 'knowledge' | 'system' | 'web' | 'storage';
  timeoutMs?: number;
}
```

### Tool Execution Flow
1. **Lookup**: Retrieve registered tool by `toolCall.name`.
2. **Schema Validation**: Verify required properties and parameter types (`validateArguments`).
3. **Execution Sandboxing**: Race the tool promise against a configurable timeout promise (default: 8000ms).
4. **Standard Result Serialization**: Returns `MCPToolResult` with `isError`, `content` array (text/json), and `executionTimeMs`.

---

## 3. Built-in MCP Tools Suite

### 1. `vector_knowledge_search`
- **Purpose**: Semantic vector search over indexed architectural documents.
- **Parameters**: `query` (string, required), `topK` (number, default 3).
- **Output**: Ranked chunks with exact Cosine Similarity scores.

### 2. `calculator`
- **Purpose**: Safe mathematical, trigonometric, and statistical computation.
- **Parameters**: `expression` (string, required).
- **Security Guardrail**: Sanitizes inputs to prevent code injection, whitelisting only mathematical operators and `Math.*` functions.

### 3. `database_lookup`
- **Purpose**: Structured queries against enterprise catalogs (`model_pricing`, `architecture_blueprints`).
- **Parameters**: `table` (enum, required), `filterKey` (string), `filterValue` (string).

### 4. `system_metrics`
- **Purpose**: Real-time telemetry on host architecture, Node.js memory RSS/heap, platform, and uptime.
- **Parameters**: `detailLevel` ('summary' | 'verbose').
