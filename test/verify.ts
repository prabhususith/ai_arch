/**
 * Automated Verification & Architecture Test Suite
 * Validates VectorMath, MCP Tool Registry, Vector RAG search, and Multi-Agent ReAct workflow.
 */

import { VectorMath, SemanticVectorizer } from '../src/rag/embeddings.js';
import { VectorStore } from '../src/rag/vector-store.js';
import { MCPRegistry } from '../src/mcp/registry.js';
import { initializeMCPTools } from '../src/mcp/tools.js';
import { OrchestrationEngine } from '../src/orchestrator/engine.js';
import { TokenCounter } from '../src/telemetry/token-counter.js';

async function runTestSuite() {
  console.log('============================================================');
  console.log('🧪 Starting AgentFlow Studio System Verification Suite');
  console.log('============================================================');

  let passedTests = 0;
  let totalTests = 0;

  function assert(condition: boolean, testName: string) {
    totalTests++;
    if (condition) {
      console.log(`  ✅ [PASS] ${testName}`);
      passedTests++;
    } else {
      console.error(`  ❌ [FAIL] ${testName}`);
      throw new Error(`Test failed: ${testName}`);
    }
  }

  // --------------------------------------------------------------------------
  // Test 1: Mathematical Cosine Similarity and L2 Normalization
  // --------------------------------------------------------------------------
  console.log('\n[Suite 1: Vector Mathematics & Geometry]');
  const u = [1, 2, 3];
  const v = [2, 4, 6]; // Collinear vector
  const w = [-2, 1, 0]; // Orthogonal vector to [1, 2, 0]

  const dot = VectorMath.dotProduct(u, v);
  assert(dot === 28, `Dot product of [1,2,3] and [2,4,6] equals 28 (got: ${dot})`);

  const normU = VectorMath.norm(u);
  assert(Math.abs(normU - Math.sqrt(14)) < 1e-9, `Euclidean norm calculation accurate`);

  const cosineCollinear = VectorMath.cosineSimilarity(u, v);
  assert(Math.abs(cosineCollinear - 1.0) < 1e-6, `Cosine similarity of collinear vectors equals 1.0 (got: ${cosineCollinear.toFixed(6)})`);

  const u2 = [1, 2, 0];
  const cosineOrthogonal = VectorMath.cosineSimilarity(u2, w);
  assert(Math.abs(cosineOrthogonal - 0.0) < 1e-6, `Cosine similarity of orthogonal vectors equals 0.0 (got: ${cosineOrthogonal.toFixed(6)})`);

  // --------------------------------------------------------------------------
  // Test 2: Semantic Vectorizer & In-Memory RAG Store
  // --------------------------------------------------------------------------
  console.log('\n[Suite 2: Vector RAG & Deterministic Embeddings]');
  const store = new VectorStore();
  const initialStats = store.getStats();
  assert(initialStats.documentCount > 0, `Vector store auto-seeds default knowledge (count: ${initialStats.documentCount})`);

  // Add custom doc
  const customDoc = store.addDocument('Kubernetes orchestrates containerized LLM inference workloads across GPU clusters.', {
    title: 'K8s GPU Inference',
    category: 'infrastructure',
  });
  assert(customDoc.embedding.length === 128, `Embedding vector has exactly 128 dimensions`);

  // Query search
  const searchResults = store.similaritySearch('container GPU cluster workload', { topK: 2 });
  assert(searchResults.length > 0, `Semantic search retrieves relevant documents`);
  assert(searchResults[0].document.id === customDoc.id, `Top match correctly identified target document by cosine score`);
  assert(searchResults[0].score > 0.3, `Cosine similarity score is high (got: ${searchResults[0].score.toFixed(4)})`);

  // --------------------------------------------------------------------------
  // Test 3: Model Context Protocol (MCP) Registry & Tool Execution
  // --------------------------------------------------------------------------
  console.log('\n[Suite 3: Model Context Protocol (MCP) Tool Registry]');
  const registry = new MCPRegistry();
  initializeMCPTools(registry, store);

  const tools = registry.listTools();
  assert(tools.length >= 4, `Registered at least 4 MCP tools (found: ${tools.length})`);

  // Execute calculator tool
  const calcResult = await registry.executeTool({
    name: 'calculator',
    arguments: { expression: '100 * 25 + Math.sqrt(144)' },
  });
  assert(!calcResult.isError, `Calculator executed without error`);
  assert(calcResult.content[0].data.result === 2512, `Calculator evaluated expression correctly (expected: 2512, got: ${calcResult.content[0].data.result})`);

  // Test schema validation error capture
  const invalidCall = await registry.executeTool({
    name: 'calculator',
    arguments: {}, // missing required expression
  });
  assert(invalidCall.isError, `Schema validator catches missing required parameter`);

  // --------------------------------------------------------------------------
  // Test 4: Token Estimation & Cost Telemetry
  // --------------------------------------------------------------------------
  console.log('\n[Suite 4: Token Counter & Cost Modeling]');
  const sampleText = 'This is a test prompt designed to evaluate subword token estimation heuristics.';
  const tokens = TokenCounter.estimateTokens(sampleText);
  assert(tokens > 10 && tokens < 30, `Token estimation realistic (estimated: ${tokens})`);

  let telemetry = TokenCounter.createTelemetry();
  telemetry = TokenCounter.recordUsage(telemetry, sampleText, 'Short answer', 150, 10);
  assert(telemetry.promptTokens > 0, `Recorded prompt tokens`);
  assert(telemetry.estimatedCostUSD > 0, `Calculated estimated cost USD`);
  assert(telemetry.cacheHitTokens === 10, `Simulated cache hit token discount`);

  // --------------------------------------------------------------------------
  // Test 5: End-to-End Multi-Agent ReAct Workflow
  // --------------------------------------------------------------------------
  console.log('\n[Suite 5: Multi-Agent ReAct Workflow (Planner, Executor, Critic)]');
  const engine = new OrchestrationEngine(registry, store);

  let traceEventsCount = 0;
  engine.on('trace', () => {
    traceEventsCount++;
  });

  const finalState = await engine.runWorkflow('Calculate token cost for 5000 prompt tokens and explain ReAct architecture advantages.');

  assert(finalState.status === 'completed', `Workflow completed successfully`);
  assert(finalState.plan !== null && finalState.plan.steps.length >= 2, `Planner generated multi-step DAG plan`);
  assert(traceEventsCount >= 4, `Orchestration engine emitted trace events (count: ${traceEventsCount})`);
  assert(finalState.critiqueHistory.length > 0, `Critic evaluated output and recorded critique`);
  assert(finalState.critiqueHistory[0].passed, `Critic validated solution quality`);
  assert(typeof finalState.finalAnswer === 'string' && finalState.finalAnswer.length > 100, `Synthesized detailed final architectural solution`);

  console.log('\n============================================================');
  console.log(`🎉 ALL ${passedTests}/${totalTests} TESTS PASSED SUCCESSFULLY!`);
  console.log('============================================================\n');
}

runTestSuite().catch((err) => {
  console.error('\n❌ Test suite failed:', err);
  process.exit(1);
});
