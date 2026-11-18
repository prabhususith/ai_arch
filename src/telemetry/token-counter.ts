/**
 * Token Counter & Cost Telemetry Engine
 * Estimates token consumption using BPE character heuristics, simulates KV-cache hits,
 * and calculates exact financial costs based on standard pricing tiers.
 */

import { TokenTelemetry, TokenRateModel } from '../types/index.js';

export class TokenCounter {
  private static defaultRateModel: TokenRateModel = {
    name: 'Gemini-1.5-Pro Enterprise',
    promptPricePer1K: 0.0035, // $3.50 per 1M
    completionPricePer1K: 0.0105, // $10.50 per 1M
  };

  /**
   * Estimates token count for an arbitrary string or JSON structure.
   * Standard subword heuristic: ~3.8 characters per token for English text/code.
   */
  public static estimateTokens(input: string | object | null | undefined): number {
    if (!input) return 0;
    const text = typeof input === 'string' ? input : JSON.stringify(input);
    if (text.length === 0) return 0;

    // Advanced heuristic: whitespace/punctuation boundaries + character count
    const words = text.split(/\s+/).length;
    const charCount = text.length;

    // Blended estimate: average of word-based and char-based subword splitting
    const charEstimate = Math.ceil(charCount / 3.8);
    const wordEstimate = Math.ceil(words * 1.3);

    return Math.max(1, Math.round((charEstimate * 0.7) + (wordEstimate * 0.3)));
  }

  /**
   * Initializes a zeroed telemetry state.
   */
  public static createTelemetry(): TokenTelemetry {
    return {
      promptTokens: 0,
      completionTokens: 0,
      totalTokens: 0,
      cacheHitTokens: 0,
      estimatedCostUSD: 0,
      totalLatencyMs: 0,
      stepCount: 0,
    };
  }

  /**
   * Updates telemetry state with new prompt and completion tokens.
   */
  public static recordUsage(
    current: TokenTelemetry,
    promptText: string,
    completionText: string,
    latencyMs: number,
    cachedPromptPrefixTokens: number = 0,
    model: TokenRateModel = this.defaultRateModel
  ): TokenTelemetry {
    const rawPromptTokens = this.estimateTokens(promptText);
    const completionTokens = this.estimateTokens(completionText);

    // Apply cache hit discount (50% discount on cached input tokens)
    const effectivePromptTokens = Math.max(0, rawPromptTokens - cachedPromptPrefixTokens);
    const cacheTokens = Math.min(rawPromptTokens, cachedPromptPrefixTokens);

    const promptCost = (effectivePromptTokens / 1000) * model.promptPricePer1K;
    const cachedCost = (cacheTokens / 1000) * (model.promptPricePer1K * 0.5);
    const completionCost = (completionTokens / 1000) * model.completionPricePer1K;

    const addedCost = promptCost + cachedCost + completionCost;

    return {
      promptTokens: current.promptTokens + rawPromptTokens,
      completionTokens: current.completionTokens + completionTokens,
      totalTokens: current.totalTokens + rawPromptTokens + completionTokens,
      cacheHitTokens: current.cacheHitTokens + cacheTokens,
      estimatedCostUSD: Number((current.estimatedCostUSD + addedCost).toFixed(6)),
      totalLatencyMs: current.totalLatencyMs + latencyMs,
      stepCount: current.stepCount + 1,
    };
  }
}
