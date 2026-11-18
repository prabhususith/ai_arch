/**
 * In-Memory Vector RAG Store
 * Implements document indexing, sliding-window chunking, and mathematical
 * Cosine Similarity nearest-neighbor search.
 */

import { VectorDocument, VectorDocumentMetadata, VectorSearchResult, RAGSearchOptions } from '../types/index.js';
import { SemanticVectorizer, VectorMath } from './embeddings.js';

export class VectorStore {
  private documents: Map<string, VectorDocument> = new Map();

  constructor() {
    this.seedDefaultKnowledge();
  }

  /**
   * Adds a single document or chunk into the vector store.
   */
  public addDocument(content: string, metadata: Partial<VectorDocumentMetadata> = {}): VectorDocument {
    const id = `doc_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    const embedding = SemanticVectorizer.generateEmbedding(content);

    const doc: VectorDocument = {
      id,
      content,
      embedding,
      metadata: {
        source: metadata.source || 'manual_entry',
        category: metadata.category || 'general',
        title: metadata.title || 'Untitled Knowledge Node',
        chunkIndex: metadata.chunkIndex ?? 0,
        tags: metadata.tags || [],
        createdAt: metadata.createdAt || Date.now(),
      },
    };

    this.documents.set(id, doc);
    return doc;
  }

  /**
   * Chunks large text into sliding windows and adds all chunks.
   */
  public addDocumentWithChunking(
    content: string,
    metadata: Partial<VectorDocumentMetadata> = {},
    chunkSize: number = 300,
    chunkOverlap: number = 50
  ): VectorDocument[] {
    const words = content.split(/\s+/);
    if (words.length <= chunkSize) {
      return [this.addDocument(content, metadata)];
    }

    const createdDocs: VectorDocument[] = [];
    let chunkIndex = 0;
    let startIndex = 0;

    while (startIndex < words.length) {
      const chunkWords = words.slice(startIndex, startIndex + chunkSize);
      const chunkContent = chunkWords.join(' ');

      const doc = this.addDocument(chunkContent, {
        ...metadata,
        title: `${metadata.title || 'Document'} (Chunk #${chunkIndex + 1})`,
        chunkIndex,
      });

      createdDocs.push(doc);
      chunkIndex++;
      startIndex += chunkSize - chunkOverlap;
    }

    return createdDocs;
  }

  /**
   * Executes mathematical Cosine Similarity search over all indexed vectors.
   */
  public similaritySearch(query: string, options: RAGSearchOptions = {}): VectorSearchResult[] {
    const topK = options.topK ?? 4;
    const minSimilarity = options.minSimilarity ?? 0.15;
    const filterCategory = options.filterCategory;

    const queryVector = SemanticVectorizer.generateEmbedding(query);
    const results: VectorSearchResult[] = [];

    for (const doc of this.documents.values()) {
      if (filterCategory && doc.metadata.category !== filterCategory) {
        continue;
      }

      const score = VectorMath.cosineSimilarity(queryVector, doc.embedding);
      if (score >= minSimilarity) {
        results.push({ document: doc, score });
      }
    }

    // Sort descending by cosine similarity score
    results.sort((a, b) => b.score - a.score);

    return results.slice(0, topK);
  }

  /**
   * Retrieves all documents in the store.
   */
  public getAllDocuments(): VectorDocument[] {
    return Array.from(this.documents.values());
  }

  /**
   * Removes a document by ID.
   */
  public deleteDocument(id: string): boolean {
    return this.documents.delete(id);
  }

  /**
   * Clears the store.
   */
  public clear(): void {
    this.documents.clear();
  }

  /**
   * Returns vector store statistics.
   */
  public getStats() {
    return {
      documentCount: this.documents.size,
      vectorDimension: 128,
      categories: Array.from(new Set(Array.from(this.documents.values()).map((d) => d.metadata.category))),
    };
  }

  /**
   * Seeds enterprise architectural knowledge base for realistic ReAct retrieval.
   */
  private seedDefaultKnowledge(): void {
    const seedCorpus = [
      {
        title: 'Multi-Agent ReAct Architecture',
        category: 'architecture',
        content: `The ReAct (Reasoning and Acting) paradigm coordinates LLMs by interleaving Thought, Action, and Observation cycles. In enterprise systems, decoupling the Planner (DAG task decomposition), Executor (tool execution loop), and Critic (evaluation and verification) prevents hallucination cascades and ensures deterministic tool invocation.`,
      },
      {
        title: 'Model Context Protocol (MCP) Standards',
        category: 'mcp',
        content: `The Model Context Protocol (MCP) is an open architectural standard designed by Anthropic and enterprise partners that exposes tools, prompts, and resources to foundation models via standardized JSON-RPC contracts. MCP enforces strict input schemas, capability negotiation, and secure isolation between execution nodes and host environments.`,
      },
      {
        title: 'Vector Search and Cosine Similarity Mathematics',
        category: 'rag',
        content: `Cosine similarity measures the cosine of the angle between two multi-dimensional vectors: cos(theta) = (u . v) / (||u|| * ||v||). In dense vector retrieval, normalizing embeddings to unit length L2=1 transforms cosine distance into a simple dot product, dramatically accelerating approximate nearest neighbor (ANN) searches such as HNSW and ScaNN.`,
      },
      {
        title: 'Server-Sent Events (SSE) vs WebSockets in AI Streaming',
        category: 'streaming',
        content: `Server-Sent Events (SSE) provide lightweight, unidirectional text streaming over HTTP/1.1 or HTTP/2 without WebSocket handshake overhead. SSE automatically supports HTTP proxies, TLS termination, built-in reconnection protocols (Last-Event-ID), and lower infrastructure complexity for token-by-token LLM output and ReAct trace telemetry.`,
      },
      {
        title: 'Token Economics and Cache Optimization',
        category: 'tokenomics',
        content: `Token optimization in multi-agent workflows hinges on prompt compression, KV-cache prefix alignment, and selective history compaction. Shared system prompts placed at the top of context windows maximize provider prompt-caching hit rates, reducing inference latency by up to 80% and cost by 50%.`,
      },
      {
        title: 'Critic Node and Self-Correction Guarantees',
        category: 'orchestration',
        content: `A dedicated Critic node performs hallucination detection, schema conformance verification, and requirement coverage scoring before responses are returned to users. If the confidence score drops below 75%, the Critic triggers an iterative self-correction loop, instructing the Planner or Executor to refine the response.`,
      },
    ];

    for (const item of seedCorpus) {
      this.addDocument(item.content, {
        title: item.title,
        category: item.category,
        source: 'built_in_seed',
        tags: [item.category, 'architecture'],
      });
    }
  }
}
