# Module 08: Enterprise Production Playbook & Hardening

## 1. High-Scale Deployment Architecture

For global enterprise deployments, the in-memory architecture transitions cleanly to a distributed cloud topology:

```
                  +---------------------------+
                  |  Cloud Load Balancer (L7) |
                  +-------------+-------------+
                                |
             +------------------+------------------+
             |                                     |
             v                                     v
+------------------------+             +------------------------+
| Express / SSE Node #1  |             | Express / SSE Node #2  |
+------------+-----------+             +------------+-----------+
             |                                      |
             +------------------+-------------------+
                                |
             +------------------v-------------------+
             |       Redis Pub/Sub State Bus        |
             |  - Cross-node SSE event broadcasting |
             |  - Distributed task locking          |
             +------------------+-------------------+
                                |
         +----------------------+----------------------+
         |                                             |
         v                                             v
+--------------------+                       +--------------------+
|  PostgreSQL / pgvector                     | Distributed Workers|
|  - Long-term session state                 | (Celery / BullMQ)  |
|  - Audit logs & Evals                      | - Async agent runs |
+--------------------+                       +--------------------+
```

---

## 2. Security Guardrails & Defense-in-Depth

1. **Prompt Injection & Jailbreak Defense**:
   - Implement regex and classifier filters before inputs reach the Planner.
   - Restrict MCP tools from executing arbitrary filesystem or shell commands; only register whitelisted mathematical or controlled storage queries.
2. **PII Masking & Data Loss Prevention**:
   - Redact credit card numbers, social security identifiers, and API keys at the API gateway layer before vectorization.
3. **Execution Timeouts & Rate Limiting**:
   - Hard 8-second execution caps on every MCP tool call.
   - Enforce IP and API token rate limiting via standard token bucket algorithms.

---

## 3. Observability & Tracing (OpenTelemetry)

In enterprise production:
- Export every `TraceEvent` to **OpenTelemetry (OTel)** collectors.
- Correlate spans using `sessionId` as the root trace ID.
- Monitor P95 / P99 latency, token burn rate, and Critic failure frequencies via Prometheus and Grafana dashboards.
