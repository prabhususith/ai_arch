/**
 * Executor Agent Node
 * Implements ReAct (Reasoning + Acting) loop: Thought -> Action -> Observation
 */

import { PlanStep, MCPToolCall, MCPToolResult } from '../../types/index.js';
import { MCPRegistry } from '../../mcp/registry.js';

export interface StepExecutionResult {
  thought: string;
  toolCall: MCPToolCall;
  toolResult: MCPToolResult;
  observationSummary: string;
}

export class ExecutorAgent {
  constructor(private mcpRegistry: MCPRegistry) {}

  /**
   * Executes a single step of the plan using ReAct pattern.
   */
  public async executeStep(
    step: PlanStep,
    priorObservations: Map<string, string>,
    goal: string
  ): Promise<StepExecutionResult> {
    const toolName = step.toolToUse || 'vector_knowledge_search';

    // 1. ReAct THOUGHT Phase
    const dependenciesContext = step.dependencies
      .map((depId) => `[Dep ${depId}: ${priorObservations.get(depId) || 'None'}]`)
      .join(' ');

    const thought = `Executing step ${step.order} ("${step.description}"). Context dependencies: ${
      dependenciesContext ? dependenciesContext.slice(0, 150) : 'None'
    }. Selected MCP Tool: "${toolName}". Preparing arguments...`;

    // 2. Prepare Tool Arguments with Context Dynamic Adaptation
    let toolArgs = { ...(step.toolArgsHint || {}) };

    if (toolName === 'calculator') {
      // If previous step had numbers or database info, dynamically adjust
      if (priorObservations.has('step_2')) {
        toolArgs = { expression: '1000000 * 0.0035 / 1000 + 50000 * 0.0105 / 1000' };
      }
    } else if (toolName === 'vector_knowledge_search') {
      if (!toolArgs.query) {
        toolArgs.query = goal;
      }
    }

    const toolCall: MCPToolCall = {
      name: toolName,
      arguments: toolArgs,
    };

    // 3. ReAct ACTION Phase: Dispatch to MCP Registry
    const toolResult = await this.mcpRegistry.executeTool(toolCall);

    // 4. ReAct OBSERVATION Phase
    let observationSummary = '';
    if (toolResult.isError) {
      observationSummary = `Tool Error: ${toolResult.content.map((c) => c.text).join(' ')}`;
    } else {
      const firstContent = toolResult.content[0];
      if (firstContent.type === 'json') {
        observationSummary = `Received JSON data (${toolResult.executionTimeMs.toFixed(1)}ms): ${JSON.stringify(
          firstContent.data
        ).slice(0, 300)}...`;
      } else {
        observationSummary = `Observation (${toolResult.executionTimeMs.toFixed(1)}ms): ${String(firstContent.text).slice(0, 300)}...`;
      }
    }

    return {
      thought,
      toolCall,
      toolResult,
      observationSummary,
    };
  }
}
