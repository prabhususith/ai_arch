/**
 * Multi-Agent Orchestration Engine
 * State machine managing Planner, Executor, and Critic lifecycle with real-time trace events.
 */

import { EventEmitter } from 'events';
import { AgentState, TraceEvent, TokenTelemetry } from '../types/index.js';
import { MCPRegistry } from '../mcp/registry.js';
import { VectorStore } from '../rag/vector-store.js';
import { PlannerAgent } from './agents/planner.js';
import { ExecutorAgent, StepExecutionResult } from './agents/executor.js';
import { CriticAgent } from './agents/critic.js';
import { TokenCounter } from '../telemetry/token-counter.js';

export class OrchestrationEngine extends EventEmitter {
  private planner: PlannerAgent;
  private executor: ExecutorAgent;
  private critic: CriticAgent;

  constructor(private mcpRegistry: MCPRegistry, private vectorStore: VectorStore) {
    super();
    this.planner = new PlannerAgent();
    this.executor = new ExecutorAgent(this.mcpRegistry);
    this.critic = new CriticAgent();
  }

  /**
   * Executes a multi-agent workflow for a given user goal.
   */
  public async runWorkflow(goal: string, sessionId: string = `sess_${Date.now()}`): Promise<AgentState> {
    const startTime = performance.now();
    let telemetry: TokenTelemetry = TokenCounter.createTelemetry();
    const trace: TraceEvent[] = [];
    const stepResults = new Map<string, StepExecutionResult>();
    const priorObservations = new Map<string, string>();

    const emitTrace = (event: Omit<TraceEvent, 'id' | 'timestamp'>) => {
      const fullEvent: TraceEvent = {
        ...event,
        id: `tr_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`,
        timestamp: Date.now(),
      };
      trace.push(fullEvent);
      this.emit('trace', fullEvent);
    };

    const updateTelemetry = (promptText: string, completionText: string, latencyMs: number) => {
      telemetry = TokenCounter.recordUsage(telemetry, promptText, completionText, latencyMs);
      this.emit('telemetry', telemetry);
    };

    // Initialize Agent State
    const state: AgentState = {
      sessionId,
      goal,
      plan: null,
      currentStepIndex: 0,
      memory: [{ role: 'user', content: goal, timestamp: Date.now() }],
      trace,
      critiqueHistory: [],
      finalAnswer: null,
      status: 'planning',
      telemetry,
    };

    this.emit('status', { status: 'planning', message: 'Planner analyzing intent and decomposing goal into DAG...' });

    // ------------------------------------------------------------------------
    // Stage 1: Planning
    // ------------------------------------------------------------------------
    const planStartTime = performance.now();
    const availableTools = this.mcpRegistry.listTools();
    const plan = await this.planner.createPlan(goal, availableTools);
    state.plan = plan;
    const planDuration = performance.now() - planStartTime;

    updateTelemetry(`System Prompt + Available Tools (${availableTools.length}) + Goal: ${goal}`, JSON.stringify(plan), planDuration);

    emitTrace({
      node: 'planner',
      type: 'plan_created',
      title: `Plan generated (${plan.steps.length} steps)`,
      payload: plan,
      durationMs: planDuration,
    });
    this.emit('plan', plan);

    // ------------------------------------------------------------------------
    // Stage 2: ReAct Execution Loop
    // ------------------------------------------------------------------------
    state.status = 'executing';
    this.emit('status', { status: 'executing', message: 'Executor processing ReAct steps...' });

    let retryCount = 0;
    let executeNextSteps = async (stepsToRun: typeof plan.steps) => {
      for (let i = 0; i < stepsToRun.length; i++) {
        const step = stepsToRun[i];
        state.currentStepIndex = step.order;
        step.status = 'in_progress';

        emitTrace({
          node: 'executor',
          stepId: step.id,
          type: 'step_start',
          title: `Starting Step ${step.order}: ${step.description}`,
          payload: { step },
        });

        // Executor ReAct execution
        const stepStartTime = performance.now();
        const execResult = await this.executor.executeStep(step, priorObservations, goal);
        const stepDuration = performance.now() - stepStartTime;

        stepResults.set(step.id, execResult);
        priorObservations.set(step.id, execResult.observationSummary);

        // Update step status
        step.status = execResult.toolResult.isError ? 'failed' : 'completed';
        step.output = execResult.observationSummary;

        // Trace Thought
        emitTrace({
          node: 'executor',
          stepId: step.id,
          type: 'thought',
          title: `Reasoning for Step ${step.order}`,
          payload: { thought: execResult.thought },
        });

        // Trace Action
        emitTrace({
          node: 'executor',
          stepId: step.id,
          type: 'action_call',
          title: `Action: Invoke ${execResult.toolCall.name}`,
          payload: { toolCall: execResult.toolCall },
        });

        // Trace Observation
        emitTrace({
          node: 'executor',
          stepId: step.id,
          type: 'observation',
          title: `Observation from ${execResult.toolCall.name}`,
          payload: {
            isError: execResult.toolResult.isError,
            content: execResult.toolResult.content,
            durationMs: execResult.toolResult.executionTimeMs,
          },
          durationMs: stepDuration,
        });

        updateTelemetry(execResult.thought, JSON.stringify(execResult.toolResult), stepDuration);
      }
    };

    await executeNextSteps(plan.steps);

    // ------------------------------------------------------------------------
    // Stage 3: Critic Evaluation & Self-Correction
    // ------------------------------------------------------------------------
    state.status = 'critiquing';
    this.emit('status', { status: 'critiquing', message: 'Critic validating evidence, coverage, and hallucination risk...' });

    const criticStartTime = performance.now();
    let critique = await this.critic.evaluate(goal, plan, stepResults, retryCount);
    const criticDuration = performance.now() - criticStartTime;

    state.critiqueHistory.push(critique);

    emitTrace({
      node: 'critic',
      type: 'critique',
      title: `Critique: Quality Score ${critique.score}/100 (${critique.passed ? 'PASSED' : 'REVISION NEEDED'})`,
      payload: critique,
      durationMs: criticDuration,
    });

    updateTelemetry(JSON.stringify(Array.from(stepResults.values())), JSON.stringify(critique), criticDuration);

    // Self-correction loop if Critic requires revision
    if (critique.shouldRetry && critique.suggestedRevision) {
      retryCount++;
      emitTrace({
        node: 'planner',
        type: 'plan_revised',
        title: `Self-Correction Triggered: Revising Plan`,
        payload: { feedback: critique.suggestedRevision },
      });

      const revisedPlan = await this.planner.revisePlan(plan, critique.suggestedRevision);
      state.plan = revisedPlan;
      this.emit('plan', revisedPlan);

      // Execute only the newly appended step
      const newSteps = revisedPlan.steps.slice(plan.steps.length);
      await executeNextSteps(newSteps);

      // Re-evaluate
      critique = await this.critic.evaluate(goal, revisedPlan, stepResults, retryCount);
      state.critiqueHistory.push(critique);
    }

    // ------------------------------------------------------------------------
    // Stage 4: Synthesis & Final Answer
    // ------------------------------------------------------------------------
    const finalAnswer = this.critic.synthesizeFinalAnswer(goal, stepResults, critique);
    state.finalAnswer = finalAnswer;
    state.status = 'completed';
    state.telemetry = telemetry;

    emitTrace({
      node: 'critic',
      type: 'final_answer',
      title: 'Synthesized Solution & Verification Report',
      payload: { finalAnswer },
      durationMs: performance.now() - startTime,
    });

    this.emit('result', {
      finalAnswer,
      critique,
      telemetry,
      totalDurationMs: performance.now() - startTime,
    });

    this.emit('status', { status: 'completed', message: 'Workflow finished successfully.' });

    return state;
  }
}
