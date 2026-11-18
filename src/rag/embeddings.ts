/**
 * Mathematical Vector & Embedding Engine
 * Implements deterministic high-dimensional vectorization, L2 Normalization,
 * and exact Cosine Similarity calculations for in-memory RAG.
 */

import { EmbeddingVector } from '../types/index.js';

export class VectorMath {
  /**
   * Calculates the exact dot product of two vectors: \sum(u_i * v_i)
   */
  public static dotProduct(u: EmbeddingVector, v: EmbeddingVector): number {
    if (u.length !== v.length) {
      throw new Error(`Vector dimension mismatch: ${u.length} vs ${v.length}`);
    }
    let sum = 0.0;
    for (let i = 0; i < u.length; i++) {
      sum += u[i] * v[i];
    }
    return sum;
  }

  /**
   * Computes the Euclidean norm (L2 magnitude) of a vector: \sqrt(\sum(u_i^2))
   */
  public static norm(v: EmbeddingVector): number {
    let sumSq = 0.0;
    for (let i = 0; i < v.length; i++) {
      sumSq += v[i] * v[i];
    }
    return Math.sqrt(sumSq);
  }

  /**
   * Normalizes a vector to unit length (L2 norm = 1.0)
   */
  public static normalize(v: EmbeddingVector): EmbeddingVector {
    const magnitude = this.norm(v);
    if (magnitude === 0.0) {
      return new Array(v.length).fill(0);
    }
    return v.map((val) => val / magnitude);
  }

  /**
   * Computes Cosine Similarity between two real vectors:
   * cos(theta) = (u . v) / (||u|| * ||v||)
   * Returns a value between -1.0 and 1.0 (clamped).
   */
  public static cosineSimilarity(u: EmbeddingVector, v: EmbeddingVector): number {
    if (u.length !== v.length) {
      throw new Error(`Dimension mismatch in cosine similarity: ${u.length} vs ${v.length}`);
    }
    const dot = this.dotProduct(u, v);
    const normU = this.norm(u);
    const normV = this.norm(v);

    if (normU === 0.0 || normV === 0.0) {
      return 0.0;
    }

    const similarity = dot / (normU * normV);
    // Float precision safety clamp [-1, 1]
    return Math.max(-1.0, Math.min(1.0, similarity));
  }

  /**
   * Calculates Euclidean distance between two vectors: \sqrt(\sum (u_i - v_i)^2)
   */
  public static euclideanDistance(u: EmbeddingVector, v: EmbeddingVector): number {
    if (u.length !== v.length) {
      throw new Error(`Dimension mismatch in euclidean distance: ${u.length} vs ${v.length}`);
    }
    let sum = 0.0;
    for (let i = 0; i < u.length; i++) {
      const diff = u[i] - v[i];
      sum += diff * diff;
    }
    return Math.sqrt(sum);
  }
}

/**
 * Deterministic Semantic Vectorizer (High-dimensional Dense Embedding Space)
 * Generates continuous dense vectors in R^D using token hashing, n-gram subword decomposition,
 * and inverse frequency weighting without requiring external external billable APIs.
 */
export class SemanticVectorizer {
  private static readonly DIMENSIONS = 128;

  // Curated semantic stop-words list for lexical noise suppression
  private static readonly STOP_WORDS = new Set([
    'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'it', 'this', 'that'
  ]);

  /**
   * Generates a normalized dense embedding vector for the given text.
   */
  public static generateEmbedding(text: string): EmbeddingVector {
    const vector = new Array(this.DIMENSIONS).fill(0.0);
    const sanitized = text.toLowerCase().replace(/[^a-z0-9\s_-]/g, ' ');
    const tokens = sanitized.split(/\s+/).filter((t) => t.length > 1 && !this.STOP_WORDS.has(t));

    if (tokens.length === 0) {
      // Empty input returns zero vector
      return vector;
    }

    // 1. Unigram & Bigram Feature Extraction with TF weighting
    for (let i = 0; i < tokens.length; i++) {
      const token = tokens[i];
      this.accumulateTokenHash(token, vector, 1.0);

      // Subword character trigrams for morphological and root similarity
      if (token.length >= 4) {
        for (let j = 0; j <= token.length - 3; j++) {
          const trigram = token.substring(j, j + 3);
          this.accumulateTokenHash(trigram, vector, 0.4);
        }
      }

      // Bigram contextual feature
      if (i < tokens.length - 1) {
        const bigram = `${token}_${tokens[i + 1]}`;
        this.accumulateTokenHash(bigram, vector, 1.5);
      }
    }

    // 2. Normalize vector to unit sphere S^{D-1}
    return VectorMath.normalize(vector);
  }

  /**
   * Hashes a token into the vector space using FNV-1a 32-bit hash algorithm
   * to distribute energy across multiple dimensions with sign preservation.
   */
  private static accumulateTokenHash(token: string, vector: number[], weight: number): void {
    let h1 = 0x811c9dc5;
    let h2 = 0x5bd1e995;

    for (let i = 0; i < token.length; i++) {
      const code = token.charCodeAt(i);
      h1 = Math.imul(h1 ^ code, 0x01000193);
      h2 = Math.imul(h2 ^ code, 0x5bd1e995);
    }

    const index1 = Math.abs(h1) % this.DIMENSIONS;
    const index2 = Math.abs(h2) % this.DIMENSIONS;
    const sign1 = (h1 & 0x1) === 0 ? 1.0 : -1.0;
    const sign2 = (h2 & 0x1) === 0 ? 1.0 : -1.0;

    vector[index1] += sign1 * weight;
    vector[index2] += sign2 * (weight * 0.7);
  }
}
