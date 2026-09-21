#!/usr/bin/env python3
"""Build Part 4: UI Controller - all rendering, interaction handlers, and view logic"""

UI_JS = r'''
<!-- PART 4: UI CONTROLLER -->
<script>
'use strict';
/* ================================================
   COMMERCEOS — UI CONTROLLER
   All view rendering and user interaction logic
   ================================================ */

// ---- PIPELINE STAGE DEFINITIONS ----
const PIPELINE_STAGES = [
  { id: 'intent', name: 'Parse Request', desc: 'NLP intent extraction' },
  { id: 'discovery', name: 'Build Intent', desc: 'Structured query construction' },
  { id: 'filter', name: 'Search Catalog', desc: 'Semantic product retrieval' },
  { id: 'inventory', name: 'Apply Constraints', desc: 'Hard + soft filtering' },
  { id: 'rank', name: 'Check Inventory', desc: 'Real-time stock verification' },
  { id: 'recommend', name: 'Rank Candidates', desc: 'Weighted scoring algorithm' },
  { id: 'cart', name: 'Generate Recommendation', desc: 'Explainable selection' },
  { id: 'checkout', name: 'Cart Ready', desc: 'Add to cart for checkout' },
  { id: 'order', name: 'Checkout', desc: 'UCP-aligned checkout session' }
];

// ---- UI CONTROLLER ----
const UI = {
  selectedForComparison: new Set(),
  _pipelineStatus: {},
  _pipelineLatencies: {},

  init() {
    this.renderPipelineTrack();
    this.bindNavigation();
    this.bindHero();
    this.renderDeveloperMode();
    this.renderArchitectureMode();
    this.renderUCPExplorer();
  },

  // ---- NAVIGATION ----
  bindNavigation() {
    document.querySelectorAll('.nav-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        const page = btn.dataset.page;
        document.querySelectorAll('.nav-tab').forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
        btn.classList.add('active'); btn.setAttribute('aria-selected','true');
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const pageEl = document.getElementById('page-' + page);
        if (pageEl) pageEl.classList.add('active');
        if (page === 'developer') this.refreshDeveloperMode();
        if (page === 'ucp') this.refreshUCPProfile();
      });
    });
    // UCP subnav
    document.querySelectorAll('.ucp-subnav').forEach(btn => {
      btn.addEventListener('click', () => {
        const sub = btn.dataset.sub;
        document.querySelectorAll('.ucp-subnav').forEach(b => { b.classList.remove('btn-primary'); b.classList.add('btn-secondary'); });
        btn.classList.add('btn-primary'); btn.classList.remove('btn-secondary');
        document.querySelectorAll('[id^="ucp-sub-"]').forEach(el => el.classList.add('hidden'));
        const el = document.getElementById('ucp-sub-' + sub);
        if (el) el.classList.remove('hidden');
        if (sub === 'profile') this.refreshUCPProfile();
        if (sub === 'capabilities') this.renderCapabilityNegotiator();
        if (sub === 'failure') this.renderFailureLab();
        if (sub === 'eval') this.setupEvalLab();
        if (sub === 'learn') this.renderLearnCards();
        if (sub === 'trust') this.renderTrustLayer();
        if (sub === 'presentation') {}
      });
    });
    // Mobile nav visibility
    if (window.innerWidth <= 600) {
      document.getElementById('mobile-nav').style.display = 'flex';
    }
    window.addEventListener('resize', () => {
      document.getElementById('mobile-nav').style.display = window.innerWidth <= 600 ? 'flex' : 'none';
    });
  },

  // ---- HERO BINDING ----
  bindHero() {
    const input = document.getElementById('main-query-input');
    const runBtn = document.getElementById('run-agent-btn');

    // Scenario chips
    document.querySelectorAll('.scenario-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        input.value = chip.dataset.query;
        input.focus();
      });
    });

    runBtn.addEventListener('click', () => this.runAgent());
    input.addEventListener('keydown', e => { if (e.key === 'Enter') this.runAgent(); });

    // Reset
    document.getElementById('reset-agent-btn').addEventListener('click', () => this.resetAgent());

    // Checkout btn
    document.getElementById('proceed-checkout-btn').addEventListener('click', () => this.startCheckout());

    // Cart controls
    document.getElementById('clear-cart-btn').addEventListener('click', () => {
      SESSION.cart = [];
      this.renderCart();
      showToast('Cart cleared');
    });

    // Compare
    document.getElementById('compare-btn').addEventListener('click', () => this.renderComparisonTable());
    document.getElementById('close-comparison-btn').addEventListener('click', () => {
      document.getElementById('comparison-area').style.display = 'none';
    });

    // Sort
    document.getElementById('sort-btn').addEventListener('click', () => {
      if (SESSION.ranked.length > 0) {
        SESSION.ranked.sort((a,b) => a.price - b.price);
        this.renderProducts(SESSION.ranked, SESSION.intent);
        showToast('Sorted by price: low to high');
      }
    });

    // Ask agent
    document.getElementById('ask-agent-btn').addEventListener('click', () => {
      const q = document.getElementById('ask-agent-input').value.trim();
      if (!q || SESSION.ranked.length === 0) return;
      this.answerComparisonQuestion(q);
    });

    // Score modal close
    document.getElementById('score-modal-close').addEventListener('click', () => {
      document.getElementById('score-modal').classList.remove('active');
    });
    document.getElementById('score-modal').addEventListener('click', e => {
      if (e.target === e.currentTarget) e.currentTarget.classList.remove('active');
    });

    // Order advance
    document.getElementById('advance-order-btn').addEventListener('click', () => {
      if (SESSION.order) {
        SESSION.order = ORDER_ENGINE.advance(SESSION.order);
        this.renderOrderTimeline();
        this.updateAgentState();
      }
    });

    // Dataflow
    document.getElementById('df-prev-btn').addEventListener('click', () => this.dataflowStep(-1));
    document.getElementById('df-next-btn').addEventListener('click', () => this.dataflowStep(1));
    document.getElementById('df-reset-btn').addEventListener('click', () => this.dataflowReset());

    // Edit intent
    document.getElementById('edit-intent-btn').addEventListener('click', () => {
      const viewer = document.getElementById('intent-json-display');
      if (viewer.contentEditable === 'true') {
        viewer.contentEditable = 'false';
        document.getElementById('edit-intent-btn').textContent = 'Edit';
        document.getElementById('rerun-intent-btn').classList.add('hidden');
      } else {
        viewer.contentEditable = 'true';
        viewer.style.outline = '1px solid var(--accent-purple)';
        document.getElementById('edit-intent-btn').textContent = 'Done';
        document.getElementById('rerun-intent-btn').classList.remove('hidden');
      }
    });

    // Presentation
    document.getElementById('start-presentation-btn').addEventListener('click', () => this.startPresentation());
    document.getElementById('exit-presentation-btn').addEventListener('click', () => this.exitPresentation());
    document.getElementById('pres-prev-btn').addEventListener('click', () => this.presentationNav(-1));
    document.getElementById('pres-next-btn').addEventListener('click', () => this.presentationNav(1));

    // Profile actions
    document.getElementById('copy-profile-btn').addEventListener('click', () => {
      const profile = UCP_PROFILE_GENERATOR.generate();
      navigator.clipboard.writeText(JSON.stringify(profile, null, 2));
      showToast('Profile JSON copied to clipboard ✓');
    });
    document.getElementById('validate-profile-btn').addEventListener('click', () => this.validateProfile());

    // Eval run
    document.getElementById('run-eval-btn').addEventListener('click', () => this.runEvaluation());

    // Copy state
    document.getElementById('copy-state-btn').addEventListener('click', () => {
      const state = this.getAgentStateJSON();
      navigator.clipboard.writeText(JSON.stringify(state, null, 2));
      showToast('Agent state copied ✓');
    });

    // Refresh metrics
    document.getElementById('refresh-metrics-btn').addEventListener('click', () => this.renderObsDashboard());
  },

  // ---- AGENT RUN ----
  async runAgent() {
    const query = document.getElementById('main-query-input').value.trim();
    if (!query) { showToast('Please enter a shopping query first'); return; }

    // Show workspace
    const workspace = document.getElementById('agent-workspace');
    workspace.style.display = 'block';
    document.getElementById('hero-section').scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => workspace.scrollIntoView({ behavior: 'smooth', block: 'start' }), 300);

    // Reset pipeline
    this.resetPipeline();
    document.getElementById('pipeline-spinner').classList.remove('hidden');
    document.getElementById('run-agent-btn').disabled = true;
    document.getElementById('trace-intent-row').style.display = 'none';
    document.getElementById('products-area').style.display = 'none';
    document.getElementById('no-match-panel').classList.add('hidden');

    // Set first stage active
    this.updatePipeline('intent', 'active');

    try {
      const result = await AGENT.run(query);
      this.renderTraceLog();
      document.getElementById('trace-intent-row').style.display = 'block';

      if (result.success) {
        document.getElementById('products-area').style.display = 'block';
      } else {
        this.renderNoMatch(result.intent);
      }
    } catch(e) {
      showToast('Agent error: ' + e.message);
    } finally {
      document.getElementById('pipeline-spinner').classList.add('hidden');
      document.getElementById('run-agent-btn').disabled = false;
    }
  },

  resetAgent() {
    this.resetPipeline();
    this.selectedForComparison.clear();
    document.getElementById('trace-intent-row').style.display = 'none';
    document.getElementById('products-area').style.display = 'none';
    document.getElementById('comparison-area').style.display = 'none';
    document.getElementById('checkout-section').style.display = 'none';
    document.getElementById('order-section').style.display = 'none';
    document.getElementById('no-match-panel').classList.add('hidden');
    document.getElementById('trace-detail-panel').classList.remove('visible');
    document.getElementById('main-query-input').value = '';
    SESSION.trace = [];
    SESSION.ranked = [];
    SESSION.intent = null;
  },

  // ---- PIPELINE ----
  renderPipelineTrack() {
    const container = document.getElementById('pipeline-stages');
    container.innerHTML = '';
    PIPELINE_STAGES.forEach((stage, i) => {
      const el = document.createElement('div');
      el.innerHTML = `
        <div class="pipeline-stage" id="stage-${stage.id}" data-stage="${stage.id}" role="listitem" tabindex="0" aria-label="${stage.name}">
          <div class="stage-icon" id="stage-icon-${stage.id}">${i+1}</div>
          <div class="stage-info">
            <div class="stage-name">${stage.name}</div>
            <div class="stage-status" id="stage-status-${stage.id}">${stage.desc}</div>
          </div>
          <div class="stage-latency" id="stage-latency-${stage.id}"></div>
        </div>
        ${i < PIPELINE_STAGES.length - 1 ? '<div class="pipeline-connector"></div>' : ''}
      `;
      container.appendChild(el);
      el.querySelector('.pipeline-stage').addEventListener('click', () => this.showTraceForStage(stage.id));
    });
  },

  updatePipeline(stageId, status, latency = null) {
    this._pipelineStatus[stageId] = status;
    if (latency) this._pipelineLatencies[stageId] = latency;

    const el = document.getElementById('stage-' + stageId);
    const iconEl = document.getElementById('stage-icon-' + stageId);
    const statusEl = document.getElementById('stage-status-' + stageId);
    const latencyEl = document.getElementById('stage-latency-' + stageId);
    if (!el) return;

    el.className = 'pipeline-stage ' + (status || '');
    if (status === 'done') {
      iconEl.textContent = '✓';
      statusEl.textContent = 'Complete';
      if (latency) latencyEl.textContent = latency + 'ms';
    } else if (status === 'active') {
      iconEl.innerHTML = '<span class="spinner" style="width:12px;height:12px;border-width:1.5px;"></span>';
      statusEl.textContent = 'Running...';
    } else if (status === 'error') {
      iconEl.textContent = '✕';
      statusEl.textContent = 'Failed';
    } else if (status === 'pending') {
      const stageIdx = PIPELINE_STAGES.findIndex(s => s.id === stageId);
      iconEl.textContent = stageIdx + 1;
      statusEl.textContent = PIPELINE_STAGES.find(s => s.id === stageId)?.desc || '';
    }

    // Update previous stage to done when new one activates
    const stages = PIPELINE_STAGES.map(s => s.id);
    const idx = stages.indexOf(stageId);
    if (status === 'active' && idx > 0) {
      const prevId = stages[idx - 1];
      if (this._pipelineStatus[prevId] !== 'done') this.updatePipeline(prevId, 'done');
    }

    // Update progress bar
    const doneCount = Object.values(this._pipelineStatus).filter(s => s === 'done').length;
    const pct = Math.round((doneCount / PIPELINE_STAGES.length) * 100);
    const progressEl = document.getElementById('pipeline-progress');
    if (progressEl) { progressEl.style.width = pct + '%'; progressEl.setAttribute('aria-valuenow', pct); }
  },

  resetPipeline() {
    this._pipelineStatus = {};
    this._pipelineLatencies = {};
    PIPELINE_STAGES.forEach(s => this.updatePipeline(s.id, 'pending'));
    const progressEl = document.getElementById('pipeline-progress');
    if (progressEl) { progressEl.style.width = '0%'; progressEl.setAttribute('aria-valuenow', 0); }
  },

  // ---- TRACE ----
  renderTraceLog() {
    const log = document.getElementById('trace-log');
    const runId = document.getElementById('trace-run-id');
    runId.textContent = SESSION.id;
    log.innerHTML = '';
    SESSION.trace.forEach((entry, idx) => {
      const el = document.createElement('div');
      el.className = 'trace-entry';
      el.setAttribute('data-idx', idx);
      el.setAttribute('role', 'row');
      const icon = entry.status === 'success' ? '✓' : entry.status === 'error' ? '✕' : '○';
      const iconColor = entry.status === 'success' ? 'var(--accent-green)' : entry.status === 'error' ? 'var(--accent-red)' : 'var(--text-muted)';
      el.innerHTML = `
        <span class="trace-status-icon" style="color:${iconColor}">${icon}</span>
        <span class="trace-event-name">${entry.event}</span>
        <span class="trace-latency">${entry.latency}ms</span>
        <span class="trace-timestamp">${new Date(entry.timestamp).toLocaleTimeString()}</span>
      `;
      el.addEventListener('click', () => this.showTraceDetail(idx, el));
      log.appendChild(el);
    });
    // Mark all pipeline stages done
    PIPELINE_STAGES.forEach(s => { if (this._pipelineStatus[s.id] !== 'done' && this._pipelineStatus[s.id] !== 'pending') this.updatePipeline(s.id, 'done'); });
    this.updatePipeline('cart', 'pending');
  },

  showTraceDetail(idx, el) {
    document.querySelectorAll('.trace-entry').forEach(e => e.classList.remove('selected'));
    el.classList.add('selected');
    const entry = SESSION.trace[idx];
    if (!entry) return;
    const panel = document.getElementById('trace-detail-panel');
    const inputDiv = document.getElementById('trace-detail-input');
    const outputDiv = document.getElementById('trace-detail-output');
    inputDiv.innerHTML = syntaxHighlight(entry.input || {});
    outputDiv.innerHTML = syntaxHighlight(entry.output || {});
    panel.classList.add('visible');
  },

  showTraceForStage(stageId) {
    const stageToEvent = { intent: 0, discovery: 1, filter: 2, inventory: 3, rank: 4, recommend: 5 };
    const idx = stageToEvent[stageId];
    if (idx !== undefined && SESSION.trace[idx]) {
      const entries = document.querySelectorAll('.trace-entry');
      if (entries[idx]) this.showTraceDetail(idx, entries[idx]);
    }
  },

  // ---- INTENT ----
  renderIntent(intent, constraints) {
    const display = document.getElementById('intent-json-display');
    const safeIntent = {
      category: intent.category,
      budget: intent.budget,
      size: intent.size,
      brand_preference: intent.brand_preference,
      use_case: intent.use_case,
      surface: intent.surface,
      confidence: intent.confidence + '%',
      source: 'LOCAL_DETERMINISTIC_PARSER'
    };
    display.innerHTML = syntaxHighlight(safeIntent);
    display.contentEditable = 'false';
    document.getElementById('edit-intent-btn').textContent = 'Edit';
    document.getElementById('rerun-intent-btn').classList.add('hidden');

    const constraintsList = document.getElementById('constraints-list');
    constraintsList.innerHTML = '';
    constraints.forEach(c => {
      const el = document.createElement('div');
      el.className = 'constraint-item';
      el.innerHTML = `
        <span class="constraint-name">${c.name}</span>
        <div style="display:flex;align-items:center;gap:6px;">
          <span class="constraint-value">${c.value}</span>
          <span class="constraint-type constraint-${c.type}">${c.type.toUpperCase()}</span>
        </div>
      `;
      constraintsList.appendChild(el);
    });
  },

  // ---- PRODUCTS ----
  renderResults(ranked, intent, hardFailures) {
    const title = document.getElementById('results-title');
    if (ranked.length === 0) {
      this.renderNoMatch(intent);
      document.getElementById('products-area').style.display = 'none';
      return;
    }
    title.textContent = `${ranked.length} products found · best match: ${ranked[0].total_score}% score`;
    this.renderProducts(ranked, intent);
    document.getElementById('products-area').style.display = 'block';
    document.getElementById('comparison-area').style.display = 'none';
  },

  renderProducts(ranked, intent) {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = '';
    this.selectedForComparison.clear();
    this.updateCompareBtn();

    ranked.forEach((item, idx) => {
      const p = item.product;
      const merchant = MERCHANTS[item.merchant_id];
      const card = document.createElement('div');
      card.className = 'product-card' + (idx === 0 ? ' top-pick' : '');
      card.setAttribute('role', 'listitem');
      card.setAttribute('tabindex', '0');
      card.setAttribute('aria-label', p.title);

      const inCompare = this.selectedForComparison.has(p.id);
      card.innerHTML = `
        <span class="product-emoji" aria-hidden="true">${p.emoji}</span>
        <div class="product-brand">${p.brand}</div>
        <div class="product-title">${p.title}</div>
        <div class="product-price">
          <span class="currency">₹</span>${item.price.toLocaleString('en-IN')}
        </div>
        <div class="product-meta">
          <span class="product-rating">★ ${p.rating}</span>
          <span class="product-reviews">(${(p.reviews || 0).toLocaleString()})</span>
          ${item.delivery ? `<span class="product-delivery">📦 ${item.delivery}</span>` : ''}
          ${merchant ? `<span class="product-merchant">${merchant.emoji} ${merchant.name}</span>` : ''}
        </div>
        <div class="product-tags">
          ${(p.tags || []).slice(0,3).map(t => `<span class="product-tag">${t}</span>`).join('')}
        </div>
        <div class="match-score-bar">
          <span class="match-score-label">AI MATCH</span>
          <div class="match-score-track"><div class="match-score-fill" style="width:${item.total_score}%"></div></div>
          <span class="match-score-value">${item.total_score}%</span>
        </div>
        <div class="product-actions">
          <button class="btn btn-primary btn-sm add-cart-btn" data-pid="${p.id}" data-mid="${item.merchant_id}" aria-label="Add ${p.title} to cart">+ Cart</button>
          <button class="btn btn-secondary btn-sm why-btn" data-pid="${p.id}" data-idx="${idx}" aria-label="Why this product?">Why?</button>
          <button class="btn btn-ghost btn-sm compare-toggle-btn ${inCompare?'text-purple':''}" data-pid="${p.id}" aria-label="Toggle comparison" aria-pressed="${inCompare}">⊞</button>
        </div>
      `;

      // Bind product actions
      card.querySelector('.add-cart-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        SESSION.cart = CART_ENGINE.add(SESSION.cart, p, item.merchant_id);
        this.renderCart();
        this.updatePipeline('cart', 'done');
        showToast(`${p.title} added to cart ✓`);
      });

      card.querySelector('.why-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        this.showScoreBreakdown(item);
      });

      card.querySelector('.compare-toggle-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        const pid = p.id;
        if (this.selectedForComparison.has(pid)) {
          this.selectedForComparison.delete(pid);
          e.currentTarget.classList.remove('text-purple');
          e.currentTarget.setAttribute('aria-pressed', 'false');
        } else if (this.selectedForComparison.size < 3) {
          this.selectedForComparison.add(pid);
          e.currentTarget.classList.add('text-purple');
          e.currentTarget.setAttribute('aria-pressed', 'true');
        } else {
          showToast('Maximum 3 products for comparison');
        }
        this.updateCompareBtn();
      });

      grid.appendChild(card);
    });
  },

  updateCompareBtn() {
    const btn = document.getElementById('compare-btn');
    const count = this.selectedForComparison.size;
    document.getElementById('compare-count').textContent = count;
    btn.disabled = count < 2;
  },

  // ---- SCORE BREAKDOWN ----
  showScoreBreakdown(item) {
    const modal = document.getElementById('score-modal');
    const body = document.getElementById('score-modal-body');
    document.getElementById('score-modal-title').textContent = `Why "${item.product.title}"?`;

    const dimLabels = {
      requirement_match: 'Requirement Match',
      budget_fit: 'Budget Fit',
      use_case: 'Use-Case Suitability',
      inventory: 'Inventory',
      rating: 'Rating',
      delivery: 'Delivery Speed'
    };

    const rows = Object.entries(item.breakdown).map(([key, val]) => `
      <div class="score-dim">
        <span class="score-dim-name">${dimLabels[key] || key}</span>
        <div class="score-dim-bar"><div class="score-dim-fill" style="width:${val.pct*100}%"></div></div>
        <span class="score-dim-val">${val.score}/${val.max}</span>
      </div>
    `).join('');

    body.innerHTML = `
      <div style="margin-bottom:12px;">
        <p class="text-sm text-muted" style="margin-bottom:10px;">Transparent ranking breakdown. Each dimension is computed deterministically from product data and your query.</p>
        <div class="score-breakdown">${rows}</div>
        <div class="score-total">
          <span class="score-total-label">TOTAL MATCH SCORE</span>
          <span class="score-total-val">${item.total_score}/100</span>
        </div>
      </div>
      <div style="padding:10px;background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.15);border-radius:var(--radius-sm);">
        <div class="text-xs text-muted" style="margin-bottom:4px;">Product Details</div>
        <div class="text-sm"><strong>${item.product.title}</strong></div>
        <div class="text-xs text-muted">${item.product.brand} · ${MERCHANTS[item.merchant_id]?.name || item.merchant_id} · ₹${item.price.toLocaleString()}</div>
        <div class="text-xs text-secondary" style="margin-top:4px;">${item.product.description}</div>
      </div>
    `;
    modal.classList.add('active');
  },

  // ---- COMPARISON ----
  renderComparisonTable() {
    if (this.selectedForComparison.size < 2) return;
    const selectedItems = SESSION.ranked.filter(r => this.selectedForComparison.has(r.product.id));
    const thead = document.getElementById('comparison-thead');
    const tbody = document.getElementById('comparison-tbody');

    const headerRow = `<tr>
      <th>Attribute</th>
      ${selectedItems.map(i => `<th>${i.product.emoji} ${i.product.title.split(' ').slice(0,3).join(' ')}</th>`).join('')}
    </tr>`;
    thead.innerHTML = headerRow;

    const rows = [
      { label: 'Price', fn: i => `₹${i.price.toLocaleString()}`, compare: (vals) => vals.findIndex(v => v === Math.min(...vals)) },
      { label: 'Rating', fn: i => `★ ${i.product.rating}`, compare: (vals) => vals.findIndex(v => v === Math.max(...vals)) },
      { label: 'Inventory', fn: i => `${i.inv} units`, compare: (vals) => vals.findIndex(v => v === Math.max(...vals)) },
      { label: 'Delivery', fn: i => i.delivery || 'N/A' },
      { label: 'Match Score', fn: i => `${i.total_score}%`, compare: (vals) => vals.findIndex(v => v === Math.max(...vals)) },
      { label: 'Merchant', fn: i => MERCHANTS[i.merchant_id]?.name || i.merchant_id },
      { label: 'Brand', fn: i => i.product.brand },
    ];

    tbody.innerHTML = rows.map(row => {
      const vals = selectedItems.map(i => row.fn(i));
      const numVals = vals.map(v => parseFloat(v.replace(/[^0-9.]/g,'')));
      const bestIdx = row.compare ? row.compare(numVals) : -1;
      return `<tr>
        <td><strong class="text-sm">${row.label}</strong></td>
        ${vals.map((v, vi) => `<td class="${vi === bestIdx ? 'winner highlight' : ''}">${v}</td>`).join('')}
      </tr>`;
    }).join('');

    document.getElementById('comparison-area').style.display = 'block';
    document.getElementById('comparison-area').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  },

  answerComparisonQuestion(q) {
    const resp = document.getElementById('ask-agent-response');
    resp.style.display = 'block';
    resp.textContent = '⏳ Analyzing...';

    setTimeout(() => {
      const ql = q.toLowerCase();
      const ranked = SESSION.ranked.slice(0, 3);
      let answer = '';

      if (ql.includes('best') || ql.includes('recommend')) {
        const top = ranked.find(r => this.selectedForComparison.has(r.product.id)) || ranked[0];
        answer = `Based on your query "${SESSION.query}", I recommend the **${top.product.title}** (${top.total_score}% match). It best balances ${SESSION.intent?.use_case?.[0] || 'your requirements'}, budget fit, and rating (★${top.product.rating}).`;
      } else if (ql.includes('cheap') || ql.includes('affordable') || ql.includes('budget')) {
        const cheapest = [...SESSION.ranked].filter(r => this.selectedForComparison.has(r.product.id)).sort((a,b) => a.price-b.price)[0];
        answer = cheapest ? `Most affordable: **${cheapest.product.title}** at ₹${cheapest.price.toLocaleString()}` : 'Please select products to compare first.';
      } else if (ql.includes('fast') || ql.includes('deliver') || ql.includes('quick')) {
        const fastest = [...SESSION.ranked].filter(r => this.selectedForComparison.has(r.product.id)).sort((a,b) => {
          const da = a.delivery?.includes('1') ? 1 : a.delivery?.includes('2') ? 2 : 5;
          const db = b.delivery?.includes('1') ? 1 : b.delivery?.includes('2') ? 2 : 5;
          return da - db;
        })[0];
        answer = fastest ? `Fastest delivery: **${fastest.product.title}** — ${fastest.delivery}` : 'No delivery info available.';
      } else {
        const top = SESSION.ranked.find(r => this.selectedForComparison.has(r.product.id));
        answer = top ? `The **${top.product.title}** (score: ${top.total_score}%) seems most suitable based on overall requirements. ${top.product.description}` : 'Run the agent with a query to get recommendations.';
      }

      resp.innerHTML = `<div style="padding:8px 10px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.15);border-radius:var(--radius-sm);">
        <span class="text-xs text-green" style="font-weight:700;display:block;margin-bottom:4px;">DEMO MODE · Deterministic Response</span>
        <span style="line-height:1.6;">${answer}</span>
      </div>`;
    }, 800);
  },

  // ---- NO MATCH ----
  renderNoMatch(intent) {
    const panel = document.getElementById('no-match-panel');
    const desc = document.getElementById('no-match-desc');
    const relaxOptions = document.getElementById('relax-options');
    panel.classList.remove('hidden');

    const constraints = [];
    if (intent?.budget?.max) constraints.push(`budget ≤ ₹${intent.budget.max.toLocaleString()}`);
    if (intent?.size) constraints.push(`size ${intent.size}`);
    if (intent?.category) constraints.push(intent.category.replace(/_/g,' '));

    desc.textContent = constraints.length > 0
      ? `No products found matching: ${constraints.join(', ')}. Try relaxing one of the constraints below.`
      : 'No products found matching your query. Try relaxing the constraints.';

    relaxOptions.innerHTML = '';
    const options = [];
    if (intent?.budget?.max) options.push({ label: `Increase budget to ₹${Math.round(intent.budget.max * 1.25).toLocaleString()}`, action: () => {
      const newIntent = {...intent, budget: {...intent.budget, max: Math.round(intent.budget.max * 1.25)}};
      this.rerunWithIntent(newIntent);
    }});
    if (intent?.brand_preference?.length > 0) options.push({ label: 'Remove brand preference', action: () => {
      const newIntent = {...intent, brand_preference: []};
      this.rerunWithIntent(newIntent);
    }});
    options.push({ label: 'Show closest matches', action: () => {
      const results = SEARCH_ENGINE.search(intent || {keywords:[], brand_preference:[], use_case:[]}, CATALOG);
      const ranked = RANKING_ENGINE.rank(results.map(r => ({product:r.product})), intent || {keywords:[], brand_preference:[], use_case:[]});
      if (ranked.length > 0) {
        SESSION.ranked = ranked;
        this.renderProducts(ranked, intent);
        document.getElementById('products-area').style.display = 'block';
        panel.classList.add('hidden');
        document.getElementById('results-title').textContent = `Showing ${ranked.length} closest matches (constraints relaxed)`;
      }
    }});

    options.forEach(opt => {
      const btn = document.createElement('button');
      btn.className = 'btn btn-secondary btn-sm';
      btn.textContent = opt.label;
      btn.addEventListener('click', opt.action);
      relaxOptions.appendChild(btn);
    });
  },

  async rerunWithIntent(newIntent) {
    SESSION.intent = newIntent;
    const candidates = SEARCH_ENGINE.search(newIntent, CATALOG);
    const { filtered } = CONSTRAINT_ENGINE.apply(candidates, newIntent);
    const ranked = RANKING_ENGINE.rank(filtered, newIntent);
    SESSION.ranked = ranked;
    if (ranked.length > 0) {
      this.renderResults(ranked, newIntent, []);
      document.getElementById('no-match-panel').classList.add('hidden');
    } else {
      this.renderNoMatch(newIntent);
    }
  },

  // ---- CART ----
  renderCart() {
    const body = document.getElementById('cart-body');
    const totals = document.getElementById('cart-totals');

    if (SESSION.cart.length === 0) {
      body.innerHTML = '<div class="cart-empty"><span class="cart-empty-icon" aria-hidden="true">🛒</span>Cart is empty</div>';
      totals.classList.add('hidden');
      return;
    }

    body.innerHTML = '';
    SESSION.cart.forEach(item => {
      const merchant = MERCHANTS[item.merchant_id];
      const price = item.product.price[item.merchant_id] || item.product.best_price;
      const el = document.createElement('div');
      el.className = 'cart-item';
      el.innerHTML = `
        <span class="cart-item-emoji" aria-hidden="true">${item.product.emoji}</span>
        <div class="cart-item-info">
          <div class="cart-item-name">${item.product.title}</div>
          <div class="cart-item-meta">${merchant?.name || item.merchant_id}</div>
        </div>
        <div class="qty-control">
          <button class="qty-btn" data-pid="${item.product.id}" data-mid="${item.merchant_id}" data-delta="-1" aria-label="Decrease quantity">−</button>
          <span class="qty-val">${item.qty}</span>
          <button class="qty-btn" data-pid="${item.product.id}" data-mid="${item.merchant_id}" data-delta="1" aria-label="Increase quantity">+</button>
        </div>
        <span class="cart-item-price">₹${(price * item.qty).toLocaleString()}</span>
        <button class="btn btn-ghost btn-sm" data-rm-pid="${item.product.id}" data-rm-mid="${item.merchant_id}" aria-label="Remove ${item.product.title}">✕</button>
      `;
      body.appendChild(el);
    });

    // Bind qty/remove buttons
    body.querySelectorAll('.qty-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        SESSION.cart = CART_ENGINE.updateQty(SESSION.cart, btn.dataset.pid, btn.dataset.mid, parseInt(btn.dataset.delta));
        this.renderCart();
      });
    });
    body.querySelectorAll('[data-rm-pid]').forEach(btn => {
      btn.addEventListener('click', () => {
        SESSION.cart = CART_ENGINE.remove(SESSION.cart, btn.dataset.rmPid, btn.dataset.rmMid);
        this.renderCart();
      });
    });

    // Totals
    const t = CART_ENGINE.totals(SESSION.cart);
    document.getElementById('cart-subtotal').textContent = formatINR(t.subtotal);
    document.getElementById('cart-shipping').textContent = t.shipping === 0 ? 'FREE' : formatINR(t.shipping);
    document.getElementById('cart-tax').textContent = formatINR(t.tax);
    document.getElementById('cart-total').textContent = formatINR(t.total);
    totals.classList.remove('hidden');
    this.updateAgentState();
  },

  // ---- CHECKOUT ----
  startCheckout() {
    if (SESSION.cart.length === 0) { showToast('Add items to cart first'); return; }
    const session = CHECKOUT_ENGINE.create(SESSION.cart);
    SESSION.checkout = session;
    this.updatePipeline('checkout', 'active');
    document.getElementById('checkout-section').style.display = 'block';
    document.getElementById('checkout-section').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    this.renderCheckoutSection();
    SESSION.checkout_success++;
    this.updateAgentState();
  },

  renderCheckoutSection() {
    const statesEl = document.getElementById('checkout-states');
    const states = CHECKOUT_ENGINE.STATES;
    const currentStatus = SESSION.checkout?.status || 'INITIALIZED';
    const currentIdx = states.indexOf(currentStatus);

    statesEl.innerHTML = states.map((s, i) => `
      <div class="checkout-state ${i < currentIdx ? 'done' : i === currentIdx ? 'active' : ''}" role="listitem" aria-label="${s}" style="position:relative;">
        ${i < states.length - 1 ? '<div class="checkout-connector ' + (i < currentIdx ? 'done' : '') + '"></div>' : ''}
        <div class="checkout-state-dot">${i < currentIdx ? '✓' : i + 1}</div>
        <div class="checkout-state-name">${s.replace(/_/g,' ')}</div>
      </div>
    `).join('');

    this.renderCheckoutForm();
    this.updateAgentState();
  },

  renderCheckoutForm() {
    const area = document.getElementById('checkout-form-area');
    const s = SESSION.checkout;
    if (!s) return;

    const actionBtn = s.status !== 'COMPLETED' ? `<button class="btn btn-primary" id="advance-checkout-btn" aria-label="Advance checkout">${
      s.status === 'INITIALIZED' ? '→ Provide Information' :
      s.status === 'REQUIRES_INFORMATION' ? '→ Ready for Checkout' :
      s.status === 'READY_FOR_CHECKOUT' ? '→ Simulate Payment' :
      s.status === 'PAYMENT_SIMULATED' ? '→ Complete Order' : ''
    }</button>` : '';

    const statusColor = s.status === 'COMPLETED' ? 'var(--accent-green)' : s.status === 'INITIALIZED' ? 'var(--text-muted)' : 'var(--accent-purple-light)';

    area.innerHTML = `
      <div class="card">
        <div class="card-header">
          <span class="card-title">Checkout Session</span>
          <div style="display:flex;gap:8px;align-items:center;">
            <span class="text-mono text-xs text-muted">${s.id}</span>
            <span style="font-size:0.72rem;font-weight:700;color:${statusColor}">${s.status}</span>
          </div>
        </div>
        <div class="card-body">
          <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
            <div class="sim-badge" style="font-size:0.65rem;">SIMULATED PAYMENT — No real transaction</div>
            <span class="ucp-version-badge">UCP ${UCP_VERSION}</span>
          </div>
          <div style="margin-bottom:12px;">
            ${s.shipping ? `<div class="text-xs text-muted">Shipping: ${s.shipping.method || 'TBD'} · ${s.shipping.address ? `${s.shipping.address.city}, ${s.shipping.address.country}` : 'Address required'}</div>` : ''}
            ${s.payment ? `<div class="text-xs text-muted">Payment: ${s.payment.handler} · ${s.payment.status}${s.payment.reference ? ' · Ref: '+s.payment.reference : ''}</div>` : ''}
          </div>
          <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
            ${actionBtn}
            <button class="btn btn-ghost btn-sm" id="view-session-json-btn" aria-label="View session JSON">{ } JSON</button>
            ${s.status === 'COMPLETED' ? '<button class="btn btn-green btn-sm" id="create-order-btn" aria-label="Create order">Create Order →</button>' : ''}
          </div>
          <div id="session-json-area" style="display:none;margin-top:10px;"></div>
        </div>
      </div>
    `;

    document.getElementById('advance-checkout-btn')?.addEventListener('click', () => {
      SESSION.checkout = CHECKOUT_ENGINE.advance(SESSION.checkout);
      this.renderCheckoutSection();
      if (SESSION.checkout.status === 'COMPLETED') {
        this.updatePipeline('checkout', 'done');
        this.updatePipeline('order', 'active');
        showToast('Checkout completed! ✓ (Simulated — no real payment)');
      }
    });

    document.getElementById('view-session-json-btn')?.addEventListener('click', (e) => {
      const area2 = document.getElementById('session-json-area');
      if (area2.style.display === 'none') {
        area2.innerHTML = `<div class="json-viewer" style="max-height:200px;">${syntaxHighlight(SESSION.checkout)}</div>`;
        area2.style.display = 'block';
        e.currentTarget.textContent = 'Hide JSON';
      } else { area2.style.display = 'none'; e.currentTarget.textContent = '{ } JSON'; }
    });

    document.getElementById('create-order-btn')?.addEventListener('click', () => {
      const order = ORDER_ENGINE.create(SESSION.checkout);
      SESSION.order = order;
      this.updatePipeline('order', 'active');
      document.getElementById('order-section').style.display = 'block';
      document.getElementById('order-section').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      document.getElementById('order-id-display').textContent = order.id;
      this.renderOrderTimeline();
      this.updateAgentState();
      showToast(`Order ${order.id} created! ✓`);
    });
  },

  // ---- ORDER ----
  renderOrderTimeline() {
    if (!SESSION.order) return;
    const order = SESSION.order;
    const timeline = document.getElementById('order-timeline');
    const states = ORDER_ENGINE.STATES;

    timeline.innerHTML = '';
    states.forEach((state, i) => {
      const isDone = i < order.status_idx;
      const isActive = i === order.status_idx;
      const isPending = i > order.status_idx;
      const event = order.events.find(e => e.status === state.key);
      const isLast = i === states.length - 1;

      timeline.innerHTML += `
        <div class="order-event" role="listitem">
          <div class="order-event-dot-wrap">
            <div class="order-event-dot ${isDone ? 'done' : isActive ? 'active' : 'pending'}" aria-label="${state.key}">${isDone ? '✓' : isActive ? '●' : '○'}</div>
            ${!isLast ? `<div class="order-event-line ${isDone ? 'done' : ''}"></div>` : ''}
          </div>
          <div class="order-event-info">
            <div class="order-event-name ${isPending ? 'text-muted' : ''}">${state.icon} ${state.label}</div>
            ${event ? `<div class="order-event-time">${new Date(event.timestamp).toLocaleString()}</div>` : ''}
            <div class="order-event-detail ${isPending ? 'text-muted' : 'text-secondary'}">${state.desc}</div>
            ${event?.payload?.tracking ? `<div class="text-mono text-xs text-cyan">Tracking: ${event.payload.tracking}</div>` : ''}
          </div>
        </div>
      `;
    });

    if (order.status === 'DELIVERED') {
      this.updatePipeline('order', 'done');
      document.getElementById('advance-order-btn').disabled = true;
      showToast('Order delivered! 🎉');
    }
  },

  // ---- DEVELOPER MODE ----
  renderDeveloperMode() {
    this.renderObsDashboard();
    this.renderAPIExplorer();
  },

  refreshDeveloperMode() {
    this.renderObsDashboard();
    this.renderAgentStateViewer();
  },

  renderObsDashboard() {
    const grid = document.getElementById('obs-metrics-grid');
    const avgLatency = SESSION.run_count > 0 ? Math.round(SESSION.total_latency / SESSION.run_count) : 0;
    const successRate = SESSION.run_count > 0 ? Math.round((SESSION.success_count / SESSION.run_count) * 100) : 0;

    const metrics = [
      { label: 'Agent Runs', value: SESSION.run_count, delta: '+' + SESSION.run_count + ' total' },
      { label: 'Success Rate', value: successRate + '%', delta: SESSION.success_count + ' successful' },
      { label: 'Avg Latency', value: avgLatency + 'ms', delta: 'per run' },
      { label: 'Tool Calls', value: SESSION.tool_calls, delta: 'cumulative' },
      { label: 'Retrievals', value: SESSION.retrieval_count, delta: 'candidates retrieved' },
      { label: 'Checkout', value: SESSION.checkout_success, delta: 'sessions completed' },
      { label: 'Cart Items', value: SESSION.cart.reduce((s,i) => s+i.qty, 0), delta: 'in cart' },
      { label: 'Failures', value: SESSION.failure_count, delta: 'total' }
    ];

    grid.innerHTML = metrics.map(m => `
      <div class="metric-card">
        <div class="metric-value">${m.value}</div>
        <div class="metric-label">${m.label}</div>
        <div class="metric-delta">${m.delta}</div>
      </div>
    `).join('');
  },

  renderAPIExplorer() {
    const sidebar = document.getElementById('api-endpoint-list');
    sidebar.innerHTML = '';
    API_SIMULATOR.ENDPOINTS.forEach((ep, idx) => {
      const el = document.createElement('div');
      el.className = 'api-endpoint' + (idx === 0 ? ' active' : '');
      el.setAttribute('role', 'listitem');
      el.setAttribute('tabindex', '0');
      el.innerHTML = `
        <span class="http-method method-${ep.method.toLowerCase()}">${ep.method}</span>
        <span class="api-path" title="${ep.path}">${ep.path.length > 25 ? ep.path.substr(0,22)+'...' : ep.path}</span>
      `;
      el.addEventListener('click', () => {
        document.querySelectorAll('.api-endpoint').forEach(e => e.classList.remove('active'));
        el.classList.add('active');
        this.renderAPIMain(ep);
      });
      sidebar.appendChild(el);
    });

    // Default: show first endpoint
    this.renderAPIMain(API_SIMULATOR.ENDPOINTS[0]);
  },

  async renderAPIMain(endpoint) {
    const main = document.getElementById('api-main-panel');
    const sampleBodies = {
      '/api/products/search': { query: 'running shoes under 8000', intent: { category: 'running_shoes', budget: { max: 8000, currency: 'INR' } } },
      '/api/cart': { session_id: 'demo_session' },
      '/api/cart/{id}/items': { items: [{ product_id: 'prod_001', quantity: 1 }] },
      '/api/checkout-sessions': { cart_id: 'cart_DEMO', line_items: [{ product_id: 'prod_001', quantity: 1 }] },
      '/api/checkout-sessions/{id}': null,
      '/api/checkout-sessions/{id}/complete': { payment: { handler: 'SIMULATED_PAYMENT' } }
    };

    const bodyTemplate = sampleBodies[endpoint.path] || null;
    const methodClass = `method-${endpoint.method.toLowerCase()}`;

    main.innerHTML = `
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
        <span class="http-method ${methodClass}">${endpoint.method}</span>
        <span class="text-mono" style="font-size:0.85rem;color:var(--text-primary);">${endpoint.path}</span>
        <span class="text-muted text-xs">— ${endpoint.desc}</span>
      </div>
      ${bodyTemplate ? `
      <div>
        <div class="json-toolbar"><span class="json-label">Request Body</span><button class="copy-btn" id="copy-req-btn">Copy</button></div>
        <div class="json-viewer" id="req-body" style="border-top:none;border-top-left-radius:0;border-top-right-radius:0;" contenteditable="true">${syntaxHighlight(bodyTemplate)}</div>
      </div>` : ''}
      <div style="display:flex;gap:8px;align-items:center;">
        <button class="btn btn-primary" id="execute-api-btn" aria-label="Execute API request">▶ Execute</button>
        <span class="text-xs text-muted">Local simulation · No external network</span>
      </div>
      <div id="api-response-area"></div>
    `;

    document.getElementById('copy-req-btn')?.addEventListener('click', () => {
      navigator.clipboard.writeText(JSON.stringify(bodyTemplate, null, 2));
      showToast('Request body copied ✓');
    });

    document.getElementById('execute-api-btn').addEventListener('click', async () => {
      const execBtn = document.getElementById('execute-api-btn');
      execBtn.disabled = true; execBtn.textContent = '⏳ Executing...';
      const respArea = document.getElementById('api-response-area');
      respArea.innerHTML = '<div class="text-muted text-xs" style="padding:8px;">Executing request...</div>';

      try {
        const reqBodyEl = document.getElementById('req-body');
        let reqBody = null;
        if (reqBodyEl) {
          try { reqBody = JSON.parse(reqBodyEl.textContent.replace(/\s+/g,' ')); } catch(e) { reqBody = bodyTemplate; }
        }
        const result = await API_SIMULATOR.execute(endpoint, reqBody);
        const statusClass = result.status < 300 ? 'status-200' : result.status < 500 ? 'status-400' : 'status-500';

        respArea.innerHTML = `
          <div>
            <div class="json-toolbar">
              <span class="json-label">Response</span>
              <div style="display:flex;gap:6px;align-items:center;">
                <span class="status-pill ${statusClass}">${result.status}</span>
                <span class="latency-pill">${result.latency}ms</span>
                ${result.valid ? '<span style="font-size:0.65rem;color:var(--accent-green);">✓ Schema Valid</span>' : '<span style="font-size:0.65rem;color:var(--accent-red);">✕ Invalid</span>'}
                <button class="copy-btn" onclick="navigator.clipboard.writeText(JSON.stringify(${JSON.stringify(result.body)},null,2));showToast('Copied ✓')">Copy</button>
              </div>
            </div>
            <div class="json-viewer" style="border-top:none;border-radius:0 0 var(--radius-md) var(--radius-md);max-height:300px;">${syntaxHighlight(result.body)}</div>
          </div>
        `;
        this.renderProtocolInspector(endpoint, reqBody, result);
      } catch(e) {
        respArea.innerHTML = `<div class="validation-result fail">Error: ${e.message}</div>`;
      }
      execBtn.disabled = false; execBtn.textContent = '▶ Execute';
    });
  },

  renderProtocolInspector(endpoint, reqBody, result) {
    const inspector = document.getElementById('protocol-inspector');
    const validations = [
      { check: 'Valid HTTP method', pass: ['GET','POST','PUT','DELETE'].includes(endpoint.method) },
      { check: 'Endpoint path well-formed', pass: endpoint.path.startsWith('/') },
      { check: 'Response status 2xx', pass: result.status >= 200 && result.status < 300 },
      { check: 'Response is valid JSON', pass: typeof result.body === 'object' },
      { check: 'UCP version in response', pass: !!(result.body?.ucpVersion || result.body?.metadata?.environment) },
      { check: 'Environment labeled', pass: !!(result.body?.environment || result.body?.metadata?.environment) }
    ];

    inspector.innerHTML = `
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;align-items:center;">
        <span class="http-method method-${endpoint.method.toLowerCase()}">${endpoint.method}</span>
        <span class="text-mono text-sm">${endpoint.path}</span>
        <span class="status-pill ${result.status < 300 ? 'status-200' : 'status-400'}">${result.status}</span>
        <span class="latency-pill">${result.latency}ms</span>
      </div>
      <div style="display:flex;flex-direction:column;gap:6px;">
        ${validations.map(v => `
          <div class="validation-result ${v.pass ? 'pass' : 'warn'}">
            ${v.pass ? '✓' : '⚠'} ${v.check}
          </div>
        `).join('')}
      </div>
    `;
  },

  renderAgentStateViewer() {
    const viewer = document.getElementById('agent-state-viewer');
    viewer.innerHTML = syntaxHighlight(this.getAgentStateJSON());
  },

  getAgentStateJSON() {
    return {
      session_id: SESSION.id,
      query: SESSION.query,
      intent: SESSION.intent,
      candidates_found: SESSION.candidates.length,
      filtered_count: SESSION.filtered.length,
      ranked_count: SESSION.ranked.length,
      top_result: SESSION.ranked[0] ? { title: SESSION.ranked[0].product.title, score: SESSION.ranked[0].total_score } : null,
      cart_items: SESSION.cart.length,
      cart_total: SESSION.cart.length > 0 ? CART_ENGINE.totals(SESSION.cart).total : 0,
      checkout_status: SESSION.checkout?.status || null,
      checkout_id: SESSION.checkout?.id || null,
      order_id: SESSION.order?.id || null,
      order_status: SESSION.order?.status || null,
      run_count: SESSION.run_count,
      environment: ENV_LABEL
    };
  },

  updateAgentState() {
    // Update dev mode state viewer if visible
    const devPage = document.getElementById('page-developer');
    if (devPage && devPage.classList.contains('active')) {
      this.renderAgentStateViewer();
      this.renderObsDashboard();
    }
  },

  // ---- ARCHITECTURE MODE ----
  renderArchitectureMode() {
    const canvas = document.getElementById('arch-canvas');
    canvas.innerHTML = `
      <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
        <div class="arch-node" data-comp="user" role="button" tabindex="0" style="background:rgba(59,130,246,0.15);border-color:var(--accent-blue);">
          <span class="arch-node-icon">👤</span> USER
        </div>
        <div class="arch-arrow" aria-hidden="true">↓</div>
        <div class="arch-group" style="width:100%;">
          <div class="arch-group-title">Shopping Agent Layer</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
            <div class="arch-node" data-comp="orchestrator" role="button" tabindex="0"><span class="arch-node-icon">🧠</span> Orchestrator</div>
            <div class="arch-node" data-comp="intent" role="button" tabindex="0"><span class="arch-node-icon">🔤</span> Intent Parser</div>
            <div class="arch-node" data-comp="retrieval" role="button" tabindex="0"><span class="arch-node-icon">🔍</span> Retrieval</div>
            <div class="arch-node" data-comp="ranking" role="button" tabindex="0"><span class="arch-node-icon">📊</span> Ranking</div>
            <div class="arch-node" data-comp="cart_engine" role="button" tabindex="0"><span class="arch-node-icon">🛒</span> Cart</div>
            <div class="arch-node" data-comp="checkout_engine" role="button" tabindex="0"><span class="arch-node-icon">💳</span> Checkout</div>
          </div>
        </div>
        <div class="arch-arrow" aria-hidden="true">↓</div>
        <div class="arch-group" style="width:100%;">
          <div class="arch-group-title">UCP Layer (v${UCP_VERSION})</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
            <div class="arch-node" data-comp="ucp_profile" role="button" tabindex="0" style="border-color:rgba(124,58,237,0.4);"><span class="arch-node-icon">⚡</span> Business Profile</div>
            <div class="arch-node" data-comp="ucp_caps" role="button" tabindex="0" style="border-color:rgba(124,58,237,0.4);"><span class="arch-node-icon">🤝</span> Capabilities</div>
            <div class="arch-node" data-comp="ucp_checkout" role="button" tabindex="0" style="border-color:rgba(124,58,237,0.4);"><span class="arch-node-icon">🔄</span> Checkout Protocol</div>
          </div>
        </div>
        <div class="arch-arrow" aria-hidden="true">↓</div>
        <div class="arch-group" style="width:100%;">
          <div class="arch-group-title">Simulated Merchants</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
            ${Object.values(MERCHANTS).map(m => `<div class="arch-node" data-comp="merchant_${m.id}" role="button" tabindex="0" style="border-color:${m.color}40;"><span class="arch-node-icon">${m.emoji}</span> ${m.name}</div>`).join('')}
          </div>
        </div>
      </div>
    `;

    // Bind click events
    canvas.querySelectorAll('.arch-node').forEach(node => {
      node.addEventListener('click', () => this.showComponentDetail(node.dataset.comp));
      node.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') this.showComponentDetail(node.dataset.comp); });
    });

    this.initDataflow();
  },

  showComponentDetail(comp) {
    const DETAILS = {
      user: { title: 'User', icon: '👤', desc: 'The human or AI system initiating a shopping request via natural language.', tech: 'Input: Natural language query\nOutput: Query string to Agent' },
      orchestrator: { title: 'Orchestrator', icon: '🧠', desc: 'Central agent controller that sequences all pipeline stages: intent parsing → discovery → filtering → ranking → recommendation.', tech: 'Pattern: Sequential pipeline\nState: Session object\nError handling: Per-stage' },
      intent: { title: 'Intent Parser', icon: '🔤', desc: 'Deterministic NLP parser that extracts structured intent from natural language. Extracts: category, budget, size, brand, use_case, surface.', tech: 'Method: Rule-based + regex\nLabeled: LOCAL_DETERMINISTIC_PARSER\nNot an LLM — clearly labeled' },
      retrieval: { title: 'Retrieval Engine', icon: '🔍', desc: 'Keyword + attribute matching search across 120-product catalog. Returns ranked candidates by relevance score.', tech: 'Method: TF-style keyword overlap\nCatalog: 120 products\nReturns: Top 30 candidates' },
      ranking: { title: 'Ranking Engine', icon: '📊', desc: 'Deterministic weighted scoring (6 dimensions). Every score is transparent and explainable.', tech: 'Weights: Req(30%) Budget(20%) UseCase(20%) Inventory(10%) Rating(10%) Delivery(10%)\nFully deterministic' },
      cart_engine: { title: 'Cart Engine', icon: '🛒', desc: 'Local state cart management. Add, remove, update quantity. Calculates subtotal, shipping, 18% GST.', tech: 'State: In-memory session\nTax: 18% GST (India)\nFree shipping: ≥₹5,000' },
      checkout_engine: { title: 'Checkout Engine', icon: '💳', desc: 'UCP-aligned checkout state machine. Manages session lifecycle from INITIALIZED to COMPLETED.', tech: `States: ${CHECKOUT_ENGINE.STATES.join(' → ')}\nUCP Version: ${UCP_VERSION}\nPayment: SIMULATED only` },
      ucp_profile: { title: 'Business Profile', icon: '⚡', desc: 'UCP-inspired business profile published at /.well-known/ucp. Declares capabilities, payment handlers, and policies.', tech: 'UCP Version: ' + UCP_VERSION + '\nEndpoint: GET /.well-known/ucp\nLabeled: UCP-INSPIRED SIMULATION' },
      ucp_caps: { title: 'Capability Negotiation', icon: '🤝', desc: 'Agents and merchants declare supported capabilities. The intersection is the negotiated set of allowed operations.', tech: 'Agent declares: what it can do\nMerchant declares: what it supports\nNegotiated: the intersection' },
      ucp_checkout: { title: 'Checkout Protocol', icon: '🔄', desc: 'UCP-aligned checkout API. POST /checkout-sessions creates a session. PUT updates it. POST /complete finishes it.', tech: 'Endpoints follow UCP structure\nIdempotency: session IDs\nNo real payment: SIMULATED' },
    };

    Object.values(MERCHANTS).forEach(m => {
      DETAILS[`merchant_${m.id}`] = { title: m.name, icon: m.emoji, desc: `Simulated merchant. ${m.tagline}\nCapabilities: ${m.capabilities.join(', ')}`, tech: `Specialty: ${m.specialty}\nRating: ★${m.rating}\nReturns: ${m.policy.returns}\nCOD: ${m.policy.cod ? 'Yes' : 'No'}` };
    });

    const detail = DETAILS[comp] || { title: comp, icon: '?', desc: 'Component details not available.', tech: '' };
    document.getElementById('arch-detail-title').textContent = `${detail.icon} ${detail.title}`;
    document.getElementById('arch-detail-body').innerHTML = `
      <p class="text-sm" style="margin-bottom:10px;line-height:1.6;">${detail.desc.replace(/\n/g,'<br>')}</p>
      ${detail.tech ? `<div class="json-viewer" style="max-height:120px;font-size:0.7rem;">${detail.tech}</div>` : ''}
    `;

    // Highlight node
    document.querySelectorAll('.arch-node').forEach(n => n.classList.remove('highlighted'));
    document.querySelector(`[data-comp="${comp}"]`)?.classList.add('highlighted');
  },

  // ---- DATAFLOW ----
  _dfStep: 0,
  _dfSteps: [
    { name: 'User Query', icon: '👤', type: 'Input', content: { step: 1, description: 'User enters a natural language shopping request. This is the raw input to the agent system.', data: { query: '"Find running shoes under ₹8,000, size 7, for daily road running"', type: 'string', source: 'user_input' } } },
    { name: 'Intent JSON', icon: '🔤', type: 'Parsed', content: { step: 2, description: 'The Intent Parser extracts structured requirements from the natural language query using deterministic NLP rules.', data: { category: 'running_shoes', budget: { max: 8000, currency: 'INR' }, size: '7', use_case: ['daily_running'], surface: 'road', confidence: '82%', source: 'LOCAL_DETERMINISTIC_PARSER' } } },
    { name: 'Retrieval Query', icon: '🔍', type: 'Search', content: { step: 3, description: 'The intent is translated into a retrieval query. Products are ranked by relevance using keyword overlap and attribute matching.', data: { intent_category: 'running_shoes', keywords: ['running', 'shoe', 'road', 'daily'], catalog_size: 120, top_k: 30 } } },
    { name: 'Candidates', icon: '📦', type: 'Retrieved', content: { step: 4, description: '30 candidate products returned from catalog search, sorted by relevance score.', data: { count: 30, top_3: ['Nike Air Zoom Pegasus 40 (rel:195)', 'Adidas Ultraboost 23 (rel:175)', 'ASICS Gel-Kayano 30 (rel:160)'] } } },
    { name: 'Filtered', icon: '⚗', type: 'Filtered', content: { step: 5, description: 'Hard constraints applied: budget ≤ ₹8,000, size 7 available, in stock. Soft constraints: surface=road, use_case=daily_running.', data: { before: 30, after: 8, rejected_reasons: ['price > ₹8,000', 'size 7 unavailable', 'out of stock'] } } },
    { name: 'Ranking', icon: '📊', type: 'Scored', content: { step: 6, description: 'Weighted scoring across 6 dimensions. Each product gets a deterministic, transparent match score.', data: { dimensions: { requirement_match: '30%', budget_fit: '20%', use_case: '20%', inventory: '10%', rating: '10%', delivery: '10%' }, top_score: 91 } } },
    { name: 'Cart', icon: '🛒', type: 'User Action', content: { step: 7, description: 'User selects a product and adds it to the cart. Cart state is managed locally with real calculation of subtotal, shipping, and GST.', data: { items: 1, subtotal: 6999, shipping: 0, tax: 1260, total: 8259 } } },
    { name: 'Checkout', icon: '💳', type: 'UCP Session', content: { step: 8, description: 'UCP-aligned checkout session created. State machine progresses through INITIALIZED → REQUIRES_INFORMATION → READY_FOR_CHECKOUT → PAYMENT_SIMULATED → COMPLETED.', data: { session_id: 'cs_EXAMPLE123', status: 'COMPLETED', ucp_version: UCP_VERSION, payment: 'SIMULATED_PAYMENT — no real transaction' } } },
    { name: 'Order', icon: '📬', type: 'Order Created', content: { step: 9, description: 'Order created after checkout completion. Lifecycle: ORDER_CREATED → CONFIRMED → PROCESSING → SHIPPED → OUT_FOR_DELIVERY → DELIVERED.', data: { order_id: 'ORD-EXAMPLE', status: 'ORDER_CREATED', events: ['ORDER_CREATED', 'CONFIRMED', 'PROCESSING', '...'] } } }
  ],

  initDataflow() {
    this._dfStep = 0;
    this.renderDataflowSteps();
    this.renderDataflowContent();
  },

  renderDataflowSteps() {
    const container = document.getElementById('dataflow-steps');
    container.innerHTML = '';
    this._dfSteps.forEach((step, i) => {
      const el = document.createElement('div');
      el.className = `dataflow-step ${i === this._dfStep ? 'active' : i < this._dfStep ? 'visited' : ''}`;
      el.setAttribute('role', 'listitem');
      el.setAttribute('tabindex', '0');
      el.innerHTML = `
        <div class="dataflow-step-icon">${step.icon}</div>
        <div class="dataflow-step-name">${step.name}</div>
        <div class="dataflow-step-type">${step.type}</div>
      `;
      el.addEventListener('click', () => { this._dfStep = i; this.renderDataflowSteps(); this.renderDataflowContent(); });
      container.appendChild(el);
    });
    document.getElementById('df-step-indicator').textContent = `Step ${this._dfStep + 1} / ${this._dfSteps.length}`;
    document.getElementById('df-prev-btn').disabled = this._dfStep === 0;
    document.getElementById('df-next-btn').disabled = this._dfStep === this._dfSteps.length - 1;
  },

  renderDataflowContent() {
    const step = this._dfSteps[this._dfStep];
    const c = step.content;
    document.getElementById('dataflow-content').innerHTML = `
      <div style="margin-bottom:10px;">
        <span class="text-xs text-muted">Step ${c.step} of ${this._dfSteps.length}</span>
        <div style="font-size:0.9rem;font-weight:700;color:var(--text-primary);margin:4px 0;">${step.icon} ${step.name}</div>
        <p class="text-sm text-secondary" style="line-height:1.6;">${c.description}</p>
      </div>
      <div class="json-viewer" style="max-height:150px;">${syntaxHighlight(c.data)}</div>
    `;
  },

  dataflowStep(delta) {
    this._dfStep = Math.max(0, Math.min(this._dfSteps.length - 1, this._dfStep + delta));
    this.renderDataflowSteps();
    this.renderDataflowContent();
  },

  dataflowReset() {
    this._dfStep = 0;
    this.renderDataflowSteps();
    this.renderDataflowContent();
  },

  // ---- UCP EXPLORER ----
  renderUCPExplorer() {
    this.refreshUCPProfile();
  },

  refreshUCPProfile() {
    const profile = UCP_PROFILE_GENERATOR.generate();
    const viewer = document.getElementById('profile-json-viewer');
    if (viewer) viewer.innerHTML = syntaxHighlight(profile);
  },

  validateProfile() {
    const profile = UCP_PROFILE_GENERATOR.generate();
    const results = UCP_PROFILE_GENERATOR.validate(profile);
    const container = document.getElementById('profile-validation-results');
    container.innerHTML = results.map(r => `
      <div class="validation-result ${r.pass ? 'pass' : r.warn ? 'warn' : 'fail'}">
        ${r.pass ? '✓' : r.warn ? '⚠' : '✕'} ${r.check}
        ${r.detail ? `<span class="text-xs" style="margin-left:4px;opacity:0.7;">— ${r.detail}</span>` : ''}
      </div>
    `).join('');
    showToast(`Validation complete: ${results.filter(r => r.pass).length}/${results.length} checks passed`);
  },

  // ---- CAPABILITY NEGOTIATOR ----
  _agentCaps: { checkout: true, cart: true, order_management: true, fulfillment: true, product_discovery: true, discount: false, identity_linking: false },
  _merchantCaps: { checkout: true, cart: true, order_management: true, fulfillment: false, product_discovery: true, discount: true, identity_linking: false },

  renderCapabilityNegotiator() {
    const grid = document.getElementById('capability-grid');
    const caps = Object.keys({...this._agentCaps, ...this._merchantCaps});
    const uniqueCaps = [...new Set(caps)];
    const negotiated = uniqueCaps.filter(c => this._agentCaps[c] && this._merchantCaps[c]);

    grid.innerHTML = `
      <div>
        <div class="capability-col-title">🤖 Agent Capabilities</div>
        ${uniqueCaps.map(c => `
          <div class="capability-item ${this._agentCaps[c] ? 'supported' : ''}">
            <span style="font-size:0.78rem;">${this._agentCaps[c] ? '✓' : '○'} ${c.replace(/_/g,' ')}</span>
            <div class="cap-toggle ${this._agentCaps[c] ? 'on' : ''}" data-side="agent" data-cap="${c}" role="switch" aria-checked="${this._agentCaps[c]}" tabindex="0" aria-label="Toggle agent ${c}"></div>
          </div>
        `).join('')}
      </div>
      <div class="neg-icon">⇄</div>
      <div>
        <div class="capability-col-title">🏪 Merchant Capabilities</div>
        ${uniqueCaps.map(c => `
          <div class="capability-item ${this._merchantCaps[c] ? 'supported' : ''}">
            <span style="font-size:0.78rem;">${this._merchantCaps[c] ? '✓' : '○'} ${c.replace(/_/g,' ')}</span>
            <div class="cap-toggle ${this._merchantCaps[c] ? 'on' : ''}" data-side="merchant" data-cap="${c}" role="switch" aria-checked="${this._merchantCaps[c]}" tabindex="0" aria-label="Toggle merchant ${c}"></div>
          </div>
        `).join('')}
      </div>
    `;

    // Negotiated result
    grid.innerHTML += `
      <div style="grid-column:1/-1;margin-top:16px;">
        <div class="capability-col-title" style="color:var(--accent-blue);">🤝 Negotiated Capabilities (Intersection)</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          ${negotiated.length > 0 ? negotiated.map(c => `<div class="capability-item negotiated" style="width:auto;">✓ ${c.replace(/_/g,' ')}</div>`).join('') : '<div class="text-muted text-sm">No shared capabilities — commerce not possible</div>'}
        </div>
      </div>
    `;

    // Bind toggles
    grid.querySelectorAll('.cap-toggle').forEach(toggle => {
      toggle.addEventListener('click', () => {
        const side = toggle.dataset.side;
        const cap = toggle.dataset.cap;
        if (side === 'agent') this._agentCaps[cap] = !this._agentCaps[cap];
        else this._merchantCaps[cap] = !this._merchantCaps[cap];
        this.renderCapabilityNegotiator();
      });
    });
  },

  // ---- LEARN UCP ----
  renderLearnCards() {
    const container = document.getElementById('learn-cards');
    const cards = [
      { icon: '⚡', title: 'What is UCP?', desc: 'Universal Commerce Protocol — an open standard (launched Jan 2026) for AI agents to interact with merchants. Built by Google, Shopify, and partners.', link: 'https://ucp.dev' },
      { icon: '🤖', title: 'Why Agentic Commerce?', desc: 'AI agents can now browse, compare, and purchase on behalf of users. UCP provides the protocol layer to make this safe, standardized, and interoperable.', link: 'https://ucp.dev/documentation/core-concepts/' },
      { icon: '📋', title: 'Business Profile', desc: 'Merchants publish a machine-readable profile at /.well-known/ucp declaring their capabilities, payment handlers, and endpoints — enabling agent discovery.', link: 'https://ucp.dev' },
      { icon: '🤝', title: 'Capability Negotiation', desc: 'Agents and merchants declare supported capabilities. The intersection determines what operations are possible. Prevents unsupported operations from being attempted.', link: 'https://ucp.dev' },
      { icon: '🔍', title: 'Product Discovery', desc: 'Agents query structured product catalogs. UCP defines standard schemas for products, variants, pricing, and availability across multiple merchants.', link: 'https://ucp.dev' },
      { icon: '🛒', title: 'Cart Management', desc: 'UCP defines cart creation, item management, and price validation. Ensures agents and merchants agree on what\'s in the cart before checkout.', link: 'https://ucp.dev' },
      { icon: '💳', title: 'Checkout', desc: 'The checkout capability manages the full session lifecycle: INITIALIZED → REQUIRES_INFORMATION → READY → PAYMENT_AUTHORIZED → COMPLETED.', link: 'https://ucp.dev' },
      { icon: '💰', title: 'Payment Handlers', desc: 'Merchants declare supported payment methods. Agents use these handlers to complete transactions. The merchant remains the seller of record.', link: 'https://ucp.dev' },
      { icon: '📦', title: 'Order Management', desc: 'Post-checkout, UCP supports order tracking, updates, cancellations, and returns — all via standardized API schemas.', link: 'https://ucp.dev' },
      { icon: '🔒', title: 'Identity Linking', desc: 'OAuth 2.0-based protocol for agents to act on behalf of authenticated users. Enables personalization while maintaining security boundaries.', link: 'https://ucp.dev' },
      { icon: '🔔', title: 'Webhooks', desc: 'Merchants can push order status updates to agents via webhooks, enabling real-time order tracking without polling.', link: 'https://ucp.dev' },
      { icon: '🏪', title: 'Merchant of Record', desc: 'UCP design principle: merchants remain the seller of record. Agents facilitate but don\'t assume liability. Customer relationship stays with merchant.', link: 'https://ucp.dev' },
    ];
    container.innerHTML = cards.map(c => `
      <div class="learn-card" role="article" tabindex="0">
        <div class="learn-card-icon">${c.icon}</div>
        <div class="learn-card-title">${c.title}</div>
        <div class="learn-card-desc">${c.desc}</div>
        <a href="${c.link}" target="_blank" rel="noopener noreferrer" class="learn-card-link">Official docs ↗</a>
      </div>
    `).join('');
  },

  // ---- TRUST LAYER ----
  renderTrustLayer() {
    const grid = document.getElementById('trust-grid');
    const items = [
      { icon: '🏪', title: 'Merchant of Record', desc: 'The merchant remains the seller of record in all UCP transactions. The AI agent facilitates but does not take liability for the sale.' },
      { icon: '🔒', title: 'No Direct Credentials', desc: 'Agents never directly receive sensitive credentials (card numbers, CVV, passwords). Payment is handled through declared payment handlers.' },
      { icon: '⚡', title: 'Declared Capabilities', desc: 'Merchants explicitly declare what they support in their business profile. Agents cannot invoke undeclared capabilities.' },
      { icon: '🔑', title: 'OAuth Identity', desc: 'Identity linking uses OAuth 2.0. Users explicitly grant agents permission to act on their behalf with defined scopes.' },
      { icon: '✓', title: 'Request Validation', desc: 'Every API request is validated against the declared schema. Invalid requests are rejected before reaching merchant systems.' },
      { icon: '🔄', title: 'Idempotency', desc: 'Checkout sessions use idempotency keys to prevent duplicate orders. Safe to retry on network failures.' },
      { icon: '🔔', title: 'Signed Webhooks', desc: 'Webhook payloads from merchants should be signed to prevent spoofing. Agents verify signatures before processing order updates.' },
      { icon: '⚠', title: 'Simulated Payments Only', desc: 'This demo uses SIMULATED_PAYMENT only. No real payment credentials are collected or processed. Clearly labeled throughout.' }
    ];
    grid.innerHTML = items.map(item => `
      <div class="trust-item" role="article">
        <div class="trust-icon">${item.icon}</div>
        <div class="trust-title">${item.title}</div>
        <div class="trust-desc">${item.desc}</div>
      </div>
    `).join('');
  },

  // ---- FAILURE LAB ----
  renderFailureLab() {
    const grid = document.getElementById('failure-grid');
    const failures = [
      { code: 'OUT_OF_STOCK', title: 'Out of Stock', desc: 'Product available at listing time but out of stock when agent attempts to add to cart.', what: 'The merchant inventory check returned 0 units available.', why: 'Inventory depletion between discovery and cart stages.', recovery: 'Find alternative product', actions: ['Find alternative', 'Alert user', 'Check other merchants'] },
      { code: 'PRICE_CHANGED', title: 'Price Changed', desc: 'Product price increased between discovery and checkout, violating budget constraint.', what: 'Old price: ₹7,499 → Current price: ₹8,199 (+₹700)', why: 'Dynamic pricing. Budget constraint: ₹8,000 now violated.', recovery: 'Re-evaluate with updated price', actions: ['Find alternative', 'Increase budget', 'Continue anyway'] },
      { code: 'SIZE_UNAVAILABLE', title: 'Size Unavailable', desc: 'Requested shoe size not in stock at the selected merchant, even though the model is listed.', what: 'Requested: Size 7. Available: 8, 9, 10 only.', why: 'Size-level inventory differs from product-level inventory.', recovery: 'Check alternate merchants or sizes', actions: ['Check VeloMart', 'Check UrbanCart', 'Try size 7.5'] },
      { code: 'MERCHANT_UNAVAILABLE', title: 'Merchant Unavailable', desc: 'Preferred merchant is temporarily offline or has suspended UCP capability endpoint.', what: 'GET /.well-known/ucp returned 503 Service Unavailable', why: 'Merchant system maintenance or outage.', recovery: 'Switch to alternate merchant', actions: ['Try VeloMart', 'Try UrbanCart', 'Wait and retry'] },
      { code: 'CHECKOUT_EXPIRED', title: 'Checkout Session Expired', desc: 'Checkout session was not completed within the 30-minute expiry window.', what: 'Session cs_DEMO expired at 2026-09-15T15:30:00Z', why: 'UCP checkout sessions have a TTL to prevent stale carts.', recovery: 'Create new checkout session', actions: ['Create new session', 'Re-add to cart'] },
      { code: 'INVALID_CART', title: 'Invalid Cart', desc: 'Cart contains a product that is no longer available or has been delisted.', what: 'POST /api/checkout-sessions returned 422 Unprocessable Entity', why: 'Product prod_001 was delisted between cart creation and checkout.', recovery: 'Remove invalid items and rebuild cart', actions: ['Remove item', 'Find replacement'] },
      { code: 'NO_PRODUCT_MATCH', title: 'No Product Match', desc: 'Agent cannot find any product satisfying all hard constraints in the catalog.', what: 'Intent: diamond running shoes size 13 under ₹500. Catalog match: 0 products.', why: 'Constraints too strict or product category doesn\'t exist in catalog.', recovery: 'Constraint relaxation', actions: ['Increase budget', 'Broaden category', 'Show closest'] },
      { code: 'CAPABILITY_MISMATCH', title: 'Capability Mismatch', desc: 'Agent requests an operation the merchant hasn\'t declared support for in their business profile.', what: 'Agent requested: discount. Merchant declared: checkout, cart, order_management only.', why: 'Negotiated capabilities don\'t include discount. Request blocked.', recovery: 'Only invoke negotiated capabilities', actions: ['Remove discount requirement', 'Try different merchant'] },
      { code: 'MALFORMED_REQUEST', title: 'Malformed UCP Request', desc: 'Request body fails schema validation. Required fields missing or wrong types.', what: 'POST /api/checkout-sessions: missing required field "line_items"', why: 'Agent generated malformed request body.', recovery: 'Validate against UCP schema before sending', actions: ['Fix request body', 'Validate schema', 'Check spec'] },
      { code: 'SERVICE_TIMEOUT', title: 'Simulated Service Timeout', desc: 'Merchant API timed out during inventory check. Agent must handle gracefully.', what: 'GET /api/inventory/{id} timed out after 5000ms', why: 'Network latency, merchant system overload, or rate limiting.', recovery: 'Retry with exponential backoff', actions: ['Retry request', 'Use cached inventory', 'Warn user'] }
    ];

    grid.innerHTML = '';
    failures.forEach(f => {
      const card = document.createElement('div');
      card.className = 'failure-card';
      card.setAttribute('role', 'article');
      card.setAttribute('tabindex', '0');
      card.innerHTML = `
        <div class="failure-code">${f.code}</div>
        <div class="failure-title">${f.title}</div>
        <div class="failure-desc">${f.desc}</div>
        <div class="failure-detail" id="fd-${f.code}" style="display:none;">
          <div style="display:flex;flex-direction:column;gap:8px;margin-bottom:10px;">
            <div><div class="text-xs text-muted" style="margin-bottom:3px;">WHAT HAPPENED</div><div class="text-sm text-secondary">${f.what}</div></div>
            <div><div class="text-xs text-muted" style="margin-bottom:3px;">WHY</div><div class="text-sm text-secondary">${f.why}</div></div>
            <div><div class="text-xs text-muted" style="margin-bottom:3px;">RECOVERY STRATEGY</div><div class="text-sm text-green">${f.recovery}</div></div>
          </div>
          <div class="failure-recovery">
            ${f.actions.map(a => `<button class="btn btn-secondary btn-sm" onclick="showToast('Action: ${a} (Demo simulation)');">${a}</button>`).join('')}
          </div>
        </div>
      `;
      card.addEventListener('click', () => {
        const detail = document.getElementById('fd-' + f.code);
        const isOpen = detail.style.display !== 'none';
        document.querySelectorAll('.failure-detail').forEach(d => d.style.display = 'none');
        document.querySelectorAll('.failure-card').forEach(c => c.classList.remove('active'));
        if (!isOpen) { detail.style.display = 'block'; card.classList.add('active'); }
      });
      grid.appendChild(card);
    });
  },

  // ---- EVALUATION LAB ----
  setupEvalLab() {
    const grid = document.getElementById('eval-grid');
    const metrics = [
      { name: 'Intent Accuracy', key: 'intent', color: 'var(--accent-purple-light)' },
      { name: 'Constraint Adherence', key: 'constraint', color: 'var(--accent-green)' },
      { name: 'Inventory Accuracy', key: 'inventory', color: 'var(--accent-blue)' },
      { name: 'Ranking Consistency', key: 'ranking', color: 'var(--accent-cyan)' },
      { name: 'Cart Correctness', key: 'cart', color: 'var(--accent-amber)' },
      { name: 'Checkout Validity', key: 'checkout', color: 'var(--accent-purple)' },
      { name: 'Protocol Validity', key: 'protocol', color: 'var(--accent-pink)' }
    ];

    grid.innerHTML = metrics.map(m => `
      <div class="eval-row">
        <span class="eval-name">${m.name}</span>
        <div class="eval-bar-track">
          <div class="eval-bar-fill" id="eval-bar-${m.key}" style="width:0%;background:${m.color};"></div>
        </div>
        <span class="eval-score" id="eval-score-${m.key}" style="color:${m.color};">--</span>
        <span class="eval-tests" id="eval-tests-${m.key}" style="color:var(--text-muted);">-- / --</span>
      </div>
    `).join('');
  },

  async runEvaluation() {
    const btn = document.getElementById('run-eval-btn');
    btn.disabled = true; btn.textContent = '⏳ Running 47 tests...';
    const detail = document.getElementById('eval-detail-panel');
    detail.innerHTML = '<div class="text-muted text-sm" style="padding:4px;">Running evaluation suite...</div>';

    await delay(600, 1000);

    const results = EVALUATION_ENGINE.run();
    results.forEach(r => {
      const bar = document.getElementById('eval-bar-' + r.name);
      const score = document.getElementById('eval-score-' + r.name);
      const tests = document.getElementById('eval-tests-' + r.name);
      if (bar) bar.style.width = r.pct + '%';
      if (score) score.textContent = r.pct + '%';
      if (tests) tests.textContent = `${r.pass} / ${r.total}`;
    });

    const totalPass = results.reduce((s, r) => s + r.pass, 0);
    const totalTests = results.reduce((s, r) => s + r.total, 0);
    const overall = Math.round((totalPass / totalTests) * 100);

    detail.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:12px;">
        <div>
          <div class="text-xs text-muted" style="margin-bottom:4px;">OVERALL EVALUATION</div>
          <div style="font-size:1.8rem;font-weight:800;color:var(--accent-green);font-family:var(--font-mono);">${overall}%</div>
        </div>
        <div class="text-sm text-secondary">${totalPass}/${totalTests} test cases passed<br><span class="text-xs text-muted">Results computed from actual test case execution, not fabricated</span></div>
      </div>
      <div style="padding:10px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.15);border-radius:var(--radius-sm);">
        <div class="text-xs text-muted" style="margin-bottom:4px;">METHODOLOGY NOTE</div>
        <div class="text-xs text-secondary">All scores computed by running actual test cases against the live agent engine. Intent parsing tested against expected structured output. Constraint accuracy verified by filtering known products. Checkout validity tested via state machine transitions. UCP protocol validity checked against generated business profile.</div>
      </div>
    `;

    btn.disabled = false; btn.textContent = '▶ Run Again';
    showToast(`Evaluation complete: ${overall}% overall ✓`);
  },

  // ---- PRESENTATION MODE ----
  _presStep: 0,
  _presSlides: [],

  startPresentation() {
    this._presStep = 0;
    this._presSlides = [
      { title: 'CommerceOS — Agentic Commerce Lab', content: `<div style="text-align:center;padding:40px 20px;"><div style="font-size:4rem;margin-bottom:20px;background:linear-gradient(135deg,#c4b5fd,#818cf8,#60a5fa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;">CommerceOS</div><div style="font-size:1.1rem;color:var(--text-secondary);margin-bottom:16px;">An interactive laboratory for AI-native commerce</div><div class="sim-badge" style="display:inline-block;margin:0 auto 16px;">SIMULATED COMMERCE ENVIRONMENT</div><div class="ucp-version-badge" style="display:inline-block;">UCP Version: ${UCP_VERSION}</div><div style="margin-top:24px;font-size:0.85rem;color:var(--text-muted);line-height:1.8;">120 Products · 3 Merchants · Full Agent Pipeline<br>Intent → Discovery → Filter → Rank → Cart → Checkout → Order</div></div>` },
      { title: 'User Request', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 1: User Input</div><h2 style="font-size:1.3rem;margin-bottom:16px;">Natural Language Shopping Request</h2><div class="main-input" style="padding:20px;border-radius:var(--radius-xl);background:rgba(20,20,40,0.8);border:1px solid var(--border-strong);font-size:1rem;color:var(--text-secondary);">"Find running shoes under ₹8,000, size 7, for daily road running."</div><div style="margin-top:24px;padding:16px;background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);border-radius:var(--radius-md);"><div class="text-xs text-purple font-bold" style="margin-bottom:8px;">WHAT THE AGENT DOES WITH THIS</div><ul style="list-style:none;display:flex;flex-direction:column;gap:8px;">${['Parses budget constraint: ≤ ₹8,000','Extracts size requirement: 7','Identifies category: running_shoes','Detects use case: daily_running','Surface: road'].map(s => `<li class="text-sm text-secondary">→ ${s}</li>`).join('')}</ul></div></div>` },
      { title: 'Agent Reasoning', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 2: Intent Extraction</div><h2 style="font-size:1.3rem;margin-bottom:16px;">Structured Intent JSON</h2><div class="json-viewer">${syntaxHighlight({category:'running_shoes',budget:{max:8000,currency:'INR'},size:'7',use_case:['daily_running'],surface:'road',confidence:'82%',source:'LOCAL_DETERMINISTIC_PARSER',environment:ENV_LABEL})}</div><div style="margin-top:16px;padding:10px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:var(--radius-sm);"><div class="text-xs text-amber">Note: Intent extraction uses deterministic NLP rules, not an LLM. Clearly labeled as LOCAL_DETERMINISTIC_PARSER.</div></div></div>` },
      { title: 'Product Discovery', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 3–5: Search + Filter</div><h2 style="font-size:1.3rem;margin-bottom:16px;">Discovering Products</h2><div class="metrics-grid" style="grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;"><div class="metric-card"><div class="metric-value">120</div><div class="metric-label">Catalog Size</div></div><div class="metric-card"><div class="metric-value">8</div><div class="metric-label">After Filter</div></div><div class="metric-card"><div class="metric-value">3</div><div class="metric-label">Merchants</div></div></div><div class="constraint-list">${[{type:'hard',name:'Price',value:'≤ ₹8,000'},{type:'hard',name:'Size',value:'7'},{type:'soft',name:'Surface',value:'road'},{type:'soft',name:'Use Case',value:'daily running'}].map(c => `<div class="constraint-item"><span class="constraint-name">${c.name}</span><div style="display:flex;gap:6px;"><span class="constraint-value">${c.value}</span><span class="constraint-type constraint-${c.type}">${c.type.toUpperCase()}</span></div></div>`).join('')}</div></div>` },
      { title: 'Rankings & Recommendations', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 6: Transparent Ranking</div><h2 style="font-size:1.3rem;margin-bottom:16px;">AI Match Scoring</h2><div style="margin-bottom:12px;padding:12px;background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);border-radius:var(--radius-md);"><div class="text-sm font-bold" style="margin-bottom:8px;">Nike Air Zoom Pegasus 40 — 91% Match</div><div class="score-breakdown">${[['Requirement Match','28/30',93],['Budget Fit','19/20',95],['Use Case','18/20',90],['Inventory','10/10',100],['Rating','9/10',92],['Delivery','7/10',70]].map(([n,s,p]) => `<div class="score-dim"><span class="score-dim-name">${n}</span><div class="score-dim-bar"><div class="score-dim-fill" style="width:${p}%"></div></div><span class="score-dim-val">${s}</span></div>`).join('')}</div></div><div class="text-xs text-muted">Every score is computed deterministically. No black-box reasoning.</div></div>` },
      { title: 'Cart & Merchant Comparison', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 7: Multi-Merchant</div><h2 style="font-size:1.3rem;margin-bottom:16px;">Same Product, 3 Merchants</h2><div style="overflow-x:auto;"><table class="comparison-table" style="width:100%;"><thead><tr><th>Merchant</th><th>Price</th><th>Inventory</th><th>Delivery</th><th>Rating</th></tr></thead><tbody><tr><td>⚡ NOVA</td><td class="highlight">₹6,999</td><td>8 units</td><td class="highlight">2 days</td><td>★4.7</td></tr><tr><td>🏃 VeloMart</td><td>₹6,499</td><td class="highlight winner">15 units</td><td>3 days</td><td>★4.4</td></tr><tr><td>🏙 UrbanCart</td><td>₹7,299</td><td>7 units</td><td>4 days</td><td>★4.2</td></tr></tbody></table></div><div style="margin-top:16px;font-size:0.8rem;color:var(--text-secondary);">Agent selects VeloMart for lowest price, UrbanCart as backup. NOVA recommended for fastest delivery.</div></div>` },
      { title: 'UCP Checkout', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 8: UCP Protocol</div><h2 style="font-size:1.3rem;margin-bottom:16px;">Checkout State Machine</h2><div class="checkout-states" style="margin-bottom:16px;">${CHECKOUT_ENGINE.STATES.map((s,i) => `<div class="checkout-state ${i===4?'done':i===3?'active':'done'}" style="position:relative;">${i<4?'<div class="checkout-connector done"></div>':''}<div class="checkout-state-dot">${i<4?'✓':i===4?'●':'○'}</div><div class="checkout-state-name">${s.replace(/_/g,' ')}</div></div>`).join('')}</div><div class="json-viewer" style="max-height:150px;">${syntaxHighlight({object:'checkout_session',id:'cs_DEMO_123',status:'COMPLETED',ucpVersion:UCP_VERSION,payment:{handler:'SIMULATED_PAYMENT',status:'CAPTURED'},metadata:{environment:ENV_LABEL,note:'Simulated — no real payment processed'}})}</div></div>` },
      { title: 'Order Lifecycle', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">STEP 9: Post-Purchase</div><h2 style="font-size:1.3rem;margin-bottom:16px;">Order Tracking</h2><div style="display:flex;flex-direction:column;gap:8px;">${ORDER_ENGINE.STATES.map((s,i) => `<div class="order-event"><div class="order-event-dot-wrap"><div class="order-event-dot ${i<2?'done':i===2?'active':'pending'}">${i<2?'✓':i===2?'●':'○'}</div>${i<ORDER_ENGINE.STATES.length-1?`<div class="order-event-line ${i<2?'done':''}"></div>`:''}</div><div class="order-event-info"><div class="order-event-name">${s.icon} ${s.label}</div><div class="order-event-detail text-muted">${s.desc}</div></div></div>`).join('')}</div></div>` },
      { title: 'Architecture & UCP', content: `<div style="padding:20px;"><div class="section-label" style="margin-bottom:8px;">SUMMARY</div><h2 style="font-size:1.3rem;margin-bottom:16px;">What Was Built</h2><div class="metrics-grid" style="grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:16px;"><div class="metric-card"><div class="metric-value">120</div><div class="metric-label">Products</div></div><div class="metric-card"><div class="metric-value">3</div><div class="metric-label">Merchants</div></div><div class="metric-card"><div class="metric-value">9</div><div class="metric-label">Pipeline Stages</div></div><div class="metric-card"><div class="metric-value">100%</div><div class="metric-label">Transparent</div></div></div><div style="padding:12px;background:rgba(124,58,237,0.08);border:1px solid rgba(124,58,237,0.2);border-radius:var(--radius-md);"><div class="text-xs text-purple font-bold" style="margin-bottom:8px;">UCP Version ${UCP_VERSION} Implementation</div><div class="text-xs text-secondary" style="line-height:1.8;">Business Profile · Capability Negotiation · Checkout State Machine · Order Lifecycle<br><span class="text-muted">Labeled: UCP-INSPIRED SIMULATION · Not officially certified</span><br><a href="https://ucp.dev" target="_blank" style="color:var(--accent-purple-light);">Official spec: ucp.dev ↗</a></div></div></div>` }
    ];

    document.getElementById('presentation-overlay').classList.add('active');
    this.renderPresSlide();
  },

  renderPresSlide() {
    const slide = this._presSlides[this._presStep];
    document.getElementById('presentation-content').innerHTML = slide.content;
    document.getElementById('pres-step-indicator').textContent = `${this._presStep + 1} / ${this._presSlides.length}`;
    document.getElementById('pres-prev-btn').disabled = this._presStep === 0;
    document.getElementById('pres-next-btn').textContent = this._presStep === this._presSlides.length - 1 ? 'Finish' : 'Next →';
    if (this._presStep === this._presSlides.length - 1) {
      document.getElementById('pres-next-btn').onclick = () => this.exitPresentation();
    } else {
      document.getElementById('pres-next-btn').onclick = () => this.presentationNav(1);
    }
  },

  presentationNav(delta) {
    this._presStep = Math.max(0, Math.min(this._presSlides.length - 1, this._presStep + delta));
    this.renderPresSlide();
  },

  exitPresentation() {
    document.getElementById('presentation-overlay').classList.remove('active');
  }
};

// ---- INIT ----
document.addEventListener('DOMContentLoaded', () => {
  UI.init();
  // Auto-render UCP profile on load
  UI.refreshUCPProfile();
  console.log('CommerceOS UI initialized. UCP:', UCP_VERSION, '| Products:', CATALOG.length);
});
</script>
'''

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'r') as f:
    content = f.read()
idx = content.rfind('</body>')
new_content = content[:idx] + UI_JS + '\n' + content[idx:]
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'w') as f:
    f.write(new_content)
print(f"Part 4 written: Complete UI Controller. File size: {len(new_content):,} bytes")
