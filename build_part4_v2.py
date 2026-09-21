#!/usr/bin/env python3
"""Build Part 4 (V2): Chat Agent UI Controller"""

import os

UI_JS = r'''
<!-- PART 4: UI CONTROLLER V2 — CHAT AGENT -->
<script>
'use strict';

window.UI = {
  _thinkSteps: null,

  init() {
    this.bindNavigation();
    this.bindInput();
    this.showGreeting();
  },

  bindNavigation() {
    document.querySelectorAll('.nav-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        const page = btn.dataset.page;
        document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const pageEl = document.getElementById('page-' + page);
        if (pageEl) setTimeout(() => pageEl.classList.add('active'), 50);
      });
    });
    const modal = document.getElementById('settings-modal');
    const kinput = document.getElementById('gemini-key-input');
    document.getElementById('settings-btn')?.addEventListener('click', () => { kinput.value = localStorage.getItem('gemini_api_key') || ''; modal.style.display = 'flex'; });
    document.getElementById('settings-close-btn')?.addEventListener('click', () => { modal.style.display = 'none'; });
    document.getElementById('settings-save-btn')?.addEventListener('click', () => { const v = kinput.value.trim(); if(v){localStorage.setItem('gemini_api_key',v);showToast('API Key saved');} modal.style.display='none'; });
    document.getElementById('settings-clear-btn')?.addEventListener('click', () => { localStorage.removeItem('gemini_api_key'); kinput.value=''; showToast('API Key cleared'); });
  },

  bindInput() {
    const input = document.getElementById('main-query-input');
    const sendBtn = document.getElementById('run-agent-btn');
    sendBtn?.addEventListener('click', () => this.runAgent());
    input?.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) this.runAgent(); });
    document.querySelectorAll('.qp-chip').forEach(chip => {
      if (chip.id === 'hero-ucp-chip') {
        chip.addEventListener('click', () => {
          this.appendAgentMessage('<span style="color:#06b6d4;font-weight:700;">⚡ Launching UCP Protocol Simulator...</span><br/><span style="font-size:0.75rem;color:var(--text-muted);">Watch how Gemini buys via the real Google UCP in 4 steps.</span>');
          setTimeout(() => { document.querySelector('[data-page=ucp]')?.click(); setTimeout(() => window.runUCPSimulator?.(), 400); }, 800);
        });
      } else {
        chip.addEventListener('click', () => {
          const inp = document.getElementById('main-query-input');
          if (inp) { inp.value = chip.dataset.query; this.runAgent(); }
        });
      }
    });
  },

  showGreeting() {
    const msgs = document.getElementById('chat-messages');
    if (!msgs) return;
    const row = document.createElement('div');
    row.className = 'chat-row';
    row.innerHTML = `
      <div class="chat-avatar agent-avatar">AI</div>
      <div class="chat-bubble agent-bubble">
        <div style="font-weight:700;color:white;margin-bottom:6px;">CommerceOS Agentic Commerce Assistant</div>
        <div style="font-size:0.8rem;color:var(--text-muted);line-height:1.65;">
          Searches catalog candidates, parses natural language constraints, applies hard &amp; soft boundary filters, and ranks results across <span style="color:#a78bfa;">6 dimensions</span>.<br/>
          <span style="font-size:0.75rem;color:#f59e0b;">[Demonstration catalog &amp; live DummyJSON integration]</span><br/><br/>
          Enter a prompt like <span style="color:white;font-weight:600;">"Sony headphones under ₹10k"</span> or select a query below.
        </div>
        <div style="margin-top:10px;padding:8px 10px;background:rgba(6,182,212,0.07);border:1px solid rgba(6,182,212,0.2);border-radius:8px;font-size:0.72rem;color:#06b6d4;">
          Google Universal Commerce Protocol (UCP) enabled — click <strong>"Simulate UCP Buy"</strong> to run direct protocol checkout.
        </div>
      </div>`;
    msgs.appendChild(row);
  },

  appendUserMessage(text) {
    const msgs = document.getElementById('chat-messages');
    if (!msgs) return;
    const row = document.createElement('div');
    row.className = 'chat-row user-row';
    row.innerHTML = `<div class="chat-avatar user-avatar" style="font-size:0.6rem;font-weight:800;color:#a78bfa;">YOU</div><div class="chat-bubble user-bubble">${text}</div>`;
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
  },

  appendAgentMessage(html) {
    const msgs = document.getElementById('chat-messages');
    if (!msgs) return;
    const row = document.createElement('div');
    row.className = 'chat-row';
    row.innerHTML = `<div class="chat-avatar agent-avatar">AI</div><div class="chat-bubble agent-bubble">${html}</div>`;
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
    return row;
  },

  startThinkingBubble() {
    const msgs = document.getElementById('chat-messages');
    if (!msgs) return;
    document.getElementById('thinking-bubble')?.remove();
    const row = document.createElement('div');
    row.className = 'chat-row';
    row.id = 'thinking-bubble';
    row.innerHTML = `
      <div class="chat-avatar agent-avatar">AI</div>
      <div class="chat-bubble agent-bubble">
        <div class="typing-dots"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>
        <div id="agent-think-steps" style="margin-top:4px;"></div>
      </div>`;
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
    this._thinkSteps = row.querySelector('#agent-think-steps');
  },

  removeThinkingBubble() {
    document.getElementById('thinking-bubble')?.remove();
    this._thinkSteps = null;
  },

  async logTerminal(msg, type = 'system') {
    if (!this._thinkSteps) return;
    const line = document.createElement('div');
    const cls = type === 'success' ? 's-success' : type === 'highlight' ? 's-highlight' : 's-system';
    line.className = `agent-step ${cls}`;
    line.textContent = msg;
    this._thinkSteps.appendChild(line);
    const dots = document.querySelector('#thinking-bubble .typing-dots');
    if (dots) dots.style.display = 'none';
    const msgs = document.getElementById('chat-messages');
    if (msgs) msgs.scrollTop = msgs.scrollHeight;
    await new Promise(r => setTimeout(r, 30 + Math.random() * 40));

    if (msg.includes('Intent extracted')) { this._dot('step-parse','done'); this._dot('step-search','active'); }
    else if (msg.includes('Retrieved') && msg.includes('candidates')) { this._dot('step-search','done'); this._dot('step-filter','active'); }
    else if (msg.includes('Applying hard constraints')) { this._dot('step-filter','done'); this._dot('step-rank','active'); }
    else if (msg.includes('Session Complete')) { this._dot('step-rank','done'); }
  },

  _dot(id, state) { const d = document.getElementById(id); if(d) d.className='step-dot '+state; },

  _resetDots() {
    ['step-parse','step-search','step-filter','step-rank'].forEach(id => this._dot(id,'pending'));
    this._dot('step-parse','active');
  },

  async runAgent() {
    const queryInput = document.getElementById('main-query-input');
    const query = queryInput?.value?.trim();
    if (!query) { showToast('Type something first!'); return; }
    document.getElementById('run-agent-btn').disabled = true;
    queryInput.value = '';

    const sidebar = document.getElementById('brain-sidebar');
    if (sidebar) sidebar.style.display = 'block';
    this._resetDots();

    this.appendUserMessage(query);
    this.startThinkingBubble();

    try {
      await AGENT.run(query);
    } catch(e) {
      this.removeThinkingBubble();
      this.appendAgentMessage(`<span style="color:#ef4444;">Error: ${e.message}</span>`);
    } finally {
      document.getElementById('run-agent-btn').disabled = false;
    }
  },

  renderResults(ranked, intent, hardFailures) {
    this.removeThinkingBubble();
    this._updateBrain(intent, ranked, hardFailures);

    if (ranked.length === 0) {
      this.appendAgentMessage(`<span style="color:#f59e0b;">No products matched.</span><br/><span style="font-size:0.78rem;color:var(--text-muted);">Try a broader search query or higher budget.</span>`);
      return;
    }

    const msgs = document.getElementById('chat-messages');
    const rejCount = (hardFailures || []).length;
    const summaryRow = document.createElement('div');
    summaryRow.className = 'chat-row';
    summaryRow.innerHTML = `
      <div class="chat-avatar agent-avatar">AI</div>
      <div class="chat-bubble agent-bubble" style="max-width:88%;width:88%;">
        <div style="margin-bottom:8px;">
          <span style="color:#10b981;font-weight:700;">Found ${ranked.length} match${ranked.length>1?'es':''}</span>
          ${rejCount > 0 ? `<span style="color:var(--text-muted);font-size:0.75rem;margin-left:6px;">(${rejCount} filtered by constraints)</span>` : ''}
          <span style="color:var(--text-muted);font-size:0.75rem;margin-left:6px;">Best Score: <span style="color:#a78bfa;font-weight:700;">${ranked[0].total_score}%</span></span>
        </div>
        <div id="inline-products-container"></div>
        <div style="margin-top:8px;font-size:0.72rem;color:var(--text-muted);">Click Amazon/Flipkart for real merchant listings. Click <strong>Buy via UCP</strong> to test protocol checkout.</div>
      </div>`;
    msgs.appendChild(summaryRow);

    const container = summaryRow.querySelector('#inline-products-container');
    ranked.forEach((item, idx) => {
      const p = item.product;
      const cleanBrand = p.brand && p.brand !== 'Generic' ? p.brand : '';
      const hasBrand = cleanBrand && p.title.toLowerCase().includes(cleanBrand.toLowerCase());
      const queryStr = hasBrand ? p.title : (cleanBrand ? `${cleanBrand} ${p.title}` : p.title);
      const aq = encodeURIComponent(queryStr.trim());
      const amazonUrl = `https://www.amazon.in/s?k=${aq}&ref=commerceos_ai`;
      const flipkartUrl = `https://www.flipkart.com/search?q=${aq}`;
      const bd = item.breakdown || {};
      const budgetOk = (bd.budget_fit?.pct || 0) >= 0.85;
      const budgetWarn = (bd.budget_fit?.pct || 0) >= 0.5;

      const card = document.createElement('div');
      card.innerHTML = `
        <div class="inline-product" onclick="window.open('${amazonUrl}','_blank')" style="opacity:0;transition:opacity 0.3s;">
          ${p.image
            ? `<img class="ip-img" src="${p.image}" alt="${p.title}" onerror="this.style.display='none';this.nextSibling.style.display='flex';" /><div class="ip-img" style="display:none;align-items:center;justify-content:center;font-size:1.1rem;color:var(--text-muted);">[IMG]</div>`
            : `<div class="ip-img" style="display:flex;align-items:center;justify-content:center;font-size:1.1rem;color:var(--text-muted);">[IMG]</div>`}
          <div class="ip-info">
            <div class="ip-title">${idx===0?'[Top Pick] ':''}${p.title}</div>
            <div class="ip-meta">${p.brand} · ★${(p.rating||4.0).toFixed(1)} ${budgetOk?'<span style="color:#10b981;">Budget Fit</span>':budgetWarn?'<span style="color:#f59e0b;">~Budget</span>':'<span style="color:#ef4444;">Over Budget</span>'}</div>
            <div style="display:flex;gap:6px;align-items:center;margin-top:2px;">
              <span style="font-size:0.8rem;font-weight:800;color:#10b981;">₹${item.price.toLocaleString('en-IN')}</span>
              <span class="ip-score">${item.total_score}% match</span>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:4px;flex-shrink:0;">
            <button onclick="event.stopPropagation(); UI.triggerUcpCheckout('${p.title.replace(/'/g,"\\'")}', ${item.price})" style="background:linear-gradient(135deg,#06b6d4,#7c3aed);color:white;border:none;border-radius:8px;padding:6px 10px;font-size:0.72rem;font-weight:700;cursor:pointer;white-space:nowrap;box-shadow:0 0 10px rgba(6,182,212,0.3);transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">Buy via UCP</button>
            <div style="display:flex;gap:4px;justify-content:center;">
              <a href="${amazonUrl}" target="_blank" rel="noopener" style="font-size:0.62rem;color:#f90;text-decoration:none;" onclick="event.stopPropagation()">Amazon ↗</a>
              <span style="font-size:0.62rem;color:var(--text-muted);">·</span>
              <a href="${flipkartUrl}" target="_blank" rel="noopener" style="font-size:0.62rem;color:#2874f0;text-decoration:none;" onclick="event.stopPropagation()">Flipkart ↗</a>
            </div>
          </div>
        </div>`;
      container.appendChild(card);
      setTimeout(() => { const ip = card.querySelector('.inline-product'); if(ip) ip.style.opacity='1'; }, idx * 130 + 100);
    });

    msgs.scrollTop = msgs.scrollHeight;
  },

  async triggerUcpCheckout(title, price) {
    const cleanTitle = title.replace(/'/g, "");
    this.appendUserMessage(`Buy ${cleanTitle} via Google UCP (₹${price.toLocaleString('en-IN')})`);
    this.startThinkingBubble();
    const delay = ms => new Promise(r => setTimeout(r, ms));
    await delay(300);
    this.removeThinkingBubble();

    const sid = 'cs_' + Math.random().toString(36).slice(2, 9);
    const oid = 'ORD-' + Date.now().toString().slice(-6);

    const msgs = document.getElementById('chat-messages');
    const ucpRow = document.createElement('div');
    ucpRow.className = 'chat-row';
    const cardId = 'ucp-card-' + Date.now();

    ucpRow.innerHTML = `
      <div class="chat-avatar agent-avatar">UCP</div>
      <div class="chat-bubble agent-bubble" id="${cardId}" style="max-width:96%;width:96%;background:rgba(8,12,24,0.96);border:1px solid rgba(6,182,212,0.4);box-shadow:0 0 35px rgba(6,182,212,0.2);">
        
        <!-- HEADER -->
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid rgba(255,255,255,0.08);">
          <div style="display:flex;align-items:center;gap:8px;">
            <div>
              <span style="color:#06b6d4;font-weight:800;font-size:0.85rem;letter-spacing:0.5px;">GOOGLE UCP DIRECT CHECKOUT SIMULATOR</span>
              <div style="font-size:0.68rem;color:var(--text-muted);">Real-time simulation of direct buying protocol execution and Google Pay token authorization</div>
            </div>
          </div>
          <span style="font-size:0.8rem;font-family:'JetBrains Mono',monospace;color:#06b6d4;font-weight:800;" id="${cardId}-pct">0%</span>
        </div>

        <!-- DUAL-PANEL LAYOUT: PHONE (LEFT) + TERMINAL TRACE (RIGHT) -->
        <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start;">
          
          <!-- LEFT PANEL: PHONE MOCKUP -->
          <div class="phone-mockup" style="box-shadow:0 0 35px rgba(6,182,212,0.35), 0 15px 40px rgba(0,0,0,0.85);margin:0 auto;">
            <div class="phone-notch"><div class="phone-notch-dot"></div></div>
            <div class="phone-status-bar">
              <span>10:42 AM</span>
              <span>5G 98%</span>
            </div>
            <div class="phone-screen" id="${cardId}-phone-screen">
              <div style="padding:10px;height:100%;display:flex;flex-direction:column;justify-content:space-between;position:relative;background:linear-gradient(180deg,#0a0a16 0%,#121226 100%);box-sizing:border-box;">
                
                <!-- TOP GEMINI HEADER IN PHONE -->
                <div>
                  <div style="display:flex;align-items:center;justify-content:space-between;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:8px;">
                    <div style="display:flex;align-items:center;gap:5px;">
                      <div style="width:18px;height:18px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:0.55rem;font-weight:800;color:white;">AI</div>
                      <span style="font-size:0.7rem;font-weight:800;color:white;">Gemini AI</span>
                    </div>
                    <span style="font-size:0.55rem;background:rgba(6,182,212,0.2);color:#06b6d4;padding:1px 5px;border-radius:4px;font-weight:700;">UCP Protocol</span>
                  </div>

                  <!-- USER BUBBLE IN PHONE -->
                  <div style="background:rgba(124,58,237,0.25);border:1px solid rgba(124,58,237,0.4);padding:6px 8px;border-radius:8px 8px 2px 8px;font-size:0.64rem;color:white;margin-bottom:8px;max-width:88%;margin-left:auto;text-align:right;">
                    Buy ${cleanTitle}
                  </div>

                  <!-- ITEM SNAPSHOT IN PHONE -->
                  <div id="${cardId}-phone-item" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:8px;font-size:0.64rem;transition:all 0.3s;">
                    <div style="font-weight:700;color:white;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${cleanTitle}</div>
                    <div style="color:#10b981;font-weight:800;font-size:0.75rem;margin-top:2px;">₹${price.toLocaleString('en-IN')}</div>
                    <div style="margin-top:4px;display:flex;align-items:center;justify-content:space-between;">
                      <span style="color:var(--text-muted);font-size:0.58rem;">CommerceOS Direct</span>
                      <span id="${cardId}-phone-status-tag" style="background:rgba(6,182,212,0.2);color:#06b6d4;padding:1px 5px;border-radius:4px;font-size:0.55rem;font-weight:700;">Discovery...</span>
                    </div>
                  </div>
                </div>

                <!-- MIDDLE SCREEN ANIMATION BODY -->
                <div id="${cardId}-phone-body" style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:8px 0;text-align:center;">
                  <div id="${cardId}-phone-icon" style="width:40px;height:40px;border-radius:50%;border:2px dashed #06b6d4;animation:spin 3s linear infinite;display:flex;align-items:center;justify-content:center;font-size:0.7rem;font-weight:800;color:#06b6d4;margin-bottom:6px;background:rgba(6,182,212,0.1);">UCP</div>
                  <div id="${cardId}-phone-step-text" style="font-size:0.68rem;color:#06b6d4;font-weight:800;">1. Discovering UCP Profile</div>
                  <div id="${cardId}-phone-subtext" style="font-size:0.58rem;color:var(--text-muted);margin-top:2px;">GET /.well-known/ucp</div>
                </div>

                <!-- GOOGLE PAY BOTTOM SHEET INSIDE PHONE -->
                <div id="${cardId}-gpay-sheet" class="gpay-sheet">
                  <div style="width:32px;height:3px;background:rgba(255,255,255,0.2);border-radius:2px;margin:0 auto 8px;"></div>
                  
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                    <span style="font-weight:900;font-size:0.82rem;letter-spacing:-0.5px;color:white;"><span style="color:#4285F4;">G</span><span style="color:#EA4335;">o</span><span style="color:#FBBC05;">o</span><span style="color:#4285F4;">g</span><span style="color:#34A853;">l</span><span style="color:#EA4335;">e</span> Pay</span>
                    <span style="font-size:0.55rem;background:rgba(16,185,129,0.2);color:#10b981;padding:1px 5px;border-radius:4px;font-weight:700;">UCP Tokenization</span>
                  </div>

                  <div style="background:rgba(255,255,255,0.06);border-radius:8px;padding:8px;margin-bottom:8px;">
                    <div style="font-size:0.58rem;color:var(--text-muted);">Paying Merchant</div>
                    <div style="font-size:0.68rem;font-weight:700;color:white;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${cleanTitle}</div>
                    <div style="font-size:0.85rem;font-weight:900;color:#10b981;margin-top:2px;">₹${price.toLocaleString('en-IN')}</div>
                  </div>

                  <div style="background:rgba(255,255,255,0.04);border:1px dashed rgba(255,255,255,0.12);border-radius:8px;padding:6px 8px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;">
                    <div style="display:flex;align-items:center;gap:5px;">
                      <span style="font-size:0.65rem;color:#a78bfa;font-weight:700;">[CARD]</span>
                      <div>
                        <div style="font-size:0.62rem;font-weight:700;color:white;">HDFC Visa •••• 4242</div>
                        <div style="font-size:0.54rem;color:var(--text-muted);">Saved Payment Method</div>
                      </div>
                    </div>
                    <span style="font-size:0.6rem;color:#06b6d4;font-weight:700;">Ready</span>
                  </div>

                  <div id="${cardId}-bio-box" style="background:linear-gradient(135deg,#06b6d4,#7c3aed);color:white;border-radius:8px;padding:8px;font-size:0.68rem;font-weight:800;text-align:center;display:flex;align-items:center;justify-content:center;gap:5px;box-shadow:0 0 15px rgba(6,182,212,0.4);">
                    <span id="${cardId}-bio-icon" style="font-size:0.75rem;font-weight:800;">[LOCK]</span> 
                    <span id="${cardId}-bio-text">Confirm Token Authorization</span>
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- RIGHT PANEL: REAL-TIME PROTOCOL TRACE -->
          <div style="flex:1;min-width:280px;height:480px;display:flex;flex-direction:column;background:rgba(0,0,0,0.55);border:1px solid rgba(255,255,255,0.08);border-radius:18px;padding:12px;box-sizing:border-box;overflow:hidden;">
            
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid rgba(255,255,255,0.06);">
              <span style="font-family:'JetBrains Mono',monospace;font-size:0.72rem;color:#06b6d4;font-weight:800;">LIVE PROTOCOL STREAM</span>
              <span style="font-size:0.65rem;color:var(--text-muted);font-family:'JetBrains Mono',monospace;">UCP Spec v2026</span>
            </div>

            <!-- PROGRESS BAR -->
            <div style="width:100%;height:4px;background:rgba(255,255,255,0.08);border-radius:4px;margin-bottom:10px;overflow:hidden;">
              <div id="${cardId}-progress" style="width:0%;height:100%;background:linear-gradient(90deg,#06b6d4,#7c3aed,#10b981);transition:width 0.4s ease;"></div>
            </div>

            <!-- STEP BADGES -->
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4px;margin-bottom:10px;font-size:0.62rem;text-align:center;">
              <div id="${cardId}-step1-badge" style="padding:4px 2px;border-radius:4px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-muted);transition:all 0.3s;">1. Discovery</div>
              <div id="${cardId}-step2-badge" style="padding:4px 2px;border-radius:4px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-muted);transition:all 0.3s;">2. Session</div>
              <div id="${cardId}-step3-badge" style="padding:4px 2px;border-radius:4px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-muted);transition:all 0.3s;">3. Token</div>
              <div id="${cardId}-step4-badge" style="padding:4px 2px;border-radius:4px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:var(--text-muted);transition:all 0.3s;">4. Complete</div>
            </div>

            <!-- LIVE STREAM TERMINAL CONTENT -->
            <div id="${cardId}-stream" style="flex:1;font-family:'JetBrains Mono',monospace;font-size:0.71rem;line-height:1.65;overflow-y:auto;padding-right:4px;"></div>

            <!-- FINAL BANNER CONTAINER -->
            <div id="${cardId}-banner" style="display:none;margin-top:8px;animation:slideUp 0.3s ease;"></div>
          </div>

        </div>
      </div>`;

    msgs.appendChild(ucpRow);
    msgs.scrollTop = msgs.scrollHeight;

    const stream = document.getElementById(`${cardId}-stream`);
    const progress = document.getElementById(`${cardId}-progress`);
    const pct = document.getElementById(`${cardId}-pct`);

    const phoneIcon = document.getElementById(`${cardId}-phone-icon`);
    const phoneStepText = document.getElementById(`${cardId}-phone-step-text`);
    const phoneSubtext = document.getElementById(`${cardId}-phone-subtext`);
    const phoneTag = document.getElementById(`${cardId}-phone-status-tag`);
    const gpaySheet = document.getElementById(`${cardId}-gpay-sheet`);
    const bioText = document.getElementById(`${cardId}-bio-text`);
    const bioIcon = document.getElementById(`${cardId}-bio-icon`);
    const bioBox = document.getElementById(`${cardId}-bio-box`);
    const phoneBody = document.getElementById(`${cardId}-phone-body`);

    const logLine = (html) => {
      const d = document.createElement('div');
      d.style.cssText = 'margin-bottom:3px;animation:fadeIn 0.3s ease;';
      d.innerHTML = html;
      stream.appendChild(d);
      stream.scrollTop = stream.scrollHeight;
    };

    const setStep = (num, colorHex) => {
      const badge = document.getElementById(`${cardId}-step${num}-badge`);
      if (badge) {
        badge.style.background = `rgba(${colorHex},0.25)`;
        badge.style.borderColor = `rgba(${colorHex},0.6)`;
        badge.style.color = 'white';
        badge.style.fontWeight = '800';
      }
      progress.style.width = `${num * 25}%`;
      pct.textContent = `${num * 25}%`;
    };

    // STEP 1: DISCOVERY
    setStep(1, '6,182,212');
    logLine('<span style="color:#06b6d4;font-weight:800;">STEP 1 — Merchant UCP Capability Discovery</span>');
    await delay(300);
    logLine('<span style="color:#60a5fa;">GET</span> <span style="color:#f59e0b;">/.well-known/ucp</span>');
    await delay(600);
    logLine('<span style="color:#10b981;">← 200 OK</span> <span style="color:var(--text-muted);">{ "name": "CommerceOS", "capabilities": ["direct_buying"] }</span>');
    logLine('<span style="color:#34d399;font-size:0.66rem;">Merchant capability verified: direct_buying active</span>');

    if (phoneStepText) phoneStepText.textContent = '1. Merchant Verified';
    if (phoneSubtext) phoneSubtext.textContent = 'direct_buying capability active';
    if (phoneTag) { phoneTag.textContent = 'Verified'; phoneTag.style.background = 'rgba(16,185,129,0.2)'; phoneTag.style.color = '#10b981'; }
    if (phoneIcon) { phoneIcon.textContent = 'OK'; phoneIcon.style.borderStyle = 'solid'; phoneIcon.style.borderColor = '#10b981'; phoneIcon.style.animation = 'none'; }

    // STEP 2: SESSION CREATION
    await delay(800);
    setStep(2, '167,139,250');
    logLine('<div style="border-top:1px solid rgba(255,255,255,0.06);margin:6px 0;"></div>');
    logLine('<span style="color:#a78bfa;font-weight:800;">STEP 2 — Creating UCP Checkout Session</span>');
    await delay(300);
    logLine(`<span style="color:#60a5fa;">POST</span> <span style="color:#f59e0b;">/ucp/checkout-sessions</span>`);
    logLine(`<span style="color:var(--text-muted);padding-left:10px;">Payload: { offerId: "${cleanTitle}", qty: 1 }</span>`);
    await delay(700);
    logLine(`<span style="color:#10b981;">← 201 Created</span> <span style="color:#f59e0b;">Status: REQUIRES_PAYMENT | ID: ${sid}</span>`);

    if (phoneStepText) { phoneStepText.textContent = '2. Session Locked'; phoneStepText.style.color = '#a78bfa'; }
    if (phoneSubtext) phoneSubtext.textContent = `ID: ${sid} · Ready for Payment`;
    if (phoneIcon) { phoneIcon.textContent = 'LOCK'; phoneIcon.style.borderColor = '#a78bfa'; }

    // STEP 3: GOOGLE PAY BOTTOM SHEET SLIDE UP
    await delay(900);
    setStep(3, '245,158,11');
    logLine('<div style="border-top:1px solid rgba(255,255,255,0.06);margin:6px 0;"></div>');
    logLine('<span style="color:#f59e0b;font-weight:800;">STEP 3 — Google Pay Direct Authorization</span>');
    await delay(400);
    logLine(`<span style="color:var(--text-muted);">↳ Sliding up Google Pay bottom sheet in phone...</span>`);

    if (gpaySheet) gpaySheet.classList.add('show');
    await delay(600);

    logLine(`<span style="color:var(--text-muted);">↳ Payment token authorization in progress...</span>`);
    await delay(800);

    if (bioIcon) bioIcon.textContent = '[...]';
    if (bioText) bioText.textContent = 'Verifying Token...';

    await delay(700);
    if (bioIcon) { bioIcon.textContent = '[OK]'; bioIcon.style.animation = 'none'; }
    if (bioText) bioText.textContent = 'Authorized';
    if (bioBox) bioBox.style.background = 'linear-gradient(135deg,#10b981,#059669)';

    logLine(`<span style="color:#10b981;">Payment tokenized: tok_gp_${sid.slice(-5)}</span>`);

    // STEP 4: COMPLETE ORDER & ORDER CONFIRMATION IN PHONE
    await delay(900);
    setStep(4, '16,185,129');
    logLine('<div style="border-top:1px solid rgba(255,255,255,0.06);margin:6px 0;"></div>');
    logLine('<span style="color:#10b981;font-weight:800;">STEP 4 — Order Settlement Complete</span>');
    await delay(300);
    logLine(`<span style="color:#60a5fa;">POST</span> <span style="color:#f59e0b;">/ucp/checkout-sessions/${sid}/complete</span>`);
    await delay(700);
    logLine(`<span style="color:#10b981;">← 200 OK</span> <span style="color:#34d399;font-weight:800;">{ status: "COMPLETED", orderId: "${oid}" }</span>`);

    if (gpaySheet) gpaySheet.classList.remove('show');
    await delay(300);

    if (phoneBody) {
      phoneBody.innerHTML = `
        <div style="animation:slideUp 0.4s ease;text-align:center;">
          <div style="width:44px;height:44px;border-radius:50%;background:rgba(16,185,129,0.2);border:2px solid #10b981;display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:800;margin:0 auto 8px;color:#10b981;">OK</div>
          <div style="color:#10b981;font-weight:900;font-size:0.75rem;">ORDER CONFIRMED</div>
          <div style="color:white;font-weight:800;font-size:0.65rem;margin-top:2px;">${oid}</div>
          <div style="color:var(--text-muted);font-size:0.56rem;margin-top:4px;">Delivery: Estimated 1-2 Days</div>
          <div style="margin-top:6px;padding:4px 6px;background:rgba(6,182,212,0.15);border:1px solid rgba(6,182,212,0.3);border-radius:6px;font-size:0.55rem;color:#06b6d4;font-weight:700;">
            Purchased via Google UCP Token
          </div>
        </div>`;
    }

    await delay(300);
    const banner = document.getElementById(`${cardId}-banner`);
    if (banner) {
      banner.style.display = 'block';
      banner.innerHTML = `
        <div style="padding:10px;background:linear-gradient(135deg,rgba(16,185,129,0.18),rgba(6,182,212,0.12));border:1px solid rgba(16,185,129,0.4);border-radius:10px;text-align:center;">
          <div style="color:#10b981;font-weight:900;font-size:0.82rem;">Order ${oid} Confirmed</div>
          <div style="color:var(--text-secondary);font-size:0.7rem;margin-top:2px;">Item: <strong style="color:white;">${cleanTitle}</strong> (₹${price.toLocaleString('en-IN')})</div>
          <div style="color:#06b6d4;font-size:0.65rem;font-weight:700;margin-top:4px;">Direct Buying via Google UCP Protocol</div>
        </div>`;
    }

    msgs.scrollTop = msgs.scrollHeight;
  },


  _updateBrain(intent, ranked, hardFailures) {
    if (!intent) return;
    const budgetStr = intent.budget?.max ? `≤ ₹${intent.budget.max.toLocaleString('en-IN')}` : 'No limit';
    const brandStr = intent.brand_preference?.length > 0 ? intent.brand_preference.join(', ') : 'Any';
    const kw = intent.keywords?.slice(0,3).join(', ') || '—';

    const intentSec = document.getElementById('brain-intent-section');
    const intentRows = document.getElementById('brain-intent-rows');
    if (intentSec && intentRows) {
      intentSec.style.display = 'block';
      intentRows.innerHTML = [
        ['Category', intent.category||'general', '#06b6d4'],
        ['Budget', budgetStr, '#10b981'],
        ['Brand', brandStr, 'white'],
        ['Keywords', kw, '#f59e0b'],
        ['Confidence', (intent.confidence||80)+'%', '#a78bfa'],
      ].map(([k,v,c])=>`<div class="brain-row"><span class="brain-key">${k}</span><span class="brain-val" style="color:${c};">${v}</span></div>`).join('');
    }

    if (ranked.length > 0) {
      const top = ranked[0]; const bd = top.breakdown || {};
      const ss = document.getElementById('brain-score-section');
      if (ss) ss.style.display = 'block';
      const sn = document.getElementById('brain-score-name');
      if (sn) { sn.textContent = top.product.title; sn.title = top.product.title; }
      const ts = document.getElementById('brain-total-score');
      if (ts) ts.textContent = top.total_score + '%';
      const sb = document.getElementById('brain-score-bars');
      if (sb) sb.innerHTML = [
        ['Category', bd.requirement_match?.pct||0, '#a78bfa'],
        ['Budget', bd.budget_fit?.pct||0, '#10b981'],
        ['Use Case', bd.use_case?.pct||0, '#06b6d4'],
        ['Rating', bd.rating?.pct||0, '#f59e0b'],
        ['Delivery', bd.delivery?.pct||0, '#3b82f6'],
        ['Stock', bd.inventory?.pct||0, '#34d399'],
      ].map(([l,p,c])=>`<div class="brain-bar-row"><div class="brain-bar-label"><span style="color:var(--text-muted);">${l}</span><span style="color:${c};font-weight:700;">${Math.round(p*100)}%</span></div><div class="brain-bar-track"><div class="brain-bar-fill" style="width:${Math.round(p*100)}%;background:${c};"></div></div></div>`).join('');
    }

    const st = document.getElementById('brain-stats-section');
    const sr = document.getElementById('brain-stats-rows');
    if (st && sr) {
      st.style.display = 'block';
      const rej = (hardFailures||[]).length;
      sr.innerHTML = `<div class="brain-row"><span class="brain-key">Matched</span><span class="brain-val" style="color:#10b981;">✅ ${ranked.length}</span></div><div class="brain-row"><span class="brain-key">Rejected</span><span class="brain-val" style="color:#ef4444;">❌ ${rej}</span></div><div class="brain-row"><span class="brain-key">Best Score</span><span class="brain-val" style="color:#a78bfa;">${ranked[0]?.total_score||0}%</span></div>`;
    }
  },

  // Legacy stubs
  updateAgentState() {},
  renderCart() {},
  renderOrderTimeline() {},
};

document.addEventListener('DOMContentLoaded', () => {
  UI.init();
  console.log('CommerceOS UI V2 initialized.');
});
</script>
'''

if __name__ == '__main__':
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    with open(filepath, 'a') as f:
        f.write(UI_JS)
    print(f"Part 4 V2 written: Animated UI Controller. File size: {len(open(filepath).read()):,} bytes")
