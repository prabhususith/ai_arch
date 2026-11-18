/**
 * AgentFlow Studio: Type System & Domain Contracts
 * Principal AI-Native Architecture Core Definitions
 */

// ============================================================================
// 1. Model Context Protocol (MCP) Tool Contracts
// ============================================================================

export type JSONSchemaType = 'string' | 'number' | 'boolean' | 'object' | 'array' | 'null';

export interface JSONSchemaProperty {
  type: JSONSchemaType;
  description: string;
  enum?: string[];
  items?: JSONSchemaProperty;
  properties?: Record<string, JSONSchemaProperty>;
  required?: string[];
}

export interface MCPToolParameterSchema {
  type: 'object';
  properties: Record<string, JSONSchemaProperty>;
  required?: string[];
}

export interface MCPToolDefinition {
  name: string;
  description: string;
  inputSchema: MCPToolParameterSchema;
  category?: 'computation' | 'knowledge' | 'system' | 'web' | 'storage';
  timeoutMs?: number;
}

export interface MCPToolCall {
  name: string;
  arguments: Record<string, any>;
}

export interface MCPToolResult {
  toolName: string;
  isError: boolean;
  content: Array<{
    type: 'text' | 'json' | 'image';
    text?: string;
    data?: any;
  }>;
  executionTimeMs: number;
}

// ============================================================================
// 2. Vector RAG & Mathematical Embedding Types
// ============================================================================

export type EmbeddingVector = number[];

export interface VectorDocumentMetadata {
  source: string;
  category: string;
  title?: string;
  chunkIndex?: number;
  tags?: string[];
  createdAt: number;
}

export interface VectorDocument {
  id: string;
  content: string;
  embedding: EmbeddingVector;
  metadata: VectorDocumentMetadata;
}

export interface VectorSearchResult {
  document: VectorDocument;
  score: number; // Cosine similarity: -1.0 to 1.0 (normalized 0.0 to 1.0 for non-negative spaces)
}

export interface RAGSearchOptions {
  topK?: number;
  minSimilarity?: number;
  filterCategory?: string;
}

// ============================================================================
// 3. Multi-Agent ReAct Orchestration Contracts
// ============================================================================

export type AgentRole = 'planner' | 'executor' | 'critic';

export type StepStatus = 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';

export interface PlanStep {
  id: string;
  order: number;
  description: string;
  toolToUse?: string;
  toolArgsHint?: Record<string, any>;
  dependencies: string[]; // step IDs that must complete first
  status: StepStatus;
  output?: string;
  error?: string;
}

export interface ExecutionPlan {
  planId: string;
  goal: string;
  steps: PlanStep[];
  strategyRationale: string;
  estimatedComplexity: 'low' | 'medium' | 'high';
  createdAt: number;
}

export type TraceEventType =
  | 'plan_created'
  | 'step_start'
  | 'thought'
  | 'action_call'
  | 'observation'
  | 'critique'
  | 'plan_revised'
  | 'token_update'
  | 'final_answer'
  | 'error';

export interface TraceEvent {
  id: string;
  timestamp: number;
  node: AgentRole | 'orchestrator' | 'mcp_registry';
  stepId?: string;
  type: TraceEventType;
  title: string;
  payload: any;
  durationMs?: number;
}

export interface CritiqueResult {
  passed: boolean;
  score: number; // 0 to 100
  feedback: string;
  hallucinationRisk: 'none' | 'low' | 'moderate' | 'high';
  suggestedRevision?: string;
  shouldRetry: boolean;
}

export interface AgentState {
  sessionId: string;
  goal: string;
  plan: ExecutionPlan | null;
  currentStepIndex: number;
  memory: Array<{
    role: 'user' | 'assistant' | 'system' | 'tool';
    content: string;
    timestamp: number;
  }>;
  trace: TraceEvent[];
  critiqueHistory: CritiqueResult[];
  finalAnswer: string | null;
  status: 'idle' | 'planning' | 'executing' | 'critiquing' | 'completed' | 'failed';
  telemetry: TokenTelemetry;
}

// ============================================================================
// 4. Tokenomics & Performance Telemetry
// ============================================================================

export interface TokenTelemetry {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
  cacheHitTokens: number;
  estimatedCostUSD: number;
  totalLatencyMs: number;
  stepCount: number;
}

export interface TokenRateModel {
  name: string;
  promptPricePer1K: number;
  completionPricePer1K: number;
}

// ============================================================================
// 5. Server-Sent Events (SSE) Protocol Payloads
// ============================================================================

export interface SSEMessage {
  event: 'status' | 'trace' | 'plan' | 'telemetry' | 'result' | 'error' | 'done';
  data: any;
}
