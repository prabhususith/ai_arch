# Module 04: Vector RAG & Mathematical Cosine Similarity

## 1. Mathematical Foundations of Cosine Similarity

Cosine similarity evaluates the cosine of the angle $\theta$ between two vectors in a high-dimensional inner product space:

$$\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} = \frac{\sum_{i=1}^n u_i v_i}{\sqrt{\sum_{i=1}^n u_i^2} \sqrt{\sum_{i=1}^n v_i^2}}$$

### Boundary Properties:
- $\cos(\theta) = 1.0$: Identical direction (maximal semantic correlation).
- $\cos(\theta) = 0.0$: Orthogonal vectors (zero correlation).
- $\cos(\theta) = -1.0$: Diametrically opposite vectors.

---

## 2. Hardware Optimization: L2 Unit Normalization

Computing the denominator $\sqrt{\sum u_i^2} \sqrt{\sum v_i^2}$ requires two square root operations and multiple floating point multiplications per comparison, which becomes a bottleneck during nearest-neighbor sweeps.

**Optimization**: Normalize all vectors to unit length $\|\mathbf{u}\| = 1.0$ at indexing time:

$$\|\mathbf{u}\| = \sqrt{\sum_{i=1}^n u_i^2} = 1.0 \implies \cos(\theta) = \mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^n u_i v_i$$

By performing L2 normalization upon document ingestion, nearest neighbor similarity collapses into a **single dot product**, enabling vector search engines to exploit hardware SIMD/AVX registers.

---

## 3. High-Dimensional Semantic Vectorizer Architecture

In AgentFlow Studio, the `SemanticVectorizer` operates over a $D=128$ dimensional dense space:

1. **Stop-word Noise Reduction**: Strips high-frequency lexical stop words.
2. **Subword N-gram Feature Hashing**: Generates character trigrams for subword morphology matching (e.g., "comput-ation", "comput-er", "comput-ing").
3. **Bigram Extraction**: Accumulates adjacent word pairs to preserve local word order context.
4. **FNV-1a 32-bit Dual Hashing**: Disperses energy across positive and negative vector coordinates to eliminate hash collisions.
5. **L2 Unit Sphere Projection**: Projects the accumulated vector onto unit hypersphere $S^{D-1}$.

---

## 4. Vector Indexing Trade-Offs: HNSW vs IVFFlat

| Dimension | Exact k-NN (Flat) | IVFFlat (Inverted File) | HNSW (Hierarchical Navigable Small World) |
| :--- | :--- | :--- | :--- |
| **Recall Rate** | 100% (Exact) | 85% - 95% | > 98% |
| **Query Latency** | $O(N \cdot D)$ (Linear) | $O(\frac{N}{K} \cdot D)$ | $O(\log N \cdot D)$ (Logarithmic) |
| **Index Build Time** | Zero | Fast | Moderate to High |
| **RAM Overhead** | Minimal (Raw Vectors) | Minimal + Centroids | High (Graph edges: 2-4x vector size) |
| **Best Used In** | Small to Medium (< 100k) | High-volume storage-constrained | Real-time, mission-critical RAG |
