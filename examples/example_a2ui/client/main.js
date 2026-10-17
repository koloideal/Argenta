import { LitElement, css, html } from 'lit';
import { ContextProvider } from '@lit/context';
import { MessageProcessor } from '@a2ui/web_core/v0_9';
import { A2uiSurface, Context, basicCatalog } from '@a2ui/lit/v0_9';
import { renderMarkdown } from '@a2ui/markdown-it';

const DEFAULT_AGENT_URL = 'ws://127.0.0.1:8765';

/**
 * Two transports: ?agent=ws://host:port (WebSocket) or
 * ?agent=http://host:port (SSE stream + POST /actions)
 */

/**
 * A2UI renderer shell: keeps a WebSocket connection to the Python agent,
 * feeds incoming messages into the MessageProcessor and renders the
 * current surface through the official <a2ui-surface> Lit element.
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
  `;

  processor = new MessageProcessor([basicCatalog], (action) => {
    this.send({ version: 'v0.9', action });
  });

  constructor() {
    super();
    this.surface = undefined;
    this.status = 'connecting';
    this.socket = undefined;
    new ContextProvider(this, {
      context: Context.markdown,
      initialValue: renderMarkdown,
    });
  }

  connectedCallback() {
    super.connectedCallback();
    this.processor.onSurfaceCreated((surface) => {
      this.surface = surface;
      this.status = 'connected';
    });
    this.processor.onSurfaceDeleted(() => {
      this.surface = undefined;
    });
    this.connect();
  }

  agentUrl() {
    return new URLSearchParams(location.search).get('agent') || DEFAULT_AGENT_URL;
  }

  connect() {
    const url = this.agentUrl();
    if (url.startsWith('http')) {
      this.connectSse(url);
      return;
    }
    const socket = new WebSocket(url);
    this.socket = socket;
    socket.addEventListener('open', () => {
      this.status = 'connected';
    });
    socket.addEventListener('message', (event) => {
      this.processor.processMessages(JSON.parse(event.data));
    });
    socket.addEventListener('close', () => {
      this.status = 'disconnected, reconnecting…';
      setTimeout(() => this.connect(), 1000);
    });
    socket.addEventListener('error', () => {
      this.status = 'connection error';
    });
  }

  connectSse(url) {
    const source = new EventSource(`${url}/events`);
    this.eventSource = source;
    source.addEventListener('open', () => {
      this.status = 'connected';
    });
    source.addEventListener('message', (event) => {
      this.processor.processMessages(JSON.parse(event.data));
    });
    // EventSource reconnects by itself; the transport replays history
    source.addEventListener('error', () => {
      this.status = 'disconnected, reconnecting…';
    });
  }

  send(message) {
    const url = this.agentUrl();
    if (url.startsWith('http')) {
      fetch(`${url}/actions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(message),
      });
      return;
    }
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    }
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
