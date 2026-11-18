# Module 06: Tokenomics & Cost Optimization Strategies

## 1. Token Estimation Mechanics

Accurate real-time cost telemetry requires token estimation before and after model inference. 

AgentFlow Studio implements a blended subword heuristic:
- **Character Splitting**: English prose averages 3.8 to 4.0 characters per token.
- **Word Factorization**: Standard punctuation and whitespace boundaries average 1.3 subword tokens per word.
- **Formula**:
  $$\text{Tokens} \approx \text{round}\left( 0.7 \times \left\lceil \frac{\text{Length}}{3.8} \right\rceil + 0.3 \times \left\lceil \text{Words} \times 1.3 \right\rceil \right)$$

---

## 2. KV-Cache Prefix Alignment & Prompt Caching

Modern foundation model providers (e.g., Google Gemini, Anthropic Claude) offer **Prompt Caching**, discounting input tokens by up to 50% - 80% if the prompt shares an exact identical prefix with recent requests.

### Optimization Principles for Multi-Agent Workflows:
1. **Static System Directives First**: Place unchanging agent persona instructions and MCP tool schemas at the very top of the context window.
2. **Deterministic Tool Schema Serialization**: Sort JSON Schema properties alphabetically to avoid false cache invalidations.
3. **Dynamic Context at the Tail**: Append variable user inputs and recent observations strictly at the end.

---

## 3. Financial Cost Calculation Model

```typescript
const promptCost = (effectivePromptTokens / 1000) * model.promptPricePer1K;
const cachedCost = (cacheTokens / 1000) * (model.promptPricePer1K * 0.5);
const completionCost = (completionTokens / 1000) * model.completionPricePer1K;
const totalCost = promptCost + cachedCost + completionCost;
```

### Enterprise Model Routing Strategy
- **High-Complexity Planning & Critique**: Route to Gemini-1.5-Pro / Claude-3.5-Sonnet (higher per-token cost, high reasoning fidelity).
- **Repetitive Tool Execution**: Route to Gemini-1.5-Flash / GPT-4o-Mini (10x lower cost, low latency).
