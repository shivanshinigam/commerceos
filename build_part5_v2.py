#!/usr/bin/env python3
"""Build Part 5 (V2): Complete other tabs (Developer, Architecture, UCP)"""

import re
import os

TABS_CSS = r'''
/* ============================================================
   COMMERCEOS V2 — TABS CSS (Dev, Arch, UCP)
   ============================================================ */

/* Developer Tab */
.event-item {
  padding: 16px;
  border-bottom: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.event-item:hover { background: rgba(255,255,255,0.02); }
.event-item.active { background: rgba(124, 58, 237, 0.1); border-left: 3px solid var(--accent-purple); }
.event-item .title { font-weight: 600; font-size: 0.95rem; color: var(--text-primary); margin-bottom: 4px; }
.event-item .badge { font-size: 0.7rem; padding: 2px 6px; border-radius: 4px; background: rgba(16, 185, 129, 0.2); color: var(--accent-green); }
.event-item .time { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-muted); }

/* Architecture Diagram */
.arch-grid {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
  padding: 40px 0;
  position: relative;
}
.arch-node {
  background: var(--bg-glass);
  border: 1px solid var(--border-default);
  padding: 24px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-glass);
  width: 300px;
  text-align: center;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(12px);
  transition: all 0.3s;
}
.arch-node:hover {
  transform: translateY(-5px);
  border-color: var(--border-strong);
  box-shadow: var(--shadow-glow);
}
.arch-node .icon { font-size: 2.5rem; margin-bottom: 12px; }
.arch-node .title { font-size: 1.2rem; font-weight: 800; color: white; margin-bottom: 8px; }
.arch-node .desc { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.4; }

.arch-merchants {
  display: flex;
  gap: 24px;
  justify-content: center;
  flex-wrap: wrap;
}
.arch-merchants .arch-node { width: 220px; }

/* Connecting Lines (CSS-only approximation) */
.arch-line {
  width: 2px;
  height: 40px;
  background: linear-gradient(to bottom, var(--accent-purple-glow), var(--accent-cyan));
  margin: 0 auto;
  position: relative;
  z-index: 1;
}
.arch-line::after {
  content: '';
  position: absolute;
  top: 0; left: -1px; width: 4px; height: 10px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 0 10px white;
  animation: data-flow 2s infinite linear;
}
@keyframes data-flow {
  0% { top: 0; opacity: 1; }
  100% { top: 40px; opacity: 0; }
}

/* UCP Explorer */
.ucp-menu-header {
  padding: 16px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--text-muted);
  text-transform: uppercase;
  border-bottom: 1px solid var(--border-subtle);
}
.ucp-nav {
  display: block;
  width: 100%;
  text-align: left;
  padding: 12px 16px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 2px solid transparent;
}
.ucp-nav:hover { color: white; background: rgba(255,255,255,0.03); }
.ucp-nav.active {
  color: var(--accent-purple-light);
  background: rgba(124, 58, 237, 0.1);
  border-left-color: var(--accent-purple);
}

.ucp-doc-section { display: none; padding: 32px; animation: fadeIn 0.3s ease forwards; }
.ucp-doc-section.active { display: block; }
.ucp-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(59, 130, 246, 0.2);
  color: var(--accent-blue-light);
  margin-right: 12px;
}
.ucp-endpoint { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: white; }
'''

TABS_HTML = r'''
<!-- PART 5: V2 TABS -->
<!-- DEVELOPER TAB -->
<div class="page" id="page-developer">
  <div class="section-container">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px;">
      <div>
        <h2 class="text-primary" style="font-size:2rem; font-weight:800; margin-bottom:8px;">Developer / Trace</h2>
        <p class="text-secondary">Inspect raw UCP JSON payloads exchanged during the simulated session.</p>
      </div>
      <div class="glass-panel" style="padding:12px 24px; border-radius:30px;">
        <span class="text-xs font-mono text-muted">TOTAL LATENCY</span><br>
        <span id="dev-total-latency" class="text-accent-cyan font-mono" style="font-size:1.2rem; font-weight:700;">0ms</span>
      </div>
    </div>
    
    <div class="two-col-layout">
      <!-- Event List -->
      <div class="glass-panel" style="padding:0; overflow:hidden; height:600px; display:flex; flex-direction:column;">
        <div class="card-header" style="background:rgba(124,58,237,0.1); border-bottom:1px solid var(--border-subtle); padding:16px;">
          <span class="card-title text-primary" style="font-size:0.9rem; letter-spacing:1px; text-transform:uppercase;">API Event Log</span>
        </div>
        <div id="dev-event-list" style="overflow-y:auto; flex:1;">
          <div style="padding:40px 24px; text-align:center; color:var(--text-muted);">
            Run the Agent in the Shopper tab to generate a trace.
          </div>
        </div>
      </div>
      
      <!-- Code Viewer -->
      <div class="glass-panel" style="padding:0; overflow:hidden; background:#000; border:1px solid var(--border-strong); display:flex; flex-direction:column; height:600px;">
        <div class="card-header" style="background:#0a0a0a; border-bottom:1px solid #222; padding:12px 16px; display:flex; gap:8px; align-items:center;">
           <div class="term-dot r"></div><div class="term-dot y"></div><div class="term-dot g"></div>
           <span class="font-mono text-xs text-muted" style="margin-left:8px;" id="dev-payload-title">No event selected</span>
        </div>
        <div style="flex:1; overflow:auto; position:relative;">
          <pre id="dev-payload-view" class="font-mono text-sm" style="padding:24px; color:var(--text-code); margin:0; line-height:1.6;">// Select an event from the log to inspect its UCP payload.</pre>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ARCHITECTURE TAB -->
<div class="page" id="page-architecture">
  <div class="section-container">
    <div style="text-align:center; margin-bottom: 24px;">
      <h2 class="text-primary" style="font-size:2.5rem; font-weight:800; margin-bottom:12px;">Agentic Topology</h2>
      <p class="text-secondary" style="max-width:600px; margin:0 auto;">How natural language intents are deterministically resolved via the Universal Commerce Protocol.</p>
    </div>
    
    <div class="arch-grid">
      <!-- 1. User -->
      <div class="arch-node">
        <div class="icon">👤</div>
        <div class="title">User</div>
        <div class="desc">Provides natural language shopping intent via prompt or voice.</div>
      </div>
      
      <div class="arch-line"></div>
      
      <!-- 2. Agent Core -->
      <div class="arch-node" style="border-color:var(--accent-purple); box-shadow:0 0 30px var(--accent-purple-glow);">
        <div class="icon">🧠</div>
        <div class="title">Agent Core (LLM)</div>
        <div class="desc">Parses intent, plans execution, and makes tool calls adhering to constraints.</div>
      </div>
      
      <div class="arch-line"></div>
      
      <!-- 3. UCP Router -->
      <div class="arch-node" style="border-color:var(--accent-cyan); box-shadow:0 0 30px rgba(6,182,212,0.3); width:350px;">
        <div class="icon">🛣️</div>
        <div class="title">UCP Network Router</div>
        <div class="desc">The protocol translation layer. Broadcasts deterministic JSON to registered merchant endpoints.</div>
      </div>
      
      <!-- Branching lines -->
      <div style="display:flex; justify-content:center; gap:200px; position:relative; width:100%; height:40px;">
         <div style="position:absolute; top:0; left:50%; transform:translateX(-50%); width:460px; height:2px; background:linear-gradient(90deg, var(--border-subtle), var(--accent-cyan), var(--border-subtle));"></div>
         <div class="arch-line" style="margin:0;"></div>
         <div class="arch-line" style="margin:0;"></div>
         <div class="arch-line" style="margin:0;"></div>
      </div>
      
      <!-- 4. Merchants -->
      <div class="arch-merchants">
        <div class="arch-node" style="border-top-color:#7c3aed;">
          <div class="title" style="color:#a78bfa;">NOVA</div>
          <div class="desc font-mono text-xs mt-2">API: /ucp/v1/*</div>
        </div>
        <div class="arch-node" style="border-top-color:#10b981;">
          <div class="title" style="color:#34d399;">VeloMart</div>
          <div class="desc font-mono text-xs mt-2">API: /ucp/v1/*</div>
        </div>
        <div class="arch-node" style="border-top-color:#f59e0b;">
          <div class="title" style="color:#fbbf24;">UrbanCart</div>
          <div class="desc font-mono text-xs mt-2">API: /ucp/v1/*</div>
        </div>
      </div>
      
    </div>
  </div>
</div>

<!-- UCP EXPLORER TAB -->
<div class="page" id="page-ucp">
  <div class="section-container">
    <div style="margin-bottom:32px;">
      <h2 class="text-primary" style="font-size:2rem; font-weight:800; margin-bottom:8px;">Google Universal Commerce Protocol <span class="badge" style="font-size:0.8rem;vertical-align:middle;margin-left:12px;background:var(--accent-purple);padding:4px 8px;border-radius:4px;">v2026-04-08</span></h2>
      <p class="text-secondary" style="line-height:1.6; max-width:700px;">
        UCP is Google's open standard for agentic commerce — enabling Gemini AI to complete purchases directly from merchants without leaving the conversational interface.
        <span style="color:#f59e0b;font-weight:600;">[Notice: Running on a simulated catalog dataset for protocol demonstration]</span>
      </p>
      <a href="https://developers.google.com/merchant/ucp" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;margin-top:12px;font-size:0.8rem;color:var(--accent-cyan);text-decoration:none;border:1px solid rgba(6,182,212,0.3);padding:6px 12px;border-radius:6px;">
        Official Specification: developers.google.com/merchant/ucp ↗
      </a>
    </div>

    <!-- UCP LIVE SIMULATOR -->
    <div style="margin-bottom:32px;border:1px solid rgba(6,182,212,0.4);border-radius:16px;overflow:hidden;">
      <div style="padding:16px 20px;background:rgba(6,182,212,0.1);border-bottom:1px solid rgba(6,182,212,0.2);display:flex;align-items:center;justify-content:space-between;">
        <div>
          <div style="font-size:0.7rem;font-weight:800;color:#06b6d4;letter-spacing:1px;margin-bottom:4px;">LIVE UCP PROTOCOL SIMULATOR</div>
          <div style="font-size:0.85rem;color:white;font-weight:700;">Simulate Google UCP direct buying transaction step-by-step</div>
        </div>
        <button id="ucp-sim-btn" onclick="runUCPSimulator()" style="background:linear-gradient(135deg,#0891b2,#7c3aed);color:white;border:none;padding:10px 20px;border-radius:10px;font-weight:800;font-size:0.82rem;cursor:pointer;transition:opacity 0.2s;" onmouseover="this.style.opacity='0.85'" onmouseout="this.style.opacity='1'">Run Protocol Simulation</button>
      </div>
      <div id="ucp-sim-area" style="padding:20px;background:rgba(0,0,0,0.4);font-family:'JetBrains Mono',monospace;font-size:0.75rem;min-height:120px;">
        <div style="color:var(--text-muted);text-align:center;padding:30px 0;">Click "Run Protocol Simulation" to watch real-time UCP JSON payload exchange →</div>
      </div>
    </div>

    <!-- HOW IT WORKS BANNER -->
    <div style="background:linear-gradient(135deg,rgba(124,58,237,0.15),rgba(6,182,212,0.1));border:1px solid rgba(124,58,237,0.3);border-radius:16px;padding:24px;margin-bottom:32px;">
      <h3 style="color:white;font-weight:800;margin-bottom:16px;">UCP Direct Buying Protocol Execution Sequence</h3>
      <div style="display:flex;gap:0;align-items:center;flex-wrap:wrap;gap:8px;">
        <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(124,58,237,0.4);border-radius:10px;padding:12px 16px;text-align:center;min-width:140px;">
          <div style="font-size:0.75rem;font-weight:800;color:#a78bfa;">STEP 1</div>
          <div style="font-size:0.8rem;color:white;margin-top:4px;">Intent Prompt<br/><span style="color:var(--text-muted);font-size:0.7rem;">User asks Gemini</span></div>
        </div>
        <div style="color:var(--accent-cyan);font-size:1.2rem;padding:0 4px;">→</div>
        <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(6,182,212,0.4);border-radius:10px;padding:12px 16px;text-align:center;min-width:140px;">
          <div style="font-size:0.75rem;font-weight:800;color:#06b6d4;">STEP 2</div>
          <div style="font-size:0.8rem;color:white;margin-top:4px;">Discovery<br/><span style="color:var(--text-muted);font-size:0.7rem;">/.well-known/ucp</span></div>
        </div>
        <div style="color:var(--accent-cyan);font-size:1.2rem;padding:0 4px;">→</div>
        <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(16,185,129,0.4);border-radius:10px;padding:12px 16px;text-align:center;min-width:140px;">
          <div style="font-size:0.75rem;font-weight:800;color:#10b981;">STEP 3</div>
          <div style="font-size:0.8rem;color:white;margin-top:4px;">Session Lock<br/><span style="color:var(--text-muted);font-size:0.7rem;">POST /checkout-sessions</span></div>
        </div>
        <div style="color:var(--accent-cyan);font-size:1.2rem;padding:0 4px;">→</div>
        <div style="background:rgba(0,0,0,0.4);border:1px solid rgba(245,158,11,0.4);border-radius:10px;padding:12px 16px;text-align:center;min-width:140px;">
          <div style="font-size:0.75rem;font-weight:800;color:#f59e0b;">STEP 4</div>
          <div style="font-size:0.8rem;color:white;margin-top:4px;">Google Pay Token<br/><span style="color:var(--text-muted);font-size:0.7rem;">Direct Settlement</span></div>
        </div>
      </div>
    </div>
    
    <div class="two-col-layout" style="grid-template-columns: 260px 1fr; gap:0; border:1px solid var(--border-subtle); border-radius:var(--radius-lg); overflow:hidden;">
      <!-- Sidebar -->
      <div style="background:rgba(0,0,0,0.3); border-right:1px solid var(--border-subtle);">
        <div class="ucp-menu-header">Step 1 · Merchant Profile</div>
        <button class="ucp-nav active" data-doc="profile">GET /.well-known/ucp</button>
        <div class="ucp-menu-header" style="margin-top:16px;">Step 2 · Direct Buying</div>
        <button class="ucp-nav" data-doc="checkout-create">POST /checkout-sessions</button>
        <button class="ucp-nav" data-doc="checkout-get">GET /checkout-sessions/:id</button>
        <button class="ucp-nav" data-doc="checkout-complete">POST /:id/complete</button>
        <div class="ucp-menu-header" style="margin-top:16px;">Reference</div>
        <button class="ucp-nav" data-doc="status-states">Status States</button>
        <button class="ucp-nav" data-doc="capabilities">Capabilities</button>
        <div style="padding:16px;margin-top:8px;border-top:1px solid var(--border-subtle);">
          <div style="font-size:0.7rem;color:var(--text-muted);line-height:1.6;">Our CommerceOS demo simulates this spec in browser JS using a demonstration catalog. A live merchant implements these REST endpoints on their server.</div>
        </div>

      </div>
      
      <!-- Content Area -->
      <div style="background:rgba(20,20,35,0.4);" id="ucp-doc-container">
        
    "budget": { "max": "number" },
    "brand_preference": ["string"],
    "surface": "string",
    "use_case": ["string"]
  }
}</pre>
        </div>
        
        <!-- CART DOC -->
        <div class="ucp-doc-section" id="doc-cart">
          <div style="margin-bottom:24px;">
            <span class="ucp-badge">POST</span> <span class="ucp-endpoint">/ucp/v1/cart</span>
          </div>
          <p class="text-secondary" style="margin-bottom:24px; line-height:1.6;">Initialize a unified cart session across multiple merchants.</p>
          <pre class="font-mono text-sm" style="background:#0a0a0a; border:1px solid #222; padding:16px; color:var(--text-code); border-radius:var(--radius-sm); overflow-x:auto;">{
  "cart_id": "string (optional)",
  "items": [
    {
      "merchant_id": "string",
      "product_id": "string",
      "qty": "integer"
    }
  ]
}</pre>
        </div>
        
        <!-- CHECKOUT DOC -->
        <div class="ucp-doc-section" id="doc-checkout">
          <div style="margin-bottom:24px;">
            <span class="ucp-badge">POST</span> <span class="ucp-endpoint">/ucp/v1/checkout</span>
          </div>
          <p class="text-secondary" style="margin-bottom:24px; line-height:1.6;">State machine for deterministic, agent-driven checkout progression without UI scraping.</p>
          <pre class="font-mono text-sm" style="background:#0a0a0a; border:1px solid #222; padding:16px; color:var(--text-code); border-radius:var(--radius-sm); overflow-x:auto;">{
  "cart_id": "string",
  "action": "enum('INITIALIZE', 'ADVANCE', 'AUTHORIZE')",
  "payload": {
    "shipping_address": { ... },
    "payment_token": "string"
  }
}</pre>
        </div>
        
        <!-- GENERIC DOC STUB for others -->
        <div class="ucp-doc-section" id="doc-product"><div style="margin-bottom:24px;"><span class="ucp-badge">GET</span> <span class="ucp-endpoint">/ucp/v1/product/:id</span></div><p class="text-secondary">Retrieve detailed schema.org aligned product data.</p></div>
        <div class="ucp-doc-section" id="doc-order"><div style="margin-bottom:24px;"><span class="ucp-badge">POST</span> <span class="ucp-endpoint">/ucp/v1/order</span></div><p class="text-secondary">Finalize order and retrieve tracking webhook subscription.</p></div>
        
      </div>
    </div>
  </div>
</div>
'''

TABS_JS = r'''
<script>
// ---- V2 TABS LOGIC ----
document.addEventListener('DOMContentLoaded', () => {
  // 1. Hook into the agent runs to populate Developer Trace
  const originalUpdate = window.UI.updateAgentState;
  
  window.UI.updateAgentState = function() {
    // Call original if needed
    if (originalUpdate) originalUpdate.apply(this, arguments);
    
    // Update trace
    const list = document.getElementById('dev-event-list');
    const totalMs = document.getElementById('dev-total-latency');
    if (!list || !SESSION.trace) return;
    
    totalMs.textContent = `${SESSION.total_latency}ms`;
    
    if (SESSION.trace.length === 0) {
      list.innerHTML = '<div style="padding:40px 24px; text-align:center; color:var(--text-muted);">No events in current session.</div>';
      return;
    }
    
    list.innerHTML = '';
    SESSION.trace.forEach((trace, idx) => {
      const el = document.createElement('div');
      el.className = 'event-item';
      
      let badgeStr = `<span class="badge">${trace.status}</span>`;
      if (trace.status === 'error') badgeStr = `<span class="badge" style="background:rgba(239, 68, 68, 0.2); color:var(--accent-red);">error</span>`;
      
      el.innerHTML = `
        <div>
          <div class="title">${trace.event.toUpperCase()}</div>
          <div style="display:flex; gap:8px; align-items:center;">
             ${badgeStr}
             <span class="time">${trace.latency}ms</span>
          </div>
        </div>
        <div class="text-secondary text-xs font-mono">#${idx+1}</div>
      `;
      
      el.addEventListener('click', () => {
        document.querySelectorAll('.event-item').forEach(e => e.classList.remove('active'));
        el.classList.add('active');
        
        document.getElementById('dev-payload-title').textContent = `${trace.event}.json`;
        
        // Format payload beautifully
        const payload = {
          timestamp: trace.timestamp,
          latency_ms: trace.latency,
          request: trace.input,
          response: trace.output
        };
        
        document.getElementById('dev-payload-view').innerHTML = syntaxHighlight(JSON.stringify(payload, null, 2));
      });
      
      list.appendChild(el);
    });
  };

  // Simple JSON syntax highlighter
  function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        let cls = 'color:#60a5fa;'; // number
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'color:#a78bfa;font-weight:600;'; // key
            } else {
                cls = 'color:#34d399;'; // string
            }
        } else if (/true|false/.test(match)) {
            cls = 'color:#f59e0b;'; // boolean
        } else if (/null/.test(match)) {
            cls = 'color:#ef4444;'; // null
        }
        return '<span style="' + cls + '">' + match + '</span>';
    });
  }

  // 2. UCP Explorer Navigation
  const ucpNavs = document.querySelectorAll('.ucp-nav');
  const ucpDocs = document.querySelectorAll('.ucp-doc-section');
  
  ucpNavs.forEach(nav => {
    nav.addEventListener('click', () => {
      ucpNavs.forEach(n => n.classList.remove('active'));
      nav.classList.add('active');
      
      const docId = 'doc-' + nav.dataset.doc;
      ucpDocs.forEach(d => d.classList.remove('active'));
      const target = document.getElementById(docId);
      if (target) target.classList.add('active');
    });
  });
});

// ---- UCP LIVE SIMULATOR (CONNECTED TO FASTAPI SERVER WHEN ONLINE) ----
window.runUCPSimulator = async function() {
  const area = document.getElementById('ucp-sim-area');
  const btn = document.getElementById('ucp-sim-btn');
  if (!area) return;
  btn.disabled = true;
  btn.textContent = 'Running...';
  area.innerHTML = '';

  const delay = ms => new Promise(r => setTimeout(r, ms));

  const appendLine = (html, indent = 0) => {
    const div = document.createElement('div');
    div.style.cssText = `padding-left:${indent * 16}px; margin-bottom:3px; animation: fadeIn 0.3s ease;`;
    div.innerHTML = html;
    area.appendChild(div);
    area.scrollTop = area.scrollHeight;
  };

  const label = (text, color) => appendLine(`<span style="color:${color};font-weight:800;">${text}</span>`);
  const req = (method, path) => appendLine(`<span style="color:#60a5fa;">${method}</span> <span style="color:#f59e0b;">${path}</span>`, 1);
  const resp = (code, msg) => appendLine(`<span style="color:${code < 300 ? '#10b981' : '#ef4444'};">← ${code} ${msg}</span>`, 1);
  const json = (obj) => {
    const str = JSON.stringify(obj, null, 2);
    const colored = str
      .replace(/"([^"]+)":/g, '<span style="color:#a78bfa;">"$1"</span>:')
      .replace(/: "([^"]+)"/g, ': <span style="color:#34d399;">"$1"</span>')
      .replace(/: (\d+)/g, ': <span style="color:#60a5fa;">$1</span>')
      .replace(/: (true|false|null)/g, ': <span style="color:#f59e0b;">$1</span>');
    appendLine(`<pre style="margin:4px 0 10px;padding:10px;background:rgba(0,0,0,0.5);border-radius:6px;overflow-x:auto;color:var(--text-code);border-left:2px solid rgba(139,92,246,0.4);">${colored}</pre>`, 1);
  };
  const divider = () => appendLine(`<div style="border-top:1px solid rgba(255,255,255,0.05);margin:12px 0;"></div>`);

  // Check if real FastAPI server is running locally on 127.0.0.1:8000
  let isLiveBackend = false;
  let backendUrl = "http://127.0.0.1:8000";
  try {
    const healthCheck = await fetch(`${backendUrl}/`, { method: "GET" });
    if (healthCheck.ok) isLiveBackend = true;
  } catch(e) { isLiveBackend = false; }

  if (isLiveBackend) {
    appendLine(`<div style="padding:6px 10px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:6px;color:#10b981;font-weight:700;margin-bottom:10px;">[LIVE FASTAPI BACKEND CONNECTED: http://127.0.0.1:8000]</div>`);
  } else {
    appendLine(`<div style="padding:6px 10px;background:rgba(6,182,212,0.15);border:1px solid rgba(6,182,212,0.3);border-radius:6px;color:#06b6d4;font-weight:700;margin-bottom:10px;">[STANDALONE SIMULATOR MODE — Protocol Spec v2026-04-08]</div>`);
  }

  // ── STEP 1: Discovery ──
  label('STEP 1 — Merchant UCP Profile Discovery', '#06b6d4');
  appendLine('<span style="color:var(--text-muted);">Gemini verifies merchant capabilities by fetching /.well-known/ucp</span>', 1);
  await delay(400);

  let profileData;
  if (isLiveBackend) {
    req('GET', `${backendUrl}/.well-known/ucp`);
    try {
      const res = await fetch(`${backendUrl}/.well-known/ucp`);
      profileData = await res.json();
      resp(res.status, res.statusText);
      json(profileData);
    } catch(err) {
      resp(500, "Connection Error");
    }
  } else {
    req('GET', 'https://commerceos.demo/.well-known/ucp');
    await delay(600);
    resp(200, 'OK');
    profileData = { "@type": "MerchantPublisherProfile", "name": "CommerceOS Demo Labs", "ucp": { "version": "2026-04-08", "capabilities": ["direct_buying", "price_availability"], "checkoutSessionsEndpoint": "https://commerceos.demo/ucp/checkout-sessions", "paymentMethods": ["GOOGLE_PAY"] } };
    json(profileData);
  }
  appendLine('<span style="color:#34d399;font-size:0.7rem;">Merchant profile verified: direct_buying capability active</span>', 1);
  divider();
  await delay(700);

  // ── STEP 2: Create Checkout Session ──
  label('STEP 2 — Create Checkout Session', '#a78bfa');
  appendLine('<span style="color:var(--text-muted);">Gemini locks inventory & creates session for SKU-IPH15-128</span>', 1);
  await delay(400);

  let sessionData;
  let activeSessionId;
  const createPayload = { lineItems: [{ offerId: "SKU-IPH15-128", quantity: 1 }], userContext: { locale: "en-IN", currency: "INR" } };

  if (isLiveBackend) {
    req('POST', `${backendUrl}/ucp/v1/checkout-sessions`);
    try {
      const res = await fetch(`${backendUrl}/ucp/v1/checkout-sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(createPayload)
      });
      sessionData = await res.json();
      activeSessionId = sessionData.sessionId;
      resp(res.status, res.statusText);
      json(sessionData);
    } catch(err) {
      resp(500, "Error creating session");
    }
  } else {
    req('POST', 'https://commerceos.demo/ucp/checkout-sessions');
    appendLine('<span style="color:var(--text-muted);">Authorization: Bearer {google_ai_token}</span>', 2);
    json(createPayload);
    await delay(800);
    resp(201, 'Created');
    activeSessionId = "cs_" + Math.random().toString(36).slice(2, 9);
    sessionData = { "sessionId": activeSessionId, "status": "REQUIRES_PAYMENT", "expiresAt": new Date(Date.now() + 1800000).toISOString(), "lineItems": [{ "offerId": "SKU-IPH15-128", "title": "Apple iPhone 15 (128GB, Blue)", "unitPrice": { "value": "79900", "currency": "INR" }, "quantity": 1 }], "pricingSummary": { "subtotal": { "value": "79900", "currency": "INR" }, "taxTotal": { "value": "14382", "currency": "INR" }, "grandTotal": { "value": "94432", "currency": "INR" } }, "paymentOptions": ["GOOGLE_PAY"] };
    json(sessionData);
  }
  appendLine(`<span style="color:#f59e0b;font-size:0.7rem;">Status: REQUIRES_PAYMENT — Session ID: ${activeSessionId}</span>`, 1);
  divider();
  await delay(800);

  // ── STEP 3: Google Pay Tokenization ──
  label('STEP 3 — Google Pay Direct Authorization', '#f59e0b');
  appendLine('<span style="color:var(--text-muted);">User confirms inside Gemini interface — Google Pay tokenizes card details</span>', 1);
  await delay(600);
  const demoToken = `tok_gp_${Math.random().toString(36).slice(2,8)}`;
  appendLine(`<span style="color:#f59e0b;">↳ Google Pay Token Generated: ${demoToken}</span>`, 1);
  await delay(500);
  appendLine('<span style="color:#10b981;">Tokenization authorization confirmed</span>', 1);
  divider();
  await delay(700);

  // ── STEP 4: Complete Order ──
  label('STEP 4 — Order Settlement & Complete', '#10b981');
  appendLine('<span style="color:var(--text-muted);">Gemini submits token to merchant server to finalize order & deduct inventory</span>', 1);
  await delay(400);

  let orderData;
  const completePayload = { paymentToken: demoToken, paymentMethod: "GOOGLE_PAY" };

  if (isLiveBackend) {
    req('POST', `${backendUrl}/ucp/v1/checkout-sessions/${activeSessionId}/complete`);
    try {
      const res = await fetch(`${backendUrl}/ucp/v1/checkout-sessions/${activeSessionId}/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(completePayload)
      });
      orderData = await res.json();
      resp(res.status, res.statusText);
      json(orderData);
    } catch(err) {
      resp(500, "Error completing order");
    }
  } else {
    req('POST', `https://commerceos.demo/ucp/checkout-sessions/${activeSessionId}/complete`);
    json(completePayload);
    await delay(900);
    resp(200, 'OK');
    const orderId = 'ORD-' + Date.now().toString().slice(-6);
    orderData = { "sessionId": activeSessionId, "status": "COMPLETED", "orderId": orderId, "completedAt": new Date().toISOString() };
    json(orderData);
  }
  divider();

  // ── DONE ──
  await delay(400);
  const finalOrderId = orderData?.orderId || ('ORD-' + Date.now().toString().slice(-6));
  appendLine(`<div style="padding:14px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:8px;text-align:center;">
    <div style="color:#10b981;font-weight:800;font-size:0.85rem;">Purchase Complete — Order ${finalOrderId}</div>
    <div style="color:var(--text-muted);font-size:0.72rem;margin-top:4px;">Direct Buying complete via Google UCP Protocol.</div>
  </div>`);

  btn.disabled = false;
  btn.textContent = 'Run Protocol Simulation';
};


// ---- HERO INLINE UCP SIMULATOR (main page) ----
window.runHeroUCPSimulator = async function() {
  const area = document.getElementById('hero-sim-area');
  const btn = document.getElementById('hero-sim-btn');
  if (!area) return;
  btn.disabled = true;
  btn.textContent = '⏳ Running...';
  area.innerHTML = '';
  area.style.display = 'block';
  area.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  const delay = ms => new Promise(r => setTimeout(r, ms));

  const appendLine = (html, indent = 0) => {
    const div = document.createElement('div');
    div.style.cssText = `padding-left:${indent * 14}px; margin-bottom:3px; animation: fadeIn 0.3s ease;`;
    div.innerHTML = html;
    area.appendChild(div);
    area.scrollTop = area.scrollHeight;
  };

  const lbl = (icon, text, color) => appendLine(`<span style="color:${color};font-weight:800;">${icon} ${text}</span>`);
  const req = (m, p) => appendLine(`<span style="color:#60a5fa;">${m}</span> <span style="color:#f59e0b;">${p}</span>`, 1);
  const res = (code, msg) => appendLine(`<span style="color:${code<300?'#10b981':'#ef4444'};">← ${code} ${msg}</span>`, 1);
  const jline = (key, val, valColor='#34d399') => appendLine(`<span style="color:#a78bfa;">"${key}"</span>: <span style="color:${valColor};">${val}</span>`, 2);
  const div = () => appendLine(`<div style="border-top:1px solid rgba(255,255,255,0.05);margin:8px 0;"></div>`);

  lbl('🔍', 'STEP 1 — Discovery', '#06b6d4');
  await delay(400);
  req('GET', '/.well-known/ucp');
  await delay(700);
  res(200, 'OK');
  appendLine(`<div style="padding:6px 10px;background:rgba(0,0,0,0.4);border-radius:6px;border-left:2px solid #a78bfa;margin:4px 0 8px;">`, 1);
  jline('capabilities', '["direct_buying", "price_availability"]');
  jline('version', '"2026-04-08"');
  appendLine(`</div>`, 1);
  appendLine('<span style="color:#10b981;font-size:0.68rem;">✅ direct_buying supported</span>', 1);
  div(); await delay(700);

  lbl('🛒', 'STEP 2 — Create Checkout Session', '#a78bfa');
  await delay(400);
  req('POST', '/ucp/checkout-sessions');
  jline('offerId', '"airpods-pro-001"', '#34d399');
  jline('currency', '"INR"', '#34d399');
  await delay(900);
  const sid = 'cs_' + Math.random().toString(36).slice(2, 8);
  res(201, 'Created');
  appendLine(`<div style="padding:6px 10px;background:rgba(0,0,0,0.4);border-radius:6px;border-left:2px solid #a78bfa;margin:4px 0 8px;">`, 1);
  jline('sessionId', `"${sid}"`);
  jline('status', '"REQUIRES_PAYMENT"', '#f59e0b');
  jline('totalPrice', '{ "value": "22990", "currency": "INR" }', '#60a5fa');
  appendLine(`</div>`, 1);
  div(); await delay(800);

  lbl('💳', 'STEP 3 — Google Pay', '#f59e0b');
  await delay(300);
  appendLine('<span style="color:#f59e0b;">↳ User taps Pay ₹22,990 in Gemini...</span>', 1);
  await delay(700);
  appendLine('<span style="color:#10b981;">✅ tok_gp_1a2b3c4d tokenized</span>', 1);
  div(); await delay(600);

  lbl('✅', 'STEP 4 — Complete', '#10b981');
  await delay(400);
  req('POST', `/ucp/checkout-sessions/${sid}/complete`);
  await delay(900);
  const oid = 'ORD-' + Date.now().toString().slice(-6);
  res(200, 'OK');
  appendLine(`<div style="padding:6px 10px;background:rgba(0,0,0,0.4);border-radius:6px;border-left:2px solid #10b981;margin:4px 0 8px;">`, 1);
  jline('status', '"COMPLETED"', '#10b981');
  jline('orderId', `"${oid}"`);
  appendLine(`</div>`, 1);
  div();
  await delay(300);
  appendLine(`<div style="padding:10px 14px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);border-radius:8px;text-align:center;">
    <span style="font-size:1rem;">🎉</span>
    <span style="color:#10b981;font-weight:800;font-size:0.8rem;margin-left:8px;">Order ${oid} — User never left Gemini</span>
  </div>`);

  btn.disabled = false;
  btn.textContent = '▶ Simulate Again';
};
</script>
'''

if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 1. Inject CSS
    css_insert_point = content.find('</style>')
    if css_insert_point != -1:
        content = content[:css_insert_point] + TABS_CSS + content[css_insert_point:]
        
    # 2. Replace STUBS with TABS_HTML
    # Strategy A: Find the STUBS comment + the 3 stub divs
    stub_pattern = re.compile(r'<!-- STUBS FOR OTHER MODES.*?-->\n(?:<div class="page" id="page-(?:developer|architecture|ucp)".*?</div>\n)+', re.DOTALL)
    
    if stub_pattern.search(content):
        content = stub_pattern.sub(TABS_HTML + "\n", content)
        print("  Tabs injected via STUBS comment pattern.")
    else:
        # Strategy B: Find each stub div by ID and replace all 3 at once
        # Find first stub div start
        d_start = content.find('<div class="page" id="page-developer">')
        # Find end of the last stub (page-ucp), accounting for single-line format
        u_marker = '<div class="page" id="page-ucp">'
        u_pos = content.find(u_marker)
        if d_start != -1 and u_pos != -1:
            # Find the closing </div> after page-ucp
            # These stubs are simple single-level divs
            end_search = content.find('<!-- TOAST', u_pos)
            if end_search == -1:
                end_search = content.find('<div id="toast"', u_pos)
            if end_search != -1:
                content = content[:d_start] + TABS_HTML + "\n\n" + content[end_search:]
                print("  Tabs injected via ID-based stub replacement.")
            else:
                content = content + "\n" + TABS_HTML
                print("  Warning: Appended TABS_HTML at end (fallback).")
        else:
            print("  Warning: Could not locate stub divs. Appending TABS_HTML.")
            content = content + "\n" + TABS_HTML
        
    # 3. Inject TABS_JS — try before </body>, fall back to appending at end
    js_insert_point = content.find('</body>')
    if js_insert_point != -1:
        content = content[:js_insert_point] + TABS_JS + "\n" + content[js_insert_point:]
    else:
        # No </body> tag — append at end of file
        content = content + "\n" + TABS_JS
        print("Note: No </body> tag found — TABS_JS appended at end of file.")
        
    with open(filepath, 'w') as f:
        f.write(content)
        
    print("Part 5 (V2 Tabs) built and injected successfully.")
