/**
 * AgentFlow Studio Entrypoint
 * Multi-Agent ReAct Orchestration, MCP Tool Registry, In-Memory Vector RAG, and Real-time SSE
 */

import { VectorStore } from './rag/vector-store.js';
import { MCPRegistry } from './mcp/registry.js';
import { initializeMCPTools } from './mcp/tools.js';
import { OrchestrationEngine } from './orchestrator/engine.js';
import { SSEManager } from './server/sse.js';
import { createServer } from './server/app.js';

async function bootstrap() {
  console.log('------------------------------------------------------------');
  console.log(' 🚀 AgentFlow Studio: Principal AI-Native Orchestration Engine');
  console.log('------------------------------------------------------------');

  // 1. Initialize Vector RAG Engine
  const vectorStore = new VectorStore();
  const stats = vectorStore.getStats();
  console.log(`[RAG] Vector Store initialized with ${stats.documentCount} seeded architectural documents.`);

  // 2. Initialize MCP Registry and Tools
  const mcpRegistry = new MCPRegistry();
  initializeMCPTools(mcpRegistry, vectorStore);
  console.log(`[MCP] Registered ${mcpRegistry.listTools().length} tools: ${mcpRegistry.listTools().map((t) => t.name).join(', ')}`);

  // 3. Initialize Orchestration Engine and SSE Manager
  const engine = new OrchestrationEngine(mcpRegistry, vectorStore);
  const sseManager = new SSEManager();

  // 4. Create and start HTTP/SSE Server
  const app = createServer(mcpRegistry, vectorStore, engine, sseManager);
  const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;

  const server = app.listen(PORT, () => {
    console.log(`[HTTP] AgentFlow Studio server listening on http://localhost:${PORT}`);
    console.log(`[GUI]  Vanilla Web GUI accessible at: http://localhost:${PORT}`);
    console.log(`[SSE]  EventStream endpoint live at:   http://localhost:${PORT}/api/stream`);
    console.log('------------------------------------------------------------');
  });

  // Graceful shutdown handling
  const shutdown = () => {
    console.log('\n[Shutdown] Closing active connections and terminating AgentFlow Studio...');
    server.close(() => {
      console.log('[Shutdown] Server exited cleanly.');
      process.exit(0);
    });
  };

  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

bootstrap().catch((err) => {
  console.error('[FATAL] Failed to bootstrap AgentFlow Studio:', err);
  process.exit(1);
});
