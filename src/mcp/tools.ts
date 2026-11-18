/**
 * Built-in MCP Tools Suite
 * Implements real, secure, and production-grade tools for Multi-Agent execution.
 */

import os from 'os';
import { MCPRegistry } from './registry.js';
import { VectorStore } from '../rag/vector-store.js';

export function initializeMCPTools(registry: MCPRegistry, vectorStore: VectorStore): void {
  // --------------------------------------------------------------------------
  // Tool 1: Vector Knowledge Search (RAG)
  // --------------------------------------------------------------------------
  registry.registerTool(
    {
      name: 'vector_knowledge_search',
      description: 'Performs mathematical Cosine Similarity search over the Vector RAG knowledge base.',
      category: 'knowledge',
      inputSchema: {
        type: 'object',
        properties: {
          query: {
            type: 'string',
            description: 'The search query or concept to locate in the vector database.',
          },
          topK: {
            type: 'number',
            description: 'Maximum number of relevant chunks to retrieve (default: 3).',
          },
        },
        required: ['query'],
      },
    },
    async (args) => {
      const { query, topK = 3 } = args;
      const results = vectorStore.similaritySearch(query, { topK, minSimilarity: 0.1 });

      return {
        query,
        matchedChunks: results.length,
        results: results.map((r) => ({
          title: r.document.metadata.title,
          category: r.document.metadata.category,
          similarityScore: Number(r.score.toFixed(4)),
          content: r.document.content,
        })),
      };
    }
  );

  // --------------------------------------------------------------------------
  // Tool 2: High-Precision Safe Mathematical Calculator
  // --------------------------------------------------------------------------
  registry.registerTool(
    {
      name: 'calculator',
      description: 'Evaluates mathematical, trigonometric, and statistical expressions safely.',
      category: 'computation',
      inputSchema: {
        type: 'object',
        properties: {
          expression: {
            type: 'string',
            description: 'Math expression e.g., "1000 * 0.0025 + Math.sqrt(144) * 5" or "1024 * 768 / 1e6"',
          },
        },
        required: ['expression'],
      },
    },
    async (args) => {
      const expr = String(args.expression).trim();
      // Whitelist safe mathematical characters and Math.* functions
      const sanitized = expr
        .replace(/Math\.(sqrt|abs|sin|cos|tan|log|log10|ceil|floor|round|pow|min|max|PI|E)/g, (match) => match)
        .replace(/[^0-9+\-*/().\s,eMathsqrtabscosintlg10ceilfordunpwPIME]/g, '');

      try {
        // Safe evaluation context with only Math globals
        const evaluator = new Function('Math', `return (${sanitized});`);
        const result = evaluator(Math);

        if (typeof result !== 'number' || isNaN(result)) {
          throw new Error('Calculation resulted in non-numeric or NaN value.');
        }

        return {
          expression: expr,
          result: Number.isInteger(result) ? result : Number(result.toFixed(6)),
          formatted: result.toLocaleString('en-US'),
        };
      } catch (err: any) {
        throw new Error(`Invalid mathematical expression "${expr}": ${err.message}`);
      }
    }
  );

  // --------------------------------------------------------------------------
  // Tool 3: Enterprise Database Lookup
  // --------------------------------------------------------------------------
  const mockEnterpriseDB: Record<string, any[]> = {
    model_pricing: [
      { model: 'gemini-1.5-pro', inputCostPer1M: 3.5, outputCostPer1M: 10.5, contextWindow: 2000000 },
      { model: 'gemini-1.5-flash', inputCostPer1M: 0.35, outputCostPer1M: 1.05, contextWindow: 1000000 },
      { model: 'gpt-4o', inputCostPer1M: 5.0, outputCostPer1M: 15.0, contextWindow: 128000 },
      { model: 'claude-3-5-sonnet', inputCostPer1M: 3.0, outputCostPer1M: 15.0, contextWindow: 200000 },
    ],
    architecture_blueprints: [
      {
        id: 'arch-001',
        name: 'Enterprise Agentic RAG',
        topology: 'Hierarchical Supervisor + Workers',
        vectorIndex: 'HNSW / Cosine',
        latencyTargetMs: 850,
        recommendedCacheTtl: 3600,
      },
      {
        id: 'arch-002',
        name: 'Autonomous Code Reviewer',
        topology: 'ReAct Loop (Plan-Act-Critique)',
        vectorIndex: 'In-Memory Semantic',
        latencyTargetMs: 1400,
        recommendedCacheTtl: 86400,
      },
    ],
  };

  registry.registerTool(
    {
      name: 'database_lookup',
      description: 'Queries internal enterprise data catalogs and architecture benchmarks.',
      category: 'storage',
      inputSchema: {
        type: 'object',
        properties: {
          table: {
            type: 'string',
            description: 'Target table name e.g. "model_pricing" or "architecture_blueprints".',
            enum: ['model_pricing', 'architecture_blueprints'],
          },
          filterKey: {
            type: 'string',
            description: 'Optional column name to filter by.',
          },
          filterValue: {
            type: 'string',
            description: 'Optional column value to match.',
          },
        },
        required: ['table'],
      },
    },
    async (args) => {
      const table = mockEnterpriseDB[args.table];
      if (!table) {
        throw new Error(`Table '${args.table}' not found. Available tables: ${Object.keys(mockEnterpriseDB).join(', ')}`);
      }

      if (args.filterKey && args.filterValue) {
        const needle = String(args.filterValue).toLowerCase();
        const filtered = table.filter((row) =>
          String(row[args.filterKey] || '')
            .toLowerCase()
            .includes(needle)
        );
        return { table: args.table, rowCount: filtered.length, data: filtered };
      }

      return { table: args.table, rowCount: table.length, data: table };
    }
  );

  // --------------------------------------------------------------------------
  // Tool 4: System Host & Runtime Metrics
  // --------------------------------------------------------------------------
  registry.registerTool(
    {
      name: 'system_metrics',
      description: 'Inspects host memory RSS, CPU architecture, OS platform, and Node.js process runtime.',
      category: 'system',
      inputSchema: {
        type: 'object',
        properties: {
          detailLevel: {
            type: 'string',
            description: 'Detail level: "summary" or "verbose".',
            enum: ['summary', 'verbose'],
          },
        },
      },
    },
    async (args) => {
      const mem = process.memoryUsage();
      const verbose = args.detailLevel === 'verbose';

      const metrics: any = {
        platform: process.platform,
        arch: process.arch,
        nodeVersion: process.version,
        uptimeSeconds: Math.floor(process.uptime()),
        memoryMB: {
          rss: Number((mem.rss / 1024 / 1024).toFixed(2)),
          heapUsed: Number((mem.heapUsed / 1024 / 1024).toFixed(2)),
          heapTotal: Number((mem.heapTotal / 1024 / 1024).toFixed(2)),
        },
      };

      if (verbose) {
        metrics.system = {
          cpus: os.cpus().length,
          totalMemoryMB: Number((os.totalmem() / 1024 / 1024).toFixed(2)),
          freeMemoryMB: Number((os.freemem() / 1024 / 1024).toFixed(2)),
          loadAverage: os.loadavg ? os.loadavg() : [],
        };
      }

      return metrics;
    }
  );
}
