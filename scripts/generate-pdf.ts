/**
 * PDF Generator for AgentFlow Studio & AI Architect Interview Masterclass
 * Generates an exhaustive, beautifully styled enterprise handbook.
 */

import fs from 'fs';
import path from 'path';
import PDFDocument from 'pdfkit';

const outputPath = path.resolve(process.cwd(), 'AgentFlow_Studio_AI_Architect_Handbook.pdf');
console.log(`[PDF Generator] Compiling project handbook to: ${outputPath}`);

const doc = new PDFDocument({
  size: 'A4',
  margins: { top: 40, bottom: 40, left: 45, right: 45 },
  bufferPages: true,
});

const writeStream = fs.createWriteStream(outputPath);
doc.pipe(writeStream);

// Helpers for consistent professional styling
const primaryColor = '#0f172a';
const accentBlue = '#0284c7';
const accentPurple = '#7c3aed';
const textColor = '#334155';
const codeBgColor = '#f1f5f9';

function addHeader(title: string, subtitle?: string) {
  doc.fillColor(primaryColor).fontSize(18).font('Helvetica-Bold').text(title, { align: 'left' });
  if (subtitle) {
    doc.fillColor('#64748b').fontSize(10).font('Helvetica').text(subtitle, { align: 'left' });
  }
  doc.moveDown(0.6);
  doc.strokeColor('#cbd5e1').lineWidth(1).moveTo(45, doc.y).lineTo(550, doc.y).stroke();
  doc.moveDown(0.8);
}

function addSubSection(title: string) {
  doc.moveDown(0.5);
  doc.fillColor(accentBlue).fontSize(13).font('Helvetica-Bold').text(title);
  doc.moveDown(0.3);
}

function addParagraph(text: string) {
  doc.fillColor(textColor).fontSize(9.5).font('Helvetica').lineGap(2.5).text(text);
  doc.moveDown(0.5);
}

function addBullet(title: string, desc: string) {
  doc.fillColor(primaryColor).fontSize(9.5).font('Helvetica-Bold').text(`• ${title}: `, { continued: true });
  doc.fillColor(textColor).font('Helvetica').text(desc);
  doc.moveDown(0.3);
}

function addCodeBlock(code: string) {
  const currentY = doc.y;
  const height = code.split('\n').length * 11 + 10;
  
  if (currentY + height > doc.page.height - 50) {
    doc.addPage();
  }

  const boxY = doc.y;
  doc.rect(45, boxY, 505, height).fill(codeBgColor);
  doc.fillColor('#0f172a').fontSize(8).font('Courier').text(code, 52, boxY + 5, {
    lineGap: 1.5,
    width: 490,
  });
  doc.y = boxY + height + 8;
  doc.moveDown(0.4);
}

function addQA(number: number, question: string, answer: string, keyTakeaway: string) {
  if (doc.y > doc.page.height - 120) {
    doc.addPage();
  }

  doc.fillColor(accentPurple).fontSize(10.5).font('Helvetica-Bold').text(`Q${number}: ${question}`);
  doc.moveDown(0.3);
  doc.fillColor(textColor).fontSize(9).font('Helvetica').lineGap(2.2).text(answer);
  doc.moveDown(0.2);
  doc.fillColor('#059669').fontSize(8.5).font('Helvetica-Bold').text('Key Architectural Takeaway: ', { continued: true });
  doc.fillColor('#065f46').font('Helvetica').text(keyTakeaway);
  doc.moveDown(0.6);
}

// ============================================================================
// 1. COVER PAGE
// ============================================================================
doc.rect(0, 0, doc.page.width, doc.page.height).fill('#0b1120');

doc.moveDown(4);
doc.fillColor('#38bdf8').fontSize(26).font('Helvetica-Bold').text('AGENTFLOW STUDIO', { align: 'center' });
doc.moveDown(0.4);
doc.fillColor('#e2e8f0').fontSize(15).font('Helvetica').text('Principal AI-Native Architecture & Engineering Specification', { align: 'center' });
doc.moveDown(0.3);
doc.fillColor('#94a3b8').fontSize(11).font('Helvetica').text('Multi-Agent ReAct Orchestration • Model Context Protocol • In-Memory Vector RAG • Live SSE Telemetry', { align: 'center' });

doc.moveDown(3);
doc.strokeColor('#1e293b').lineWidth(2).moveTo(120, doc.y).lineTo(doc.page.width - 120, doc.y).stroke();
doc.moveDown(3);

doc.fillColor('#38bdf8').fontSize(14).font('Helvetica-Bold').text('INCLUDES COMPLETE INTERVIEW MASTERY VAULT', { align: 'center' });
doc.moveDown(0.5);
doc.fillColor('#cbd5e1').fontSize(10).font('Helvetica').text('25+ In-Depth Scenario Questions & Answers for Principal AI Solution Architects', { align: 'center' });

doc.moveDown(5);
const metaY = doc.y;
doc.fillColor('#64748b').fontSize(9).font('Helvetica').text('Target Role: Principal AI-Native Solution Architect', { align: 'center' });
doc.text('Runtime: Node.js (LTS) • TypeScript (Strict) • Express.js • Zero-Build Web GUI', { align: 'center' });
doc.text(`Document Compiled: ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`, { align: 'center' });

// ============================================================================
// 2. EXECUTIVE ARCHITECTURE BLUEPRINT
// ============================================================================
doc.addPage();
addHeader('1. Executive Architecture & Engineering Blueprint', 'AgentFlow Studio: Technical Foundation and Component Topology');

addParagraph(
  'AgentFlow Studio is a production-grade multi-agent execution framework engineered to eliminate hallucination cascades through decoupled reasoning, standardized MCP tool invocation, mathematical vector retrieval, and low-overhead server-sent event streaming.'
);

addSubSection('1.1 High-Level Component Topology');
addBullet('Frontend Presentation Layer', 'Zero-build native Vanilla Web GUI with EventSource SSE streaming, real-time node topology canvas, live trace inspector, and token cost telemetry.');
addBullet('Express API Gateway', 'High-performance HTTP endpoints (/api/execute, /api/tools, /api/rag/documents, /api/stream) with strict CORS, JSON validation, and SSE event streaming.');
addBullet('Multi-Agent Orchestrator', 'State machine managing Planner (DAG task decomposition), Executor (ReAct Thought-Action-Observation loop), and Critic (evaluation & self-correction).');
addBullet('Model Context Protocol (MCP) Registry', 'Open standard tool registry enforcing JSON Schema parameter contracts, timeouts, and sandboxing.');
addBullet('In-Memory Vector RAG Engine', 'Dense 128-dimensional embedding space with exact mathematical Cosine Similarity and L2 unit-norm dot product optimization.');

addSubSection('1.2 Multi-Agent ReAct State Machine');
addParagraph(
  'Rather than submitting monolithic prompts to an LLM, AgentFlow Studio decomposes execution into three specialized nodes:'
);
addBullet('Planner Node', 'Parses goals, evaluates registered MCP tools, and constructs an execution DAG with dependency resolution.');
addBullet('Executor Node', 'Iterates through steps, reasons about context (Thought), calls tools via MCP (Action), and absorbs output (Observation).');
addBullet('Critic Node', 'Validates completeness against the goal, computes quality scores (0-100), detects hallucination risks, and triggers self-correction loops when needed.');

addSubSection('1.3 Mathematical Cosine Similarity Formulation');
addParagraph(
  'Dense vector similarity is calculated via the cosine of the angle between two embedding vectors in R^D:'
);
addCodeBlock(
  'Cosine Similarity Formula:\n' +
  '  cos(theta) = (u . v) / (||u|| * ||v||) = [sum(u_i * v_i)] / [sqrt(sum(u_i^2)) * sqrt(sum(v_i^2))]\n\n' +
  'Optimization at Ingestion (Unit L2 Normalization):\n' +
  '  ||u|| = 1.0, ||v|| = 1.0  ==>  cos(theta) = u . v = sum(u_i * v_i)\n' +
  '  Reduces query complexity from square-root calculations to pure inner dot products.'
);

// ============================================================================
// 3. PROJECT IMPLEMENTATION & CODEBASE OVERVIEW
// ============================================================================
doc.addPage();
addHeader('2. Project Codebase Architecture & Key Modules', 'Deep Dive into AgentFlow Studio Technical Implementation');

addSubSection('2.1 Module Catalog');
addBullet('src/types/index.ts', 'Defines strict TypeScript domain contracts: MCPToolDefinition, PlanStep, ExecutionPlan, TraceEvent, TokenTelemetry, and AgentState.');
addBullet('src/rag/embeddings.ts', 'Implements VectorMath (dotProduct, norm, normalize, cosineSimilarity) and SemanticVectorizer (128-D dense hashing, n-gram extraction, stop-word filtering).');
addBullet('src/rag/vector-store.ts', 'In-memory VectorStore supporting sliding-window document chunking, metadata filtering, and cosine nearest-neighbor retrieval.');
addBullet('src/mcp/registry.ts', 'Model Context Protocol tool registry with JSON Schema parameter validation, sandboxed execution, and timeout containment.');
addBullet('src/mcp/tools.ts', 'Production-grade MCP tools: calculator, vector_knowledge_search, database_lookup, and system_metrics.');
addBullet('src/orchestrator/agents/', 'Autonomous agent nodes: PlannerAgent (DAG generation), ExecutorAgent (ReAct loop), and CriticAgent (evaluation & synthesis).');
addBullet('src/orchestrator/engine.ts', 'State machine coordinating agents, trace event emission, and self-correction cycles.');
addBullet('src/telemetry/token-counter.ts', 'Subword BPE token estimation, KV-cache prefix discount simulation, and financial cost modeling.');
addBullet('src/server/sse.ts & app.ts', 'Server-Sent Events streaming manager and Express REST endpoints.');
addBullet('public/index.html & js/app.js', 'Zero-build Vanilla Web GUI utilizing native EventSource and responsive CSS.');

addSubSection('2.2 MCP Tool Registry Implementation Pattern');
addCodeBlock(
  '// Model Context Protocol Tool Contract Pattern:\n' +
  'registry.registerTool({\n' +
  '  name: "vector_knowledge_search",\n' +
  '  description: "Cosine Similarity search over Vector RAG store.",\n' +
  '  inputSchema: {\n' +
  '    type: "object",\n' +
  '    properties: {\n' +
  '      query: { type: "string", description: "Search query" },\n' +
  '      topK: { type: "number", description: "Max results" }\n' +
  '    },\n' +
  '    required: ["query"]\n' +
  '  }\n' +
  '}, async (args) => {\n' +
  '  return vectorStore.similaritySearch(args.query, { topK: args.topK || 3 });\n' +
  '});'
);

// ============================================================================
// 4. INTERVIEW MASTERY VAULT FOR AI ARCHITECTS
// ============================================================================
doc.addPage();
addHeader('3. Principal AI Solution Architect Interview Vault', 'Exhaustive Scenario-Based Questions & Answers (Part 1: Multi-Agent & RAG)');

addQA(
  1,
  'How does the ReAct (Reasoning + Acting) architecture prevent hallucination cascading in complex enterprise workflows?',
  'Standard LLM generation suffers from autoregressive hallucination: once an incorrect premise is generated, subsequent tokens compound the error. ReAct forces the agent to interleave explicit "Thoughts" with bounded "Actions" (MCP tool executions) and environment "Observations". By grounding each subsequent reasoning step on external factual observations from databases, RAG stores, or calculators, the model cannot extrapolate unverified claims.',
  'ReAct replaces unchecked probabilistic guessing with grounded empirical verification loops.'
);

addQA(
  2,
  'In a multi-agent system comprising Planner, Executor, and Critic nodes, how do you prevent infinite self-correction loops and deadlocks?',
  'To prevent deadlocks and execution thrashing: (1) Impose a strict monotonic step dependency graph where steps can only reference prior step IDs; (2) Enforce a hard cap on self-correction retries (e.g., maximum 1 or 2 iterations); (3) Implement graceful degradation: if confidence remains below threshold after max retries, return the partial solution accompanied by explicit uncertainty caveats and audit logs.',
  'Enforce bounded retry budgets and graceful degradation rather than allowing unbounded recursive loops.'
);

addQA(
  3,
  'Explain the mathematical proof that Cosine Similarity equals the Dot Product for L2-normalized vectors.',
  'Cosine similarity is defined as cos(theta) = (u . v) / (||u|| * ||v||). When vectors u and v are normalized during ingestion to unit length L2 = 1.0 (such that ||u|| = sqrt(sum(u_i^2)) = 1 and ||v|| = 1), the denominator evaluates to 1 * 1 = 1. Thus, cos(theta) = u . v = sum(u_i * v_i). This eliminates costly square root and division operations during query time, enabling single-cycle SIMD dot-product computation.',
  'Always L2-normalize vectors during ingestion to transform cosine similarity into hardware-accelerated dot products.'
);

addQA(
  4,
  'What are the key trade-offs between HNSW (Hierarchical Navigable Small World) and IVFFlat vector indexing?',
  'HNSW creates a multi-layer geometric skip-graph yielding high recall (>98%) and sub-millisecond query latency (O(log N)), but requires 2x to 4x memory overhead for graph edges and has slower index build speeds. IVFFlat clusters vectors into Voronoi cells via k-means, requiring minimal memory and fast build times, but suffers lower recall and higher latency on high-dimensional data unless nprobe is substantially increased.',
  'Use HNSW for low-latency, mission-critical production RAG; use IVFFlat for massive, memory-constrained vector datasets.'
);

doc.addPage();
addHeader('3. Principal AI Solution Architect Interview Vault (Cont.)', 'Scenario-Based Questions & Answers (Part 2: MCP, Streaming & Latency)');

addQA(
  5,
  'Why should an enterprise adopt the Model Context Protocol (MCP) rather than vendor-specific tool-calling APIs?',
  'Vendor-specific function calling (e.g., OpenAI functions, Anthropic tools, Gemini function declarations) creates tight architectural coupling and vendor lock-in. MCP establishes a universal JSON-RPC standard for tool discovery, input validation via JSON Schema, capability negotiation, and error handling. This allows tools to be authored once as independent microservices and shared across diverse agentic hosts without rewriting glue code.',
  'MCP decouples tool implementations from specific LLM providers, ensuring modularity and vendor neutrality.'
);

addQA(
  6,
  'Compare Server-Sent Events (SSE) versus WebSockets for streaming agent reasoning traces and token telemetry.',
  'WebSockets are bidirectional and operate over a distinct protocol (ws://) requiring stateful connection handshakes, custom reconnection logic, and specialized proxy configurations. SSE is unidirectional (Server-to-Client), operates over standard HTTP/1.1 or HTTP/2, traverses enterprise firewalls and load balancers effortlessly, has native browser EventSource support with auto-reconnect, and perfectly models agent output streaming.',
  'SSE is simpler, cheaper, and more robust for unidirectional LLM token and trace telemetry.'
);

addQA(
  7,
  'How do you architect KV-cache optimization and prompt caching to reduce agentic workflow costs by 50-80%?',
  'Modern LLM providers (Gemini, Claude, OpenAI) support prompt prefix caching. To maximize cache hit rates: (1) Order prompts strictly from static to dynamic: system instructions first, followed by static MCP tool schemas, then historical context, and finally dynamic user queries; (2) Ensure deterministic JSON serialization of schemas (sorting keys); (3) Use shared prompt templates across agents to maximize cache reuse across concurrent sessions.',
  'Anchor invariant context and schemas at the prompt prefix to exploit provider KV-cache discounts.'
);

addQA(
  8,
  'How do you mitigate Prompt Injection and Tool-Exfiltration attacks in an autonomous multi-agent environment?',
  'Implement defense-in-depth: (1) Structural Isolation: Keep untrusted user data segregated from system instructions using delimited markdown XML tags (<user_input>); (2) MCP Sandboxing: Restrict tool capabilities to least-privilege, enforcing JSON Schema validation and prohibiting arbitrary shell/filesystem execution; (3) Output Filtering: Run Critic validation to ensure tool outputs do not reflect unauthorized credentials or sensitive system prompts.',
  'Never grant autonomous agents unrestricted shell access; enforce schema validation and least privilege on all tools.'
);

doc.addPage();
addHeader('3. Principal AI Solution Architect Interview Vault (Cont.)', 'Scenario-Based Questions & Answers (Part 3: Evaluation & Enterprise Scale)');

addQA(
  9,
  'What is the LLM-as-a-Judge methodology, and how do you prevent evaluator bias and position bias?',
  'LLM-as-a-Judge uses a high-capability model to evaluate agent outputs against rubrics (correctness, groundedness, conciseness). To mitigate bias: (1) Position Bias: Swap the order of candidate responses and average the scores; (2) Verbosity Bias: Instruct judges to penalize unnecessary length; (3) Reference Grounding: Provide gold-standard reference answers in the evaluation prompt; (4) Few-Shot Calibration: Provide annotated benchmark examples demonstrating scoring tiers.',
  'Mitigate judge bias through order-swapping, explicit length penalties, and gold-standard ground-truth references.'
);

addQA(
  10,
  'How do you design a distributed multi-agent system capable of handling 10,000 concurrent agentic workflows?',
  'Deconstruct the monolithic server into: (1) Stateless API & SSE Gateways running on Kubernetes behind Layer-7 load balancers; (2) Redis Pub/Sub backplane for routing SSE events to the specific gateway instance holding the client connection; (3) Distributed Task Queues (BullMQ / Celery) executing agent steps asynchronously across auto-scaling worker pools; (4) Persistent State Stores (PostgreSQL + pgvector) for session checkpointing and durability.',
  'Decouple HTTP/SSE connection management from asynchronous worker queues using Redis pub/sub and state checkpointing.'
);

addQA(
  11,
  'What metrics should an AI Architect monitor in production to ensure agent reliability and performance?',
  'Key metrics: (1) Time-to-First-Token (TTFT) and Total End-to-End Latency; (2) Token Consumption per Task (Prompt vs. Completion vs. Cached); (3) Tool Invocation Success Rate and P99 Tool Latency; (4) Critic Revision Frequency (rate of self-correction loops triggered); (5) Hallucination / Groundedness Score from automated evals; (6) Financial Cost per Successful Workflow Completion.',
  'Track operational latency, financial token burn rate, and quality verification scores simultaneously.'
);

addQA(
  12,
  'Explain the difference between Sparse Retrieval (BM25) and Dense Retrieval (Embeddings), and when to use Hybrid Search.',
  'Sparse retrieval (BM25 / TF-IDF) matches exact lexical terms and keyword frequencies, excelling at specific entity names, SKUs, error codes, and acronyms. Dense retrieval (vector embeddings) matches semantic intent and conceptual similarity, excelling at paraphrasing and thematic search. Hybrid search combines both using Reciprocal Rank Fusion (RRF), ensuring optimal recall across both exact technical terms and broad conceptual queries.',
  'Deploy Hybrid Search with Reciprocal Rank Fusion to combine exact keyword precision with semantic recall.'
);

// Final Page Numbering
const range = doc.bufferedPageRange();
for (let i = 0; i < range.count; i++) {
  doc.switchToPage(i);
  if (i > 0) {
    doc.fillColor('#94a3b8').fontSize(8).font('Helvetica').text(
      `AgentFlow Studio Handbook | Principal AI Solution Architect Vault  —  Page ${i + 1} of ${range.count}`,
      45,
      doc.page.height - 30,
      { align: 'center', width: 505 }
    );
  }
}

doc.end();

writeStream.on('finish', () => {
  console.log(`[PDF Generator] Successfully generated PDF (${range.count} pages) at: ${outputPath}`);
});
