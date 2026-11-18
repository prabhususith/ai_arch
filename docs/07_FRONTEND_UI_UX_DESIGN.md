# Module 07: Zero-Build Vanilla Frontend Architecture

## 1. Zero-Build Design Philosophy

Modern web development frequently suffers from excessive build tooling complexity (Webpack, Rollup, Vite, Next.js, hundreds of NPM sub-dependencies).

**AgentFlow Studio** adheres to the **Zero-Build Native Principle**:
1. **Zero Transpilation Overhead**: Written in standard ES6 JavaScript, HTML5, and CSS3 natively understood by all modern browsers.
2. **Instant Hot Reloading**: Static files are served directly by Express without bundler wait times.
3. **Micro-Footprint**: Zero front-end NPM dependencies, eliminating supply-chain attack vectors.

---

## 2. Component Layout & Visual Hierarchy

The GUI is structured as a dual-pane responsive command center:

1. **Header**: Live SSE connection status dot (green/red) and active UUID session monitor.
2. **Left Sidebar**:
   - Orchestration control form with multi-line prompt input.
   - Quick architectural presets (Token Cost, Vector RAG, MCP Tools, System Metrics).
   - Deep-dive drawer tabs: MCP Tools catalog, Vector Knowledge Base with on-the-fly document indexer, and AI Architect Interview Q&A.
3. **Workspace Canvas**:
   - **Topology Track**: Visual pipeline showing Planner $\rightarrow$ Executor $\rightarrow$ Critic $\rightarrow$ Synthesizer nodes with glowing status animations.
   - **Telemetry Ribbon**: High-visibility real-time counters for prompt tokens, completion tokens, total tokens, cache hits, dollar cost, and latency.
   - **Plan DAG Container**: Real-time rendering of generated sub-steps.
   - **Live ReAct Trace Inspector**: Color-coded collapsible cards (Purple = Thought, Blue = Action, Cyan = Observation, Amber = Critique).
   - **Verified Output Card**: Final structured architectural verdict with verification score and risk indicator.
