import { LitElement, css, html } from 'lit';
import { ContextProvider } from '@lit/context';
import { MessageProcessor } from '@a2ui/web_core/v0_9';
import { A2uiSurface, Context, basicCatalog } from '@a2ui/lit/v0_9';
import { renderMarkdown } from '@a2ui/markdown-it';

const DEFAULT_AGENT_URL = 'ws://127.0.0.1:8765';
const RECONNECT_DELAY_MS = 1000;
const END = Symbol('stream end');

/**
 * ?agent=ws://host:port | http://host:port (SSE) | poll://host:port.
 * Every connector resolves to {send, messages}, where messages is an
 * async iterable of A2UI messages; unavailability rejects the promise
 * and the next transport on the same host:port gets a turn.
 */

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/** Adapts an event-driven source into an async iterable of messages. */
function messageQueue() {
  const items = [];
  const waiters = [];
  return {
    push(item) {
      const waiter = waiters.shift();
      if (waiter) waiter(item);
      else items.push(item);
    },
    close() {
      this.push(END);
    },
    async *[Symbol.asyncIterator]() {
      for (;;) {
        const item = items.length
          ? items.shift()
          : await new Promise((resolve) => waiters.push(resolve));
        if (item === END) return;
        yield item;
      }
    },
  };
}

const postAction = (url, message) =>
  fetch(`${url}/actions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message),
  }).catch(() => {});

function viaWebSocket(url) {
  return new Promise((resolve, reject) => {
    const socket = new WebSocket(url);
    const queue = messageQueue();
    socket.onopen = () =>
      resolve({ send: (m) => socket.send(JSON.stringify(m)), messages: queue });
    socket.onmessage = (event) => queue.push(JSON.parse(event.data));
    socket.onerror = () => reject(new Error('websocket unavailable'));
    socket.onclose = () => queue.close();
  });
}

function viaEventSource(url) {
  return new Promise((resolve) => {
    const source = new EventSource(`${url}/events`);
    const queue = messageQueue();
    source.onopen = () => resolve({ send: (m) => postAction(url, m), messages: queue });
    source.onmessage = (event) => queue.push(JSON.parse(event.data));
    source.onerror = () => {
      // cut EventSource's own auto-reconnect: a dead agent or a transport
      // switch hands control back to the fallback chain, which re-probes
      // every connector from the start
      source.close();
      queue.close();
      resolve(null); // no-op once the connection resolved
    };
  });
}

async function viaPoll(url) {
  const probe = await fetch(`${url}/events?after=0`);
  if (!probe.ok) throw new Error('poll unavailable');
  const messages = {
    async *[Symbol.asyncIterator]() {
      let cursor = 0;
      for (;;) {
        const response = await fetch(`${url}/events?after=${cursor}`);
        if (!response.ok) return; // a dead agent hands control back to the fallback chain
        const batch = await response.json();
        for (const message of batch.messages) yield message;
        cursor = batch.next;
      }
    },
  };
  return { send: (m) => postAction(url, m), messages };
}

/**
 * A2UI renderer shell: connects to the Python agent, feeds incoming
 * messages into the MessageProcessor and renders the current surface
 * through the official <a2ui-surface> Lit element.
 */
class ArgentaA2uiApp extends LitElement {
  static properties = {
    surface: { attribute: false },
    status: {},
  };

  static styles = css`
    .a2ui-container {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .status {
      font-size: 0.875rem;
      opacity: 0.6;
    }
    /* the output card is the first child of the root column: fix its
       height and let the log scroll inside instead of growing the page */
    a2ui-surface > a2ui-basic-column > a2ui-card:first-of-type {
      display: block;
      max-height: 16rem;
      overflow-y: auto;
    }
    a2ui-surface > a2ui-basic-column > a2ui-card:first-of-type pre {
      margin: 0;
    }
  `;

  processor = new MessageProcessor([basicCatalog], (action) => {
    this.send({ version: 'v0.9', action });
  });

  constructor() {
    super();
    this.surface = undefined;
    this.status = 'connecting';
    this.outbound = undefined;
    new ContextProvider(this, {
      context: Context.markdown,
      initialValue: renderMarkdown,
    });
  }

  connectedCallback() {
    super.connectedCallback();
    this.processor.onSurfaceCreated((surface) => {
      this.surface = surface;
    });
    this.processor.onSurfaceDeleted(() => {
      this.surface = undefined;
    });
    void this.run();
  }

  agentUrl() {
    return new URLSearchParams(location.search).get('agent') || DEFAULT_AGENT_URL;
  }

  /** Tries each transport on the agent address; null when none answers. */
  async openTransport() {
    const url = this.agentUrl();
    const httpUrl = url.replace(/^\w+/, 'http');
    const connectors = url.startsWith('ws')
      ? [() => viaWebSocket(url), () => viaEventSource(httpUrl), () => viaPoll(httpUrl)]
      : [() => viaEventSource(httpUrl), () => viaPoll(httpUrl)];
    for (const connect of connectors) {
      try {
        const conn = await connect();
        if (conn) return conn;
      } catch {
        // transport unavailable — try the next one
      }
    }
    return null;
  }

  async run() {
    for (;;) {
      const conn = await this.openTransport();
      this.outbound = conn?.send;
      this.status = conn ? 'connected' : 'unreachable, retrying…';
      if (conn) {
        try {
          for await (const message of conn.messages) {
            this.processor.processMessages(message);
            this.pinLogScroll();
          }
        } catch {
          // the transport dropped mid-stream — reconnect
        }
        this.status = 'disconnected, reconnecting…';
      }
      await sleep(RECONNECT_DELAY_MS);
    }
  }

  send(message) {
    this.outbound?.(message);
  }

  /**
   * Keeps the output card glued to the log tail. Once the user scrolls
   * up, the pin releases until they return to the bottom.
   */
  pinLogScroll() {
    const card = this.shadowRoot?.querySelector(
      'a2ui-surface > a2ui-basic-column > a2ui-card',
    );
    if (!card) return;
    if (!card.dataset.pinHooked) {
      card.dataset.pinHooked = '1';
      card.addEventListener('scroll', () => {
        this._logPinned =
          card.scrollTop + card.clientHeight >= card.scrollHeight - 24;
      });
    }
    if (this._logPinned === false) return;
    requestAnimationFrame(() => {
      card.scrollTop = card.scrollHeight;
    });
  }

  render() {
    return html`
      <div class="a2ui-container">
        <div class="status">${this.agentUrl()} — ${this.status}</div>
        ${this.surface
          ? html`<a2ui-surface .surface=${this.surface}></a2ui-surface>`
          : html`<div>Waiting for the agent surface…</div>`}
      </div>
    `;
  }
}

customElements.define('argenta-a2ui-app', ArgentaA2uiApp);
