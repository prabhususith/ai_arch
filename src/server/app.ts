/**
 * Express Application & REST/SSE Endpoints
 * Exposes multi-agent execution, MCP catalog, Vector RAG queries, and SSE streaming.
 */

import express, { Request, Response } from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { MCPRegistry } from '../mcp/registry.js';
import { VectorStore } from '../rag/vector-store.js';
import { OrchestrationEngine } from '../orchestrator/engine.js';
import { SSEManager } from './sse.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function createServer(
  mcpRegistry: MCPRegistry,
  vectorStore: VectorStore,
  engine: OrchestrationEngine,
  sseManager: SSEManager
) {
  const app = express();

  app.use(cors());
  app.use(express.json());

  // Serve static assets from public/
  const publicDir = path.resolve(__dirname, '../../public');
  app.use(express.static(publicDir));

  // --------------------------------------------------------------------------
  // 1. Health & Host Telemetry
  // --------------------------------------------------------------------------
  app.get('/api/health', (req: Request, res: Response) => {
    res.json({
      status: 'healthy',
      service: 'AgentFlow Studio',
      timestamp: Date.now(),
      sseClients: sseManager.getActiveCount(),
      mcpToolsCount: mcpRegistry.listTools().length,
      ragStats: vectorStore.getStats(),
      nodeVersion: process.version,
      memoryUsageMB: {
        rss: Number((process.memoryUsage().rss / 1024 / 1024).toFixed(2)),
        heapUsed: Number((process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2)),
      },
    });
  });

  // --------------------------------------------------------------------------
  // 2. MCP Tool Registry Endpoints
  // --------------------------------------------------------------------------
  app.get('/api/tools', (req: Request, res: Response) => {
    res.json({
      count: mcpRegistry.listTools().length,
      tools: mcpRegistry.listTools(),
    });
  });

  app.post('/api/tools/execute', async (req: Request, res: Response) => {
    const { name, arguments: args } = req.body;
    if (!name) {
      return res.status(400).json({ error: 'Tool name is required.' });
    }
    const result = await mcpRegistry.executeTool({ name, arguments: args || {} });
    res.json(result);
  });

  // --------------------------------------------------------------------------
  // 3. Vector RAG Store Endpoints
  // --------------------------------------------------------------------------
  app.get('/api/rag/documents', (req: Request, res: Response) => {
    const docs = vectorStore.getAllDocuments();
    res.json({
      count: docs.length,
      documents: docs.map((d) => ({
        id: d.id,
        title: d.metadata.title,
        category: d.metadata.category,
        source: d.metadata.source,
        contentPreview: d.content.slice(0, 160) + '...',
        content: d.content,
        embeddingDimension: d.embedding.length,
        createdAt: d.metadata.createdAt,
      })),
    });
  });

  app.post('/api/rag/documents', (req: Request, res: Response) => {
    const { content, title, category } = req.body;
    if (!content) {
      return res.status(400).json({ error: 'Content is required.' });
    }
    const doc = vectorStore.addDocument(content, {
      title: title || 'User Knowledge Note',
      category: category || 'user_uploads',
      source: 'api_upload',
    });
    res.status(201).json({
      message: 'Document successfully vectorized and indexed.',
      document: {
        id: doc.id,
        title: doc.metadata.title,
        category: doc.metadata.category,
        embeddingLength: doc.embedding.length,
      },
    });
  });

  app.post('/api/rag/search', (req: Request, res: Response) => {
    const { query, topK = 3, minSimilarity = 0.1 } = req.body;
    if (!query) {
      return res.status(400).json({ error: 'Search query is required.' });
    }
    const results = vectorStore.similaritySearch(query, { topK, minSimilarity });
    res.json({
      query,
      resultsCount: results.length,
      results: results.map((r) => ({
        id: r.document.id,
        title: r.document.metadata.title,
        category: r.document.metadata.category,
        score: Number(r.score.toFixed(4)),
        content: r.document.content,
      })),
    });
  });

  // --------------------------------------------------------------------------
  // 4. Server-Sent Events (SSE) Streaming Route
  // --------------------------------------------------------------------------
  app.get('/api/stream', (req: Request, res: Response) => {
    const clientId = (req.query.sessionId as string) || `sess_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    sseManager.registerClient(clientId, res);
  });

  // --------------------------------------------------------------------------
  // 5. Workflow Execution Endpoint (SSE + REST)
  // --------------------------------------------------------------------------
  app.post('/api/execute', async (req: Request, res: Response) => {
    const { goal, sessionId } = req.body;
    if (!goal || typeof goal !== 'string') {
      return res.status(400).json({ error: 'Goal string is required.' });
    }

    const currentSessionId = sessionId || `sess_${Date.now()}`;

    // Wire engine event hooks to SSE manager for this specific session or broadcast
    const onStatus = (data: any) => sseManager.send(currentSessionId, 'status', data);
    const onPlan = (data: any) => sseManager.send(currentSessionId, 'plan', data);
    const onTrace = (data: any) => sseManager.send(currentSessionId, 'trace', data);
    const onTelemetry = (data: any) => sseManager.send(currentSessionId, 'telemetry', data);
    const onResult = (data: any) => sseManager.send(currentSessionId, 'result', data);

    engine.on('status', onStatus);
    engine.on('plan', onPlan);
    engine.on('trace', onTrace);
    engine.on('telemetry', onTelemetry);
    engine.on('result', onResult);

    try {
      const finalState = await engine.runWorkflow(goal, currentSessionId);
      res.json({
        sessionId: currentSessionId,
        status: finalState.status,
        plan: finalState.plan,
        telemetry: finalState.telemetry,
        finalAnswer: finalState.finalAnswer,
        traceCount: finalState.trace.length,
      });
    } catch (err: any) {
      sseManager.send(currentSessionId, 'error', { message: err.message });
      res.status(500).json({ error: err.message });
    } finally {
      engine.off('status', onStatus);
      engine.off('plan', onPlan);
      engine.off('trace', onTrace);
      engine.off('telemetry', onTelemetry);
      engine.off('result', onResult);
    }
  });

  // --------------------------------------------------------------------------
  // 6. AI Architect Interview Questions & Answers Catalog
  // --------------------------------------------------------------------------
  app.get('/api/interview-qa', (req: Request, res: Response) => {
    res.json({
      role: 'Principal AI-Native Solution Architect',
      totalQuestions: 15,
      sections: [
        {
          category: 'Multi-Agent Systems & ReAct Architecture',
          questions: [
            {
              q: 'How does the ReAct (Reasoning + Acting) pattern solve hallucination cascading compared to direct LLM generation?',
              a: 'ReAct forces explicit thought reasoning prior to triggering bounded, verifiable external actions (MCP tools / APIs). The observation from the environment is fed back into context before the next thought, grounding intermediate reasoning steps in concrete facts rather than probabilistic autoregression.',
            },
            {
              q: 'In a multi-agent topology (Planner, Executor, Critic), how do you prevent deadlocks and infinite self-correction loops?',
              a: 'Deadlock prevention requires strict state-machine guardrails: (1) Monotonic step progression with dependency DAG checking, (2) Hard bounded retry caps on Critic re-evaluations (e.g., maximum 2 retry iterations), and (3) Graceful degradation policies where sub-optimal answers with low confidence scores are returned with explicit uncertainty warnings rather than halting the process.',
            },
          ],
        },
        {
          category: 'Vector RAG & Mathematical Retrieval',
          questions: [
            {
              q: 'Explain the mathematical equivalence between Cosine Similarity and Dot Product for normalized vectors.',
              a: 'Cosine similarity is defined as (u . v) / (||u|| * ||v||). When both vectors u and v are L2-normalized during document ingestion (such that ||u|| = 1 and ||v|| = 1), the denominator simplifies to 1 * 1 = 1. Consequently, cosine similarity reduces to the pure dot product (sum(u_i * v_i)), enabling vector engines to avoid costly square-root calculations at query runtime and leverage hardware SIMD/BLAS instructions.',
            },
            {
              q: 'What are the architectural trade-offs between Approximate Nearest Neighbor (ANN) indexes like HNSW vs IVFFlat?',
              a: 'HNSW (Hierarchical Navigable Small World) provides superior recall (>98%) and sub-millisecond query latency through multi-layer skip-list graph traversal, but consumes substantial memory (2-4x vector size) and requires longer build times. IVFFlat clusters vectors into Voronoi cells, reducing memory footprint and index build time, but suffers lower recall and higher latency on high-dimensional vectors unless inverted lists are extensively searched (nprobe increase).',
            },
          ],
        },
        {
          category: 'Model Context Protocol (MCP) & Tool Registry',
          questions: [
            {
              q: 'Why adopt the Model Context Protocol (MCP) over ad-hoc custom function-calling wrappers?',
              a: 'MCP standardizes tool discovery, parameter schemas (JSON Schema), error handling, and resource streaming across diverse LLM providers and agent hosts. It decouples tool implementations into reusable micro-services, facilitates capability negotiation, and enables standardized security sandboxing without vendor lock-in.',
            },
          ],
        },
      ],
    });
  });

  return app;
}
