/**
 * Model Context Protocol (MCP) Tool Registry
 * Conforms to MCP specification for tool discovery, JSON Schema validation,
 * execution sandboxing, and standardized error encapsulation.
 */

import { MCPToolDefinition, MCPToolResult, MCPToolCall } from '../types/index.js';

export type ToolHandler = (args: Record<string, any>) => Promise<any> | any;

export interface RegisteredTool {
  definition: MCPToolDefinition;
  handler: ToolHandler;
}

export class MCPRegistry {
  private tools: Map<string, RegisteredTool> = new Map();

  /**
   * Registers a new tool into the MCP catalog.
   */
  public registerTool(definition: MCPToolDefinition, handler: ToolHandler): void {
    if (this.tools.has(definition.name)) {
      throw new Error(`MCP Tool with name '${definition.name}' is already registered.`);
    }
    this.tools.set(definition.name, { definition, handler });
  }

  /**
   * Returns all available tools conforming to MCP listTools protocol.
   */
  public listTools(): MCPToolDefinition[] {
    return Array.from(this.tools.values()).map((t) => t.definition);
  }

  /**
   * Retrieves a specific tool definition by name.
   */
  public getTool(name: string): MCPToolDefinition | undefined {
    return this.tools.get(name)?.definition;
  }

  /**
   * Validates arguments against the tool's parameter schema.
   */
  private validateArguments(schema: MCPToolDefinition['inputSchema'], args: Record<string, any>): string[] {
    const errors: string[] = [];
    if (!args || typeof args !== 'object') {
      return ['Arguments must be a valid JSON object.'];
    }

    if (schema.required) {
      for (const requiredField of schema.required) {
        if (!(requiredField in args) || args[requiredField] === undefined || args[requiredField] === null) {
          errors.push(`Missing required parameter: '${requiredField}'`);
        }
      }
    }

    for (const [key, value] of Object.entries(args)) {
      const propDef = schema.properties[key];
      if (propDef) {
        const actualType = Array.isArray(value) ? 'array' : typeof value;
        if (propDef.type === 'number' && typeof value === 'number') {
          // valid
        } else if (propDef.type !== actualType && value !== null) {
          errors.push(`Parameter '${key}' expected type '${propDef.type}', got '${actualType}'`);
        }
      }
    }

    return errors;
  }

  /**
   * Executes a tool via MCP invocation standard with timeout and error capture.
   */
  public async executeTool(toolCall: MCPToolCall): Promise<MCPToolResult> {
    const startTime = performance.now();
    const tool = this.tools.get(toolCall.name);

    if (!tool) {
      return {
        toolName: toolCall.name,
        isError: true,
        content: [
          {
            type: 'text',
            text: `Tool '${toolCall.name}' not found in MCP registry. Available: ${Array.from(this.tools.keys()).join(', ')}`,
          },
        ],
        executionTimeMs: performance.now() - startTime,
      };
    }

    // 1. Schema Validation
    const validationErrors = this.validateArguments(tool.definition.inputSchema, toolCall.arguments || {});
    if (validationErrors.length > 0) {
      return {
        toolName: toolCall.name,
        isError: true,
        content: [
          {
            type: 'text',
            text: `Validation failed for tool '${toolCall.name}': ${validationErrors.join('; ')}`,
          },
        ],
        executionTimeMs: performance.now() - startTime,
      };
    }

    // 2. Safe Execution with Timeout
    const timeoutMs = tool.definition.timeoutMs || 8000;

    try {
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error(`MCP Tool '${toolCall.name}' timed out after ${timeoutMs}ms`)), timeoutMs)
      );

      const executionPromise = Promise.resolve(tool.handler(toolCall.arguments));
      const rawResult = await Promise.race([executionPromise, timeoutPromise]);

      const formattedContent =
        typeof rawResult === 'string'
          ? [{ type: 'text' as const, text: rawResult }]
          : [
              {
                type: 'json' as const,
                text: JSON.stringify(rawResult, null, 2),
                data: rawResult,
              },
            ];

      return {
        toolName: toolCall.name,
        isError: false,
        content: formattedContent,
        executionTimeMs: performance.now() - startTime,
      };
    } catch (err: any) {
      return {
        toolName: toolCall.name,
        isError: true,
        content: [
          {
            type: 'text',
            text: `Error executing MCP tool '${toolCall.name}': ${err.message || String(err)}`,
          },
        ],
        executionTimeMs: performance.now() - startTime,
      };
    }
  }
}
