# Module 05: Streaming SSE Telemetry & Transport Protocols

## 1. Why Server-Sent Events (SSE) for AI Workflows?

Modern AI user experiences require real-time streaming of intermediate reasoning thoughts, tool calls, and token generation.

### SSE vs WebSockets vs Long Polling

| Criterion | Server-Sent Events (SSE) | WebSockets (WS) | Long Polling |
| :--- | :--- | :--- | :--- |
| **Directionality** | Unidirectional (Server $\rightarrow$ Client) | Bidirectional (Full Duplex) | Request-Response Simulation |
| **Protocol** | Standard HTTP/1.1 or HTTP/2 | Custom `ws://` / `wss://` | Standard HTTP |
| **Proxy / Firewall Traversal** | Seamless (Standard HTTP) | Often blocked or throttled | Seamless |
| **Connection Recovery** | Native `Last-Event-ID` auto-reconnect | Requires custom client code | Manual reconnect logic |
| **Overhead** | Minimal headers | Protocol upgrade handshake | High HTTP header overhead |

**Verdict**: Because agent execution and telemetry updates flow unidirectionally from the server orchestrator to the client UI, **SSE is the optimal architectural fit**.

---

## 2. The SSE Protocol Contract

SSE relies on the MIME type `text/event-stream`. Each event is formatted as a text block terminated by a double newline:

```http
event: status
data: {"status":"planning","message":"Decomposing goal..."}

event: trace
data: {"id":"tr_1","node":"executor","type":"thought","title":"Reasoning..."}

event: telemetry
data: {"promptTokens":120,"completionTokens":45,"estimatedCostUSD":0.00089}
```

### Server Configuration Directives:
```typescript
res.setHeader('Content-Type', 'text/event-stream');
res.setHeader('Cache-Control', 'no-cache');
res.setHeader('Connection', 'keep-alive');
res.setHeader('X-Accel-Buffering', 'no'); // Disables Nginx buffering
```

---

## 3. Client Consumption via Native `EventSource`

The browser connects without external dependencies:

```javascript
const eventSource = new EventSource(`/api/stream?sessionId=${sessionId}`);

eventSource.addEventListener('trace', (e) => {
  const traceEvent = JSON.parse(e.data);
  updateTraceUI(traceEvent);
});

eventSource.addEventListener('telemetry', (e) => {
  const metrics = JSON.parse(e.data);
  updateMetricsRibbon(metrics);
});
```
