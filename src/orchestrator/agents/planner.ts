/**
 * Planner Agent Node
 * Decomposes high-level user inquiries into a dependency-ordered Execution Plan (DAG).
 */

import { ExecutionPlan, PlanStep, MCPToolDefinition } from '../../types/index.js';

export class PlannerAgent {
  /**
   * Generates a concrete execution plan based on the goal and registered MCP tools.
   */
  public async createPlan(goal: string, availableTools: MCPToolDefinition[]): Promise<ExecutionPlan> {
    const planId = `plan_${Date.now()}`;
    const lowerGoal = goal.toLowerCase();

    const toolNames = availableTools.map((t) => t.name);
    const steps: PlanStep[] = [];

    // Analyze intent to construct intelligent execution DAG
    const requiresMath = /calculate|math|cost|latency|sum|pricing|tokens|estimate|how much/i.test(lowerGoal);
    const requiresKnowledge = /what is|how to|architecture|explain|mcp|rag|cosine|react|sse|design/i.test(lowerGoal);
    const requiresSystem = /system|memory|cpu|node|runtime|os|platform|specs/i.test(lowerGoal);
    const requiresDatabase = /database|table|pricing|blueprint|catalog|benchmark/i.test(lowerGoal);

    let stepCounter = 1;

    // Step 1: Context & Knowledge Gathering
    if (requiresKnowledge || (!requiresMath && !requiresSystem && !requiresDatabase)) {
      steps.push({
        id: `step_${stepCounter}`,
        order: stepCounter,
        description: `Retrieve architectural ground-truth and semantic documentation via In-Memory Vector RAG.`,
        toolToUse: toolNames.includes('vector_knowledge_search') ? 'vector_knowledge_search' : undefined,
        toolArgsHint: { query: goal, topK: 3 },
        dependencies: [],
        status: 'pending',
      });
      stepCounter++;
    }

    // Step 2: Database / Benchmark Query (if applicable)
    if (requiresDatabase || requiresMath) {
      const table = lowerGoal.includes('pricing') || lowerGoal.includes('cost') ? 'model_pricing' : 'architecture_blueprints';
      steps.push({
        id: `step_${stepCounter}`,
        order: stepCounter,
        description: `Query enterprise database catalog for benchmark tables and pricing rates.`,
        toolToUse: toolNames.includes('database_lookup') ? 'database_lookup' : undefined,
        toolArgsHint: { table },
        dependencies: steps.length > 0 ? [steps[steps.length - 1].id] : [],
        status: 'pending',
      });
      stepCounter++;
    }

    // Step 3: Precise Computation / Calculation (if applicable)
    if (requiresMath) {
      steps.push({
        id: `step_${stepCounter}`,
        order: stepCounter,
        description: `Execute high-precision mathematical evaluation using the MCP Calculator tool.`,
        toolToUse: toolNames.includes('calculator') ? 'calculator' : undefined,
        toolArgsHint: { expression: '1000 * 0.0035 + 200 * 0.0105' },
        dependencies: steps.length > 0 ? [steps[steps.length - 1].id] : [],
        status: 'pending',
      });
      stepCounter++;
    }

    // Step 4: System Host Telemetry (if requested)
    if (requiresSystem) {
      steps.push({
        id: `step_${stepCounter}`,
        order: stepCounter,
        description: `Inspect active host infrastructure, memory consumption, and runtime metrics.`,
        toolToUse: toolNames.includes('system_metrics') ? 'system_metrics' : undefined,
        toolArgsHint: { detailLevel: 'verbose' },
        dependencies: [],
        status: 'pending',
      });
      stepCounter++;
    }

    // Fallback: If no specific trigger matched, add general RAG search step
    if (steps.length === 0) {
      steps.push({
        id: `step_1`,
        order: 1,
        description: `Consult knowledge base for domain context and architectural guidelines.`,
        toolToUse: 'vector_knowledge_search',
        toolArgsHint: { query: goal, topK: 3 },
        dependencies: [],
        status: 'pending',
      });
    }

    return {
      planId,
      goal,
      steps,
      strategyRationale: `Decomposed goal into ${steps.length} sequential execution stages utilizing ${steps.map(s => s.toolToUse).filter(Boolean).join(', ')}.`,
      estimatedComplexity: steps.length > 2 ? 'high' : steps.length > 1 ? 'medium' : 'low',
      createdAt: Date.now(),
    };
  }

  /**
   * Refines or extends a plan based on Critic feedback.
   */
  public async revisePlan(currentPlan: ExecutionPlan, feedback: string): Promise<ExecutionPlan> {
    const revisedSteps = [...currentPlan.steps];
    const newStepId = `step_${revisedSteps.length + 1}`;

    revisedSteps.push({
      id: newStepId,
      order: revisedSteps.length + 1,
      description: `Critic Revision Action: Address critique "${feedback.slice(0, 100)}..." via targeted knowledge verification.`,
      toolToUse: 'vector_knowledge_search',
      toolArgsHint: { query: feedback, topK: 2 },
      dependencies: [revisedSteps[revisedSteps.length - 1].id],
      status: 'pending',
    });

    return {
      ...currentPlan,
      steps: revisedSteps,
      strategyRationale: `Plan revised to incorporate feedback: ${feedback}`,
    };
  }
}
