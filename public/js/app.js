/**
 * AgentFlow Studio Frontend Controller
 * Zero-Build Native Vanilla ES6 with EventSource SSE streaming,
 * visual topology animation, telemetry tracking, and RAG/MCP explorer.
 */

class AgentFlowApp {
  constructor() {
    this.sessionId = `sess_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    this.eventSource = null;
    this.traceCount = 0;

    this.initDOMElements();
    this.bindEvents();
    this.initSSEConnection();
    this.loadMCPTools();
    this.loadRAGDocuments();
    this.loadInterviewQuestions();
  }

  initDOMElements() {
    // Header & Status
    this.sseStatusBadge = document.getElementById('sseStatusBadge');
    this.activeSessionIdSpan = document.getElementById('activeSessionId');
    this.activeSessionIdSpan.textContent = this.sessionId;

    // Controls
    this.goalInput = document.getElementById('goalInput');
    this.runBtn = document.getElementById('runBtn');
    this.resetBtn = document.getElementById('resetBtn');
    this.presetBtns = document.querySelectorAll('.preset-btn');

    // Pipeline Nodes
    this.nodePlanner = document.getElementById('nodePlanner');
    this.nodeExecutor = document.getElementById('nodeExecutor');
    this.nodeCritic = document.getElementById('nodeCritic');
    this.nodeSynthesis = document.getElementById('nodeSynthesis');

    this.plannerStatus = document.getElementById('plannerStatus');
    this.executorStatus = document.getElementById('executorStatus');
    this.criticStatus = document.getElementById('criticStatus');
    this.synthesisStatus = document.getElementById('synthesisStatus');

    // Telemetry Metrics
    this.metricPromptTokens = document.getElementById('metricPromptTokens');
    this.metricCompletionTokens = document.getElementById('metricCompletionTokens');
    this.metricTotalTokens = document.getElementById('metricTotalTokens');
    this.metricCacheHits = document.getElementById('metricCacheHits');
    this.metricCost = document.getElementById('metricCost');
    this.metricLatency = document.getElementById('metricLatency');

    // Plan Card
    this.planSection = document.getElementById('planSection');
    this.planComplexity = document.getElementById('planComplexity');
    this.planRationale = document.getElementById('planRationale');
    this.planStepsContainer = document.getElementById('planStepsContainer');

    // Trace & Result
    this.traceContainer = document.getElementById('traceContainer');
    this.traceCountSpan = document.getElementById('traceCount');
    this.finalResultContainer = document.getElementById('finalResultContainer');
    this.criticScoreBadge = document.getElementById('criticScoreBadge');
    this.criticRiskBadge = document.getElementById('criticRiskBadge');

    // Tabs & Deep-dive components
    this.tabBtns = document.querySelectorAll('.tab-btn');
    this.tabContents = document.querySelectorAll('.tab-content');
    this.mcpToolsList = document.getElementById('mcpToolsList');
    this.mcpCountBadge = document.getElementById('mcpCountBadge');
    this.ragDocsList = document.getElementById('ragDocsList');
    this.ragCountBadge = document.getElementById('ragCountBadge');
    this.addDocBtn = document.getElementById('addDocBtn');
    this.ragDocTitle = document.getElementById('ragDocTitle');
    this.ragDocContent = document.getElementById('ragDocContent');
    this.interviewQuestionsList = document.getElementById('interviewQuestionsList');
  }

  bindEvents() {
    this.runBtn.addEventListener('click', () => this.handleRunWorkflow());
    this.resetBtn.addEventListener('click', () => this.handleReset());

    this.presetBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const preset = e.target.dataset.preset;
        this.applyPreset(preset);
      });
    });

    this.tabBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const tabId = e.target.dataset.tab;
        this.switchTab(tabId, e.target);
      });
    });

    this.addDocBtn.addEventListener('click', () => this.handleAddRAGDoc());
  }

  applyPreset(type) {
    if (type === 'cost') {
      this.goalInput.value = 'Calculate token pricing and monthly cost for 1,000,000 prompt tokens and 50,000 completion tokens under Gemini-1.5-Pro, and query pricing benchmarks.';
    } else if (type === 'rag') {
      this.goalInput.value = 'Explain the mathematical relationship between Cosine Similarity and Dot Product in vector retrieval, and search knowledge store for RAG standards.';
    } else if (type === 'mcp') {
      this.goalInput.value = 'Explain the Model Context Protocol (MCP) tool contract specification and verify active registered tools.';
    } else if (type === 'system') {
      this.goalInput.value = 'Inspect host runtime metrics, memory heap usage, platform architecture, and evaluate system stability.';
    }
  }

  switchTab(tabId, activeBtn) {
    this.tabBtns.forEach((b) => b.classList.remove('active'));
    this.tabContents.forEach((c) => c.classList.remove('active'));

    activeBtn.classList.add('active');
    const target = document.getElementById(tabId);
    if (target) target.classList.add('active');
  }

  // ==========================================================================
  // SSE Streaming Protocol Handler
  // ==========================================================================
  initSSEConnection() {
    if (this.eventSource) {
      this.eventSource.close();
    }

    const streamUrl = `/api/stream?sessionId=${encodeURIComponent(this.sessionId)}`;
    this.eventSource = new EventSource(streamUrl);

    this.eventSource.onopen = () => {
      this.updateSSEStatus(true);
    };

    this.eventSource.onerror = () => {
      this.updateSSEStatus(false);
    };

    // SSE Event Listeners
    this.eventSource.addEventListener('status', (e) => {
      const data = JSON.parse(e.data);
      this.handleStatusEvent(data);
    });

    this.eventSource.addEventListener('plan', (e) => {
      const plan = JSON.parse(e.data);
      this.renderPlan(plan);
    });

    this.eventSource.addEventListener('trace', (e) => {
      const traceEvent = JSON.parse(e.data);
      this.renderTraceEvent(traceEvent);
    });

    this.eventSource.addEventListener('telemetry', (e) => {
      const telemetry = JSON.parse(e.data);
      this.renderTelemetry(telemetry);
    });

    this.eventSource.addEventListener('result', (e) => {
      const result = JSON.parse(e.data);
      this.renderFinalResult(result);
    });

    this.eventSource.addEventListener('error', (e) => {
      const err = JSON.parse(e.data);
      this.renderError(err.message || 'Workflow execution error');
    });
  }

  updateSSEStatus(connected) {
    const dot = this.sseStatusBadge.querySelector('.status-dot');
    const label = this.sseStatusBadge.querySelector('.status-label');
    if (connected) {
      dot.className = 'status-dot connected';
      label.textContent = 'SSE Active';
    } else {
      dot.className = 'status-dot disconnected';
      label.textContent = 'Reconnecting...';
    }
  }

  handleStatusEvent(data) {
    const status = data.status;
    this.resetNodeHighlights();

    if (status === 'planning') {
      this.nodePlanner.classList.add('active');
      this.plannerStatus.textContent = 'Planning...';
    } else if (status === 'executing') {
      this.nodePlanner.classList.remove('active');
      this.nodePlanner.classList.add('completed');
      this.plannerStatus.textContent = 'Done';

      this.nodeExecutor.classList.add('active');
      this.executorStatus.textContent = 'Executing ReAct...';
    } else if (status === 'critiquing') {
      this.nodeExecutor.classList.remove('active');
      this.nodeExecutor.classList.add('completed');
      this.executorStatus.textContent = 'Done';

      this.nodeCritic.classList.add('active');
      this.criticStatus.textContent = 'Verifying...';
    } else if (status === 'completed') {
      this.nodeCritic.classList.remove('active');
      this.nodeCritic.classList.add('completed');
      this.criticStatus.textContent = 'Verified';

      this.nodeSynthesis.classList.add('completed');
      this.synthesisStatus.textContent = 'Complete';
      this.runBtn.disabled = false;
      this.runBtn.innerHTML = '<span class="btn-icon">▶</span> Run Workflow';
    }
  }

  resetNodeHighlights() {
    [this.nodePlanner, this.nodeExecutor, this.nodeCritic, this.nodeSynthesis].forEach((n) => {
      n.classList.remove('active', 'completed');
    });
    this.plannerStatus.textContent = 'Idle';
    this.executorStatus.textContent = 'Idle';
    this.criticStatus.textContent = 'Idle';
    this.synthesisStatus.textContent = 'Idle';
  }

  // ==========================================================================
  // Workflow Execution Dispatcher
  // ==========================================================================
  async handleRunWorkflow() {
    const goal = this.goalInput.value.trim();
    if (!goal) {
      alert('Please specify an architectural goal or prompt.');
      return;
    }

    this.runBtn.disabled = true;
    this.runBtn.innerHTML = '<span class="btn-icon">⏳</span> Orchestrating Agents...';

    // Clear trace and results
    this.traceContainer.innerHTML = '';
    this.traceCount = 0;
    this.traceCountSpan.textContent = '0 events';
    this.finalResultContainer.innerHTML = '<div class="empty-state"><span class="empty-icon">⚙️</span><p>Agents active: streaming ReAct trace...</p></div>';
    this.criticScoreBadge.textContent = 'Score: --';
    this.criticRiskBadge.textContent = 'Risk: --';

    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goal, sessionId: this.sessionId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Execution failed');
      }
    } catch (err) {
      this.renderError(err.message);
      this.runBtn.disabled = false;
      this.runBtn.innerHTML = '<span class="btn-icon">▶</span> Run Workflow';
    }
  }

  handleReset() {
    this.goalInput.value = '';
    this.planSection.style.display = 'none';
    this.traceContainer.innerHTML = '<div class="empty-state"><span class="empty-icon">⏳</span><p>Ready. Enter a goal and run the multi-agent workflow.</p></div>';
    this.finalResultContainer.innerHTML = '<div class="empty-state"><span class="empty-icon">🎯</span><p>Final verified output will render here.</p></div>';
    this.resetNodeHighlights();
    this.renderTelemetry({
      promptTokens: 0,
      completionTokens: 0,
      totalTokens: 0,
      cacheHitTokens: 0,
      estimatedCostUSD: 0,
      totalLatencyMs: 0,
    });
  }

  // ==========================================================================
  // Renderers: Plan, Trace, Telemetry, and Results
  // ==========================================================================
  renderPlan(plan) {
    this.planSection.style.display = 'block';
    this.planComplexity.textContent = `Complexity: ${plan.estimatedComplexity.toUpperCase()}`;
    this.planRationale.textContent = plan.strategyRationale;

    this.planStepsContainer.innerHTML = plan.steps
      .map(
        (step) => `
      <div class="plan-step-box ${step.status}" id="plan-step-${step.id}">
        <div class="step-order">Step ${step.order} [${step.status.toUpperCase()}]</div>
        <div class="step-desc">${this.escapeHTML(step.description)}</div>
        <div class="step-tool">Tool: ${step.toolToUse || 'None (Internal Reasoning)'}</div>
      </div>
    `
      )
      .join('');
  }

  renderTraceEvent(event) {
    this.traceCount++;
    this.traceCountSpan.textContent = `${this.traceCount} events`;

    const item = document.createElement('div');
    item.className = `trace-item ${event.type}`;

    let payloadHTML = '';
    if (event.payload) {
      payloadHTML = `<pre class="trace-payload">${this.escapeHTML(JSON.stringify(event.payload, null, 2))}</pre>`;
    }

    const timeStr = new Date(event.timestamp).toLocaleTimeString();
    const durationStr = event.durationMs ? ` (${event.durationMs.toFixed(1)}ms)` : '';

    item.innerHTML = `
      <div class="trace-meta">
        <span>[${event.node.toUpperCase()}] ${event.type}</span>
        <span>${timeStr}${durationStr}</span>
      </div>
      <div class="trace-title"><strong>${this.escapeHTML(event.title)}</strong></div>
      ${payloadHTML}
    `;

    this.traceContainer.appendChild(item);
    this.traceContainer.scrollTop = this.traceContainer.scrollHeight;
  }

  renderTelemetry(telemetry) {
    this.metricPromptTokens.textContent = telemetry.promptTokens.toLocaleString();
    this.metricCompletionTokens.textContent = telemetry.completionTokens.toLocaleString();
    this.metricTotalTokens.textContent = telemetry.totalTokens.toLocaleString();
    this.metricCacheHits.textContent = telemetry.cacheHitTokens.toLocaleString();
    this.metricCost.textContent = `$${telemetry.estimatedCostUSD.toFixed(6)}`;
    this.metricLatency.textContent = `${Math.round(telemetry.totalLatencyMs)} ms`;
  }

  renderFinalResult(result) {
    if (result.critique) {
      this.criticScoreBadge.textContent = `Score: ${result.critique.score}/100`;
      this.criticRiskBadge.textContent = `Risk: ${result.critique.hallucinationRisk.toUpperCase()}`;
    }

    // Convert simple markdown headings & lists to styled HTML
    let formattedText = this.escapeHTML(result.finalAnswer)
      .replace(/### (.*?)\n/g, '<h3>$1</h3>')
      .replace(/#### (.*?)\n/g, '<h4>$1</h4>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n- (.*?)(?=\n|$)/g, '<li>$1</li>')
      .replace(/\n\n/g, '<br/><br/>');

    this.finalResultContainer.innerHTML = formattedText;
  }

  renderError(msg) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'trace-item';
    errorDiv.style.borderLeft = '3px solid #f43f5e';
    errorDiv.innerHTML = `
      <div class="trace-meta">
        <span style="color: #f43f5e;">[ERROR] System Exception</span>
      </div>
      <div>${this.escapeHTML(msg)}</div>
    `;
    this.traceContainer.appendChild(errorDiv);
  }

  // ==========================================================================
  // Catalog Loaders: MCP Tools, Vector RAG Documents, and Interview Vault
  // ==========================================================================
  async loadMCPTools() {
    try {
      const res = await fetch('/api/tools');
      const data = await res.json();
      this.mcpCountBadge.textContent = data.count;

      this.mcpToolsList.innerHTML = data.tools
        .map(
          (t) => `
        <div class="tool-item">
          <h5>${this.escapeHTML(t.name)}</h5>
          <p>${this.escapeHTML(t.description)}</p>
        </div>
      `
        )
        .join('');
    } catch (err) {
      console.error('Failed to load MCP tools:', err);
    }
  }

  async loadRAGDocuments() {
    try {
      const res = await fetch('/api/rag/documents');
      const data = await res.json();
      this.ragCountBadge.textContent = data.count;

      this.ragDocsList.innerHTML = data.documents
        .map(
          (d) => `
        <div class="rag-item">
          <h5>${this.escapeHTML(d.title)} [${d.category}]</h5>
          <p>${this.escapeHTML(d.contentPreview)}</p>
        </div>
      `
        )
        .join('');
    } catch (err) {
      console.error('Failed to load RAG docs:', err);
    }
  }

  async handleAddRAGDoc() {
    const title = this.ragDocTitle.value.trim();
    const content = this.ragDocContent.value.trim();
    if (!content) {
      alert('Document content cannot be empty.');
      return;
    }

    try {
      const res = await fetch('/api/rag/documents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content, category: 'custom_notes' }),
      });

      if (res.ok) {
        this.ragDocTitle.value = '';
        this.ragDocContent.value = '';
        await this.loadRAGDocuments();
      }
    } catch (err) {
      alert('Error indexing document: ' + err.message);
    }
  }

  async loadInterviewQuestions() {
    try {
      const res = await fetch('/api/interview-qa');
      const data = await res.json();

      let html = '';
      data.sections.forEach((sec) => {
        html += `<h4 style="font-size: 0.8rem; color: #38bdf8; margin: 10px 0 6px 0;">${this.escapeHTML(sec.category)}</h4>`;
        sec.questions.forEach((item) => {
          html += `
            <div class="qa-card">
              <div class="qa-question" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                <span>${this.escapeHTML(item.q)}</span>
                <span>▾</span>
              </div>
              <div class="qa-answer" style="display: none;">
                ${this.escapeHTML(item.a)}
              </div>
            </div>
          `;
        });
      });

      this.interviewQuestionsList.innerHTML = html;
    } catch (err) {
      console.error('Failed to load interview Q&A:', err);
    }
  }

  escapeHTML(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

// Initialize Application on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  window.agentFlowApp = new AgentFlowApp();
});
