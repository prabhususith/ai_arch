/**
 * Server-Sent Events (SSE) Streaming Manager
 * Handles HTTP text/event-stream connections, event frame serialization,
 * and client disconnection cleanup.
 */

import { Response } from 'express';

export class SSEManager {
  private clients: Map<string, Response> = new Map();

  /**
   * Registers a client response stream for SSE.
   */
  public registerClient(clientId: string, res: Response): void {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no'); // Disable Nginx proxy buffering
    res.flushHeaders?.();

    // Send initial handshake
    this.sendToClient(res, 'status', { message: 'SSE connection established', clientId });

    this.clients.set(clientId, res);

    res.on('close', () => {
      this.clients.delete(clientId);
    });
  }

  /**
   * Sends an SSE message frame to a specific client.
   */
  public send(clientId: string, event: string, data: any): void {
    const res = this.clients.get(clientId);
    if (res) {
      this.sendToClient(res, event, data);
    }
  }

  /**
   * Broadcasts an SSE frame to all connected clients.
   */
  public broadcast(event: string, data: any): void {
    for (const res of this.clients.values()) {
      this.sendToClient(res, event, data);
    }
  }

  /**
   * Formats and writes the SSE frame conforming to standard W3C EventSource specifications.
   */
  private sendToClient(res: Response, event: string, data: any): void {
    try {
      const payload = typeof data === 'string' ? data : JSON.stringify(data);
      res.write(`event: ${event}\n`);
      res.write(`data: ${payload}\n\n`);
    } catch (err) {
      // Stream may be closed
    }
  }

  /**
   * Removes a client.
   */
  public removeClient(clientId: string): void {
    const res = this.clients.get(clientId);
    if (res) {
      try {
        res.end();
      } catch (err) {}
      this.clients.delete(clientId);
    }
  }

  /**
   * Count of active SSE connections.
   */
  public getActiveCount(): number {
    return this.clients.size;
  }
}
