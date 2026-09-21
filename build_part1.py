#!/usr/bin/env python3
"""Build Part 1: HTML head + complete CSS design system + HTML shell"""

HTML_PART1 = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="CommerceOS — An interactive laboratory for AI-native commerce. Watch an AI agent discover products, compare merchants, and complete checkout using the Universal Commerce Protocol (UCP).">
<title>CommerceOS | Agentic Commerce Lab</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* ============================================================
   COMMERCEOS — DESIGN SYSTEM
   UCP Version: 2026-08-25 | Environment: SIMULATED
   ============================================================ */

:root {
  --bg-primary: #08080f;
  --bg-secondary: #0f0f1a;
  --bg-tertiary: #161622;
  --bg-card: #111120;
  --bg-card-hover: #181828;
  --bg-glass: rgba(20,20,40,0.7);
  --border-subtle: rgba(120,120,200,0.1);
  --border-default: rgba(120,120,200,0.15);
  --border-strong: rgba(120,120,200,0.25);
  --accent-purple: #7c3aed;
  --accent-purple-light: #a855f7;
  --accent-blue: #3b82f6;
  --accent-blue-light: #60a5fa;
  --accent-cyan: #06b6d4;
  --accent-green: #10b981;
  --accent-green-light: #34d399;
  --accent-amber: #f59e0b;
  --accent-red: #ef4444;
  --accent-pink: #ec4899;
  --text-primary: #f0f0f8;
  --text-secondary: #9090b0;
  --text-muted: #50506a;
  --text-code: #a78bfa;
  --gradient-hero: linear-gradient(135deg, #0f0520 0%, #08080f 40%, #0a1520 100%);
  --gradient-purple: linear-gradient(135deg, #7c3aed, #4f46e5);
  --gradient-blue: linear-gradient(135deg, #3b82f6, #06b6d4);
  --gradient-green: linear-gradient(135deg, #10b981, #06b6d4);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.4);
  --shadow-md: 0 4px 20px rgba(0,0,0,0.5);
  --shadow-lg: 0 8px 40px rgba(0,0,0,0.6);
  --shadow-glow-purple: 0 0 30px rgba(124,58,237,0.15);
  --shadow-glow-blue: 0 0 30px rgba(59,130,246,0.15);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --font-sans: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --transition: 0.2s cubic-bezier(0.4,0,0.2,1);
  --transition-slow: 0.4s cubic-bezier(0.4,0,0.2,1);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; font-size: 14px; }

body {
  font-family: var(--font-sans);
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
  overflow-x: hidden;
  min-height: 100vh;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-purple); }

/* TYPOGRAPHY */
h1,h2,h3,h4,h5,h6 { font-weight: 700; letter-spacing: -0.02em; line-height: 1.2; }
code, pre, .mono { font-family: var(--font-mono); }

/* ANIMATIONS */
@keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
@keyframes slideIn { from { opacity:0; transform:translateX(-12px); } to { opacity:1; transform:translateX(0); } }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
@keyframes spin { to { transform:rotate(360deg); } }
@keyframes gradient-shift { 0%,100% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } }
@keyframes glow-pulse { 0%,100% { box-shadow: 0 0 20px rgba(124,58,237,0.2); } 50% { box-shadow: 0 0 40px rgba(124,58,237,0.4); } }
@keyframes flow { 0% { stroke-dashoffset: 100; } 100% { stroke-dashoffset: 0; } }
@keyframes scanline { 0% { transform: translateY(-100%); } 100% { transform: translateY(100vh); } }
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }
@keyframes bounce-in { 0% { transform:scale(0.8); opacity:0; } 60% { transform:scale(1.05); opacity:1; } 100% { transform:scale(1); } }
@keyframes progress-fill { from { width:0; } to { width:var(--target-width); } }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}

/* LAYOUT */
.app-container { display: flex; flex-direction: column; min-height: 100vh; }

/* TOP NAV */
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(8,8,15,0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 24px;
  display: flex; align-items: center; justify-content: space-between;
  height: 56px;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-size: 1.1rem; font-weight: 800; letter-spacing: -0.03em;
}
.nav-logo-mark {
  width: 28px; height: 28px;
  background: var(--gradient-purple);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 900; color: white;
}
.nav-logo-text { color: var(--text-primary); }
.nav-logo-text span { color: var(--accent-purple-light); }
.nav-tabs { display: flex; gap: 2px; }
.nav-tab {
  padding: 6px 14px; border-radius: var(--radius-sm);
  font-size: 0.8rem; font-weight: 500; color: var(--text-secondary);
  cursor: pointer; transition: all var(--transition);
  border: none; background: none;
  letter-spacing: 0.01em;
}
.nav-tab:hover { color: var(--text-primary); background: var(--bg-tertiary); }
.nav-tab.active { color: var(--text-primary); background: var(--bg-tertiary); border: 1px solid var(--border-default); }
.nav-status { display: flex; align-items: center; gap: 12px; }
.status-badge {
  display: flex; align-items: center; gap: 5px;
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em;
  color: var(--text-muted); text-transform: uppercase;
}
.status-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: var(--accent-green);
  animation: pulse 2s infinite;
}
.status-dot.amber { background: var(--accent-amber); }
.status-dot.blue { background: var(--accent-blue); }
.ucp-version-badge {
  background: rgba(124,58,237,0.12);
  border: 1px solid rgba(124,58,237,0.25);
  padding: 3px 8px; border-radius: 4px;
  font-size: 0.65rem; font-weight: 700; letter-spacing: 0.06em;
  color: var(--accent-purple-light); text-transform: uppercase;
}
.sim-badge {
  background: rgba(245,158,11,0.12);
  border: 1px solid rgba(245,158,11,0.25);
  padding: 3px 8px; border-radius: 4px;
  font-size: 0.6rem; font-weight: 700; letter-spacing: 0.06em;
  color: var(--accent-amber);
}

/* PAGE / SECTION SYSTEM */
.page { display: none; animation: fadeIn 0.3s ease; }
.page.active { display: block; }

/* HERO SECTION */
.hero {
  min-height: calc(100vh - 56px);
  background: var(--gradient-hero);
  position: relative; overflow: hidden;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 60px 24px 40px;
  text-align: center;
}
.hero-mesh {
  position: absolute; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 60% 50% at 20% 30%, rgba(124,58,237,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 80% 70%, rgba(59,130,246,0.1) 0%, transparent 60%),
    radial-gradient(ellipse 40% 60% at 50% 100%, rgba(6,182,212,0.06) 0%, transparent 70%);
}
.hero-grid {
  position: absolute; inset: 0; z-index: 0;
  background-image: 
    linear-gradient(rgba(120,120,200,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(120,120,200,0.04) 1px, transparent 1px);
  background-size: 40px 40px;
}
.hero-content { position: relative; z-index: 1; max-width: 760px; }
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(124,58,237,0.1); border: 1px solid rgba(124,58,237,0.2);
  padding: 4px 12px; border-radius: 100px;
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em;
  color: var(--accent-purple-light); text-transform: uppercase;
  margin-bottom: 24px;
}
.hero-title {
  font-size: clamp(3rem, 8vw, 5.5rem);
  font-weight: 900; letter-spacing: -0.04em;
  line-height: 1;
  background: linear-gradient(135deg, #ffffff 0%, #c4b5fd 40%, #818cf8 80%, #60a5fa 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}
.hero-subtitle {
  font-size: 1rem; color: var(--text-secondary);
  font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase;
  margin-bottom: 20px;
}
.hero-tagline {
  font-size: 1.15rem; color: var(--text-secondary);
  max-width: 520px; margin: 0 auto 32px;
  line-height: 1.7;
}
.hero-tagline strong { color: var(--text-primary); }
.hero-secondary-tagline {
  font-size: 0.8rem; color: var(--text-muted);
  letter-spacing: 0.15em; text-transform: uppercase;
  margin-bottom: 36px;
}
.hero-secondary-tagline span { color: var(--accent-cyan); margin: 0 8px; }

/* MAIN INPUT */
.main-input-wrapper {
  position: relative; max-width: 600px; margin: 0 auto 20px;
}
.main-input {
  width: 100%;
  background: rgba(20,20,40,0.8);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-xl);
  padding: 16px 140px 16px 20px;
  font-family: var(--font-sans);
  font-size: 0.95rem; color: var(--text-primary);
  outline: none;
  transition: all var(--transition);
  backdrop-filter: blur(10px);
}
.main-input:focus {
  border-color: var(--accent-purple);
  box-shadow: 0 0 0 3px rgba(124,58,237,0.15), var(--shadow-glow-purple);
}
.main-input::placeholder { color: var(--text-muted); }
.run-btn {
  position: absolute; right: 8px; top: 50%; transform: translateY(-50%);
  background: var(--gradient-purple);
  border: none; border-radius: var(--radius-lg);
  padding: 8px 20px; font-family: var(--font-sans);
  font-size: 0.8rem; font-weight: 700; color: white;
  cursor: pointer; transition: all var(--transition);
  letter-spacing: 0.04em; white-space: nowrap;
}
.run-btn:hover { transform: translateY(-50%) scale(1.02); box-shadow: 0 4px 20px rgba(124,58,237,0.4); }
.run-btn:active { transform: translateY(-50%) scale(0.98); }
.run-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* HERO LIVE INDICATORS */
.hero-indicators {
  display: flex; align-items: center; gap: 20px;
  justify-content: center; flex-wrap: wrap;
  margin-bottom: 28px;
}
.hero-indicator {
  display: flex; align-items: center; gap: 6px;
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.08em;
  color: var(--text-muted); text-transform: uppercase;
}
.hero-indicator .dot { width: 5px; height: 5px; border-radius: 50%; background: var(--accent-green); animation: pulse 2s infinite; }
.hero-indicator .dot.blue { background: var(--accent-blue); }
.hero-indicator .dot.purple { background: var(--accent-purple); }
.hero-indicator .value { color: var(--text-secondary); font-weight: 700; }

/* DEMO SCENARIOS */
.demo-scenarios {
  display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;
  max-width: 700px; margin: 0 auto;
}
.scenario-chip {
  background: rgba(20,20,40,0.6); border: 1px solid var(--border-default);
  padding: 6px 12px; border-radius: 100px;
  font-size: 0.72rem; color: var(--text-secondary);
  cursor: pointer; transition: all var(--transition);
  white-space: nowrap;
}
.scenario-chip:hover { border-color: var(--accent-purple); color: var(--text-primary); background: rgba(124,58,237,0.1); }

/* SECTION LAYOUTS */
.section-container { max-width: 1200px; margin: 0 auto; padding: 32px 24px; }
.section-header { margin-bottom: 24px; }
.section-title { font-size: 1.4rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.section-subtitle { font-size: 0.85rem; color: var(--text-muted); }
.section-label {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
  color: var(--text-muted); text-transform: uppercase;
  margin-bottom: 8px;
}
.section-divider { height: 1px; background: var(--border-subtle); margin: 32px 0; }

/* TWO COLUMN LAYOUT */
.two-col { display: grid; grid-template-columns: 340px 1fr; gap: 20px; align-items: start; }
.three-col { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.two-col-equal { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

/* CARD SYSTEM */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--transition);
}
.card:hover { border-color: var(--border-default); }
.card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-subtle);
}
.card-title { font-size: 0.8rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); }
.card-body { padding: 16px; }

/* AGENT PIPELINE VISUALIZATION */
.pipeline-track {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg); padding: 16px;
  position: sticky; top: 76px;
}
.pipeline-stage {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 10px; border-radius: var(--radius-sm);
  margin-bottom: 2px; cursor: pointer;
  transition: all var(--transition);
  position: relative;
}
.pipeline-stage:hover { background: rgba(255,255,255,0.03); }
.pipeline-stage.active { background: rgba(124,58,237,0.1); border: 1px solid rgba(124,58,237,0.2); }
.pipeline-stage.done { background: rgba(16,185,129,0.05); }
.pipeline-stage.error { background: rgba(239,68,68,0.05); }
.stage-icon {
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.65rem; font-weight: 700; flex-shrink: 0;
  background: var(--bg-tertiary); border: 1px solid var(--border-default);
  color: var(--text-muted);
}
.pipeline-stage.done .stage-icon { background: rgba(16,185,129,0.15); border-color: var(--accent-green); color: var(--accent-green); }
.pipeline-stage.active .stage-icon { background: rgba(124,58,237,0.2); border-color: var(--accent-purple); color: var(--accent-purple-light); animation: glow-pulse 2s infinite; }
.pipeline-stage.error .stage-icon { background: rgba(239,68,68,0.15); border-color: var(--accent-red); color: var(--accent-red); }
.stage-info { flex: 1; min-width: 0; }
.stage-name { font-size: 0.78rem; font-weight: 500; color: var(--text-primary); }
.stage-status { font-size: 0.68rem; color: var(--text-muted); }
.stage-latency { font-size: 0.68rem; font-family: var(--font-mono); color: var(--text-muted); }
.pipeline-connector { width: 1px; height: 10px; background: var(--border-subtle); margin-left: 21px; }

/* AGENT TRACE PANEL */
.trace-panel {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg); overflow: hidden;
}
.trace-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; border-bottom: 1px solid var(--border-subtle);
  background: rgba(0,0,0,0.2);
}
.trace-title { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); }
.trace-log { max-height: 200px; overflow-y: auto; padding: 8px; }
.trace-entry {
  display: grid; grid-template-columns: 20px 1fr auto auto;
  align-items: center; gap: 8px;
  padding: 6px 8px; border-radius: var(--radius-sm);
  cursor: pointer; transition: background var(--transition);
  font-size: 0.75rem;
}
.trace-entry:hover { background: rgba(255,255,255,0.04); }
.trace-entry.selected { background: rgba(124,58,237,0.1); }
.trace-status-icon { font-size: 0.75rem; }
.trace-event-name { color: var(--text-secondary); font-family: var(--font-mono); }
.trace-latency { color: var(--accent-cyan); font-family: var(--font-mono); white-space: nowrap; }
.trace-timestamp { color: var(--text-muted); font-family: var(--font-mono); white-space: nowrap; }
.trace-detail {
  padding: 12px; background: rgba(0,0,0,0.3);
  border-top: 1px solid var(--border-subtle);
  display: none;
}
.trace-detail.visible { display: block; animation: fadeIn 0.2s ease; }

/* INTENT PANEL */
.intent-panel { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); overflow: hidden; }
.intent-json {
  font-family: var(--font-mono); font-size: 0.75rem;
  line-height: 1.6; padding: 14px;
  color: var(--text-secondary);
  background: rgba(0,0,0,0.3);
  min-height: 120px; white-space: pre;
  overflow: auto;
}
.json-key { color: #a78bfa; }
.json-string { color: #34d399; }
.json-number { color: #f59e0b; }
.json-bool { color: #60a5fa; }

/* PRODUCT CARDS */
.products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
.product-card {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg); padding: 16px;
  cursor: pointer; transition: all var(--transition);
  position: relative; overflow: hidden;
}
.product-card:hover { border-color: var(--border-strong); transform: translateY(-2px); box-shadow: var(--shadow-md); }
.product-card.selected { border-color: var(--accent-purple); box-shadow: 0 0 0 1px var(--accent-purple), var(--shadow-glow-purple); }
.product-card.top-pick::before {
  content: 'TOP PICK';
  position: absolute; top: 12px; right: 12px;
  background: var(--gradient-purple);
  padding: 2px 6px; border-radius: 3px;
  font-size: 0.55rem; font-weight: 800; letter-spacing: 0.08em; color: white;
}
.product-emoji { font-size: 2.5rem; margin-bottom: 10px; display: block; }
.product-brand { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px; }
.product-title { font-size: 0.9rem; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; line-height: 1.3; }
.product-price { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); }
.product-price .currency { font-size: 0.75rem; font-weight: 500; color: var(--text-secondary); margin-right: 1px; }
.product-price .original { font-size: 0.8rem; color: var(--text-muted); text-decoration: line-through; margin-left: 6px; font-weight: 400; }
.product-meta { display: flex; gap: 8px; align-items: center; margin: 8px 0; flex-wrap: wrap; }
.product-rating { font-size: 0.72rem; color: var(--accent-amber); font-weight: 600; }
.product-reviews { font-size: 0.68rem; color: var(--text-muted); }
.product-delivery { font-size: 0.68rem; color: var(--accent-green); font-weight: 500; }
.product-merchant { font-size: 0.68rem; color: var(--text-muted); }
.product-tags { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 8px; }
.product-tag {
  padding: 2px 6px; border-radius: 3px;
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;
  background: rgba(120,120,200,0.08); border: 1px solid var(--border-subtle);
  color: var(--text-muted);
}
.match-score-bar {
  margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--border-subtle);
  display: flex; align-items: center; gap: 8px;
}
.match-score-label { font-size: 0.65rem; color: var(--text-muted); font-weight: 600; white-space: nowrap; }
.match-score-track { flex: 1; height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
.match-score-fill { height: 100%; border-radius: 2px; background: var(--gradient-purple); transition: width 0.6s ease; }
.match-score-value { font-size: 0.72rem; font-weight: 700; color: var(--accent-purple-light); white-space: nowrap; font-family: var(--font-mono); }
.product-actions { display: flex; gap: 6px; margin-top: 10px; }

/* BUTTONS */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 14px; border-radius: var(--radius-sm);
  font-family: var(--font-sans); font-size: 0.78rem; font-weight: 600;
  cursor: pointer; transition: all var(--transition);
  border: 1px solid transparent; white-space: nowrap;
}
.btn-primary { background: var(--gradient-purple); color: white; border-color: transparent; }
.btn-primary:hover { opacity: 0.9; transform: translateY(-1px); }
.btn-secondary { background: var(--bg-tertiary); color: var(--text-secondary); border-color: var(--border-default); }
.btn-secondary:hover { color: var(--text-primary); border-color: var(--border-strong); }
.btn-ghost { background: transparent; color: var(--text-muted); border-color: transparent; }
.btn-ghost:hover { background: var(--bg-tertiary); color: var(--text-primary); }
.btn-green { background: rgba(16,185,129,0.15); color: var(--accent-green); border-color: rgba(16,185,129,0.25); }
.btn-green:hover { background: rgba(16,185,129,0.25); }
.btn-danger { background: rgba(239,68,68,0.1); color: var(--accent-red); border-color: rgba(239,68,68,0.2); }
.btn-danger:hover { background: rgba(239,68,68,0.2); }
.btn-sm { padding: 4px 10px; font-size: 0.72rem; }
.btn-lg { padding: 12px 24px; font-size: 0.9rem; border-radius: var(--radius-md); }
.btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; }

/* CART */
.cart-panel { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); overflow: hidden; }
.cart-item { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-bottom: 1px solid var(--border-subtle); }
.cart-item-emoji { font-size: 1.5rem; }
.cart-item-info { flex: 1; min-width: 0; }
.cart-item-name { font-size: 0.8rem; font-weight: 500; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cart-item-meta { font-size: 0.68rem; color: var(--text-muted); }
.qty-control { display: flex; align-items: center; gap: 6px; }
.qty-btn { width: 22px; height: 22px; border-radius: 50%; background: var(--bg-tertiary); border: 1px solid var(--border-default); color: var(--text-secondary); cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; justify-content: center; transition: all var(--transition); }
.qty-btn:hover { border-color: var(--border-strong); color: var(--text-primary); }
.qty-val { font-size: 0.8rem; font-weight: 600; color: var(--text-primary); min-width: 16px; text-align: center; font-family: var(--font-mono); }
.cart-item-price { font-size: 0.85rem; font-weight: 700; color: var(--text-primary); font-family: var(--font-mono); }
.cart-totals { padding: 12px 14px; }
.cart-total-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 6px; }
.cart-total-row.grand { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); border-top: 1px solid var(--border-subtle); padding-top: 8px; margin-top: 4px; }
.cart-empty { padding: 32px; text-align: center; color: var(--text-muted); font-size: 0.8rem; }
.cart-empty-icon { font-size: 2rem; display: block; margin-bottom: 8px; opacity: 0.4; }

/* CHECKOUT STATE MACHINE */
.checkout-states {
  display: flex; gap: 0; position: relative;
  background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg);
  overflow: hidden; padding: 16px;
}
.checkout-state {
  flex: 1; text-align: center; padding: 12px 6px;
  position: relative;
}
.checkout-state-dot {
  width: 32px; height: 32px; border-radius: 50%;
  margin: 0 auto 6px; display: flex; align-items: center; justify-content: center;
  font-size: 0.7rem; font-weight: 700;
  background: var(--bg-tertiary); border: 2px solid var(--border-default);
  color: var(--text-muted); transition: all var(--transition-slow);
}
.checkout-state.active .checkout-state-dot { background: rgba(124,58,237,0.2); border-color: var(--accent-purple); color: var(--accent-purple-light); animation: glow-pulse 2s infinite; }
.checkout-state.done .checkout-state-dot { background: rgba(16,185,129,0.15); border-color: var(--accent-green); color: var(--accent-green); }
.checkout-state-name { font-size: 0.62rem; font-weight: 600; letter-spacing: 0.04em; color: var(--text-muted); text-transform: uppercase; }
.checkout-state.active .checkout-state-name { color: var(--accent-purple-light); }
.checkout-state.done .checkout-state-name { color: var(--accent-green); }
.checkout-connector { position: absolute; top: 28px; left: 50%; right: -50%; height: 2px; background: var(--border-subtle); z-index: 0; }
.checkout-state.done .checkout-connector { background: var(--accent-green); }

/* ORDER LIFECYCLE */
.order-timeline { padding: 16px; }
.order-event { display: flex; gap: 12px; margin-bottom: 16px; }
.order-event-dot-wrap { display: flex; flex-direction: column; align-items: center; }
.order-event-dot { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; flex-shrink: 0; }
.order-event-dot.done { background: rgba(16,185,129,0.15); border: 2px solid var(--accent-green); color: var(--accent-green); }
.order-event-dot.active { background: rgba(124,58,237,0.15); border: 2px solid var(--accent-purple); color: var(--accent-purple-light); animation: glow-pulse 2s infinite; }
.order-event-dot.pending { background: var(--bg-tertiary); border: 2px solid var(--border-default); color: var(--text-muted); }
.order-event-line { flex: 1; width: 2px; background: var(--border-subtle); min-height: 20px; }
.order-event-line.done { background: var(--accent-green); }
.order-event-info { flex: 1; padding-bottom: 4px; }
.order-event-name { font-size: 0.82rem; font-weight: 600; color: var(--text-primary); margin-bottom: 2px; }
.order-event-time { font-size: 0.68rem; color: var(--text-muted); font-family: var(--font-mono); }
.order-event-detail { font-size: 0.72rem; color: var(--text-secondary); margin-top: 2px; }

/* COMPARISON TABLE */
.comparison-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.comparison-table th { padding: 10px 12px; text-align: left; font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); border-bottom: 1px solid var(--border-subtle); }
.comparison-table td { padding: 10px 12px; border-bottom: 1px solid rgba(120,120,200,0.05); color: var(--text-secondary); }
.comparison-table td.highlight { color: var(--accent-green); font-weight: 600; }
.comparison-table td.winner { background: rgba(16,185,129,0.05); }
.comparison-table tr:last-child td { border-bottom: none; }

/* JSON VIEWER */
.json-viewer {
  background: rgba(0,0,0,0.4); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); padding: 14px;
  font-family: var(--font-mono); font-size: 0.73rem; line-height: 1.7;
  overflow: auto; white-space: pre; max-height: 320px;
}
.json-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 12px; background: rgba(0,0,0,0.3);
  border-bottom: 1px solid var(--border-subtle);
}
.json-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); }
.copy-btn { background: transparent; border: 1px solid var(--border-default); padding: 2px 8px; border-radius: 4px; font-size: 0.65rem; color: var(--text-muted); cursor: pointer; transition: all var(--transition); font-family: var(--font-sans); }
.copy-btn:hover { border-color: var(--border-strong); color: var(--text-primary); }

/* VALIDATION */
.validation-result { display: flex; align-items: center; gap: 6px; padding: 6px 10px; border-radius: var(--radius-sm); font-size: 0.75rem; font-weight: 500; }
.validation-result.pass { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.2); color: var(--accent-green); }
.validation-result.fail { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2); color: var(--accent-red); }
.validation-result.warn { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2); color: var(--accent-amber); }

/* API EXPLORER */
.api-explorer { display: grid; grid-template-columns: 220px 1fr; gap: 0; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); overflow: hidden; }
.api-sidebar { border-right: 1px solid var(--border-subtle); padding: 12px 0; }
.api-endpoint {
  padding: 8px 14px; cursor: pointer; transition: background var(--transition);
  font-family: var(--font-mono); font-size: 0.7rem;
  display: flex; align-items: center; gap: 8px;
}
.api-endpoint:hover { background: rgba(255,255,255,0.04); }
.api-endpoint.active { background: rgba(124,58,237,0.1); border-right: 2px solid var(--accent-purple); }
.http-method { font-weight: 700; font-size: 0.62rem; letter-spacing: 0.05em; padding: 1px 5px; border-radius: 3px; }
.method-get { background: rgba(16,185,129,0.15); color: var(--accent-green); }
.method-post { background: rgba(59,130,246,0.15); color: var(--accent-blue); }
.method-put { background: rgba(245,158,11,0.15); color: var(--accent-amber); }
.method-delete { background: rgba(239,68,68,0.15); color: var(--accent-red); }
.api-path { color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.api-main { padding: 16px; display: flex; flex-direction: column; gap: 12px; }
.api-controls { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.status-pill { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 100px; font-size: 0.68rem; font-weight: 700; font-family: var(--font-mono); }
.status-200 { background: rgba(16,185,129,0.1); color: var(--accent-green); }
.status-400 { background: rgba(245,158,11,0.1); color: var(--accent-amber); }
.status-500 { background: rgba(239,68,68,0.1); color: var(--accent-red); }
.latency-pill { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: 100px; font-size: 0.68rem; font-weight: 600; background: rgba(6,182,212,0.1); color: var(--accent-cyan); font-family: var(--font-mono); }

/* ARCHITECTURE DIAGRAM */
.arch-container { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); overflow: hidden; }
.arch-canvas { padding: 24px; min-height: 400px; position: relative; }
.arch-node {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--bg-tertiary); border: 1px solid var(--border-default);
  border-radius: var(--radius-md); padding: 8px 14px;
  font-size: 0.78rem; font-weight: 600;
  cursor: pointer; transition: all var(--transition);
  position: relative; z-index: 1;
}
.arch-node:hover { border-color: var(--accent-purple); box-shadow: var(--shadow-glow-purple); }
.arch-node.highlighted { border-color: var(--accent-purple); background: rgba(124,58,237,0.1); }
.arch-node-icon { font-size: 1rem; }
.arch-group { background: rgba(120,120,200,0.04); border: 1px solid rgba(120,120,200,0.08); border-radius: var(--radius-lg); padding: 14px; }
.arch-group-title { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; }
.arch-arrow { color: var(--text-muted); font-size: 1.2rem; text-align: center; margin: 4px 0; }

/* CAPABILITY NEGOTIATION */
.capability-grid { display: grid; grid-template-columns: 1fr 80px 1fr; gap: 12px; align-items: start; }
.capability-col-title { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 10px; }
.capability-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 7px 10px; border-radius: var(--radius-sm); margin-bottom: 4px;
  background: var(--bg-tertiary); border: 1px solid var(--border-subtle);
  font-size: 0.78rem; transition: all var(--transition);
}
.capability-item.supported { border-color: rgba(16,185,129,0.2); background: rgba(16,185,129,0.05); }
.capability-item.negotiated { border-color: rgba(59,130,246,0.2); background: rgba(59,130,246,0.05); color: var(--accent-blue-light); }
.cap-toggle { width: 28px; height: 16px; border-radius: 100px; background: var(--border-default); position: relative; cursor: pointer; transition: all var(--transition); flex-shrink: 0; }
.cap-toggle.on { background: var(--accent-green); }
.cap-toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 12px; height: 12px; border-radius: 50%; background: white; transition: left 0.2s; }
.cap-toggle.on::after { left: 14px; }
.neg-icon { text-align: center; padding-top: 24px; font-size: 1.5rem; color: var(--text-muted); }

/* METRICS DASHBOARD */
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
.metric-card { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; }
.metric-value { font-size: 1.6rem; font-weight: 800; color: var(--text-primary); line-height: 1; margin-bottom: 4px; font-family: var(--font-mono); }
.metric-label { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); }
.metric-delta { font-size: 0.7rem; color: var(--accent-green); margin-top: 4px; font-weight: 600; }

/* FAILURE LAB */
.failure-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 14px; }
.failure-card {
  background: var(--bg-card); border: 1px solid rgba(239,68,68,0.15);
  border-radius: var(--radius-lg); padding: 16px; cursor: pointer;
  transition: all var(--transition);
}
.failure-card:hover { border-color: rgba(239,68,68,0.3); transform: translateY(-2px); }
.failure-card.active { border-color: var(--accent-red); background: rgba(239,68,68,0.05); }
.failure-code { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; color: var(--accent-red); font-family: var(--font-mono); margin-bottom: 6px; }
.failure-title { font-size: 0.88rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px; }
.failure-desc { font-size: 0.75rem; color: var(--text-secondary); line-height: 1.5; }
.failure-detail { margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(239,68,68,0.15); }
.failure-recovery { margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap; }

/* EVALUATION LAB */
.eval-grid { display: grid; gap: 10px; }
.eval-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 14px; background: var(--bg-card);
  border: 1px solid var(--border-subtle); border-radius: var(--radius-md);
}
.eval-name { font-size: 0.8rem; font-weight: 500; color: var(--text-primary); min-width: 200px; }
.eval-bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.eval-bar-fill { height: 100%; border-radius: 3px; transition: width 1s ease; }
.eval-score { font-size: 0.8rem; font-weight: 700; font-family: var(--font-mono); min-width: 40px; text-align: right; }
.eval-tests { font-size: 0.68rem; color: var(--text-muted); min-width: 80px; text-align: right; font-family: var(--font-mono); }

/* PRESENTATION MODE */
.presentation-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: var(--bg-primary);
  display: none; flex-direction: column;
}
.presentation-overlay.active { display: flex; }
.presentation-header { padding: 20px 32px; border-bottom: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; }
.presentation-content { flex: 1; padding: 40px; overflow-y: auto; }
.presentation-footer { padding: 20px 32px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; }
.pres-step-indicator { font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono); }

/* LEARN UCP CARDS */
.learn-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 14px; }
.learn-card {
  background: var(--bg-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg); padding: 16px;
  transition: all var(--transition); cursor: pointer;
}
.learn-card:hover { border-color: var(--border-strong); transform: translateY(-2px); }
.learn-card-icon { font-size: 1.8rem; margin-bottom: 10px; }
.learn-card-title { font-size: 0.88rem; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
.learn-card-desc { font-size: 0.75rem; color: var(--text-secondary); line-height: 1.5; }
.learn-card-link { font-size: 0.7rem; color: var(--accent-purple-light); margin-top: 8px; display: inline-flex; align-items: center; gap: 4px; text-decoration: none; }
.learn-card-link:hover { text-decoration: underline; }

/* TRUST LAYER */
.trust-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.trust-item { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; }
.trust-icon { font-size: 1.4rem; margin-bottom: 8px; }
.trust-title { font-size: 0.82rem; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; }
.trust-desc { font-size: 0.73rem; color: var(--text-secondary); line-height: 1.5; }

/* PROGRESS BAR */
.progress-bar { height: 3px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--gradient-purple); transition: width 0.4s ease; border-radius: 2px; }

/* MISC UTILITY */
.text-purple { color: var(--accent-purple-light); }
.text-green { color: var(--accent-green); }
.text-amber { color: var(--accent-amber); }
.text-red { color: var(--accent-red); }
.text-blue { color: var(--accent-blue); }
.text-cyan { color: var(--accent-cyan); }
.text-muted { color: var(--text-muted); }
.text-sm { font-size: 0.78rem; }
.text-xs { font-size: 0.68rem; }
.text-mono { font-family: var(--font-mono); }
.font-bold { font-weight: 700; }
.font-medium { font-weight: 500; }
.mt-1 { margin-top: 4px; }
.mt-2 { margin-top: 8px; }
.mt-3 { margin-top: 12px; }
.mt-4 { margin-top: 16px; }
.mb-2 { margin-bottom: 8px; }
.gap-2 { gap: 8px; }
.flex { display: flex; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.flex-wrap { flex-wrap: wrap; }
.w-full { width: 100%; }
.hidden { display: none !important; }
.visible { display: block !important; }
.rounded { border-radius: var(--radius-sm); }
.no-select { user-select: none; }

/* LOADING SPINNER */
.spinner { width: 16px; height: 16px; border: 2px solid var(--border-default); border-top-color: var(--accent-purple); border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }

/* NOTIFICATION TOAST */
.toast {
  position: fixed; bottom: 24px; right: 24px; z-index: 9998;
  background: var(--bg-tertiary); border: 1px solid var(--border-strong);
  border-radius: var(--radius-md); padding: 12px 16px;
  font-size: 0.8rem; color: var(--text-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(80px); opacity: 0;
  transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
}
.toast.show { transform: translateY(0); opacity: 1; }

/* CONSTRAINT PANEL */
.constraint-list { display: flex; flex-direction: column; gap: 6px; }
.constraint-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 7px 10px; background: var(--bg-tertiary);
  border: 1px solid var(--border-subtle); border-radius: var(--radius-sm);
  font-size: 0.78rem;
}
.constraint-type { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.08em; padding: 1px 5px; border-radius: 3px; }
.constraint-hard { background: rgba(239,68,68,0.15); color: var(--accent-red); }
.constraint-soft { background: rgba(245,158,11,0.15); color: var(--accent-amber); }
.constraint-name { color: var(--text-secondary); }
.constraint-value { color: var(--text-primary); font-weight: 600; font-family: var(--font-mono); }

/* DATAFLOW STEPPER */
.dataflow-panel { background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 20px; }
.dataflow-steps { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }
.dataflow-step {
  background: var(--bg-tertiary); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md); padding: 12px;
  text-align: center; cursor: pointer; transition: all var(--transition);
}
.dataflow-step:hover { border-color: var(--border-strong); }
.dataflow-step.active { border-color: var(--accent-purple); background: rgba(124,58,237,0.08); }
.dataflow-step.visited { border-color: rgba(16,185,129,0.2); background: rgba(16,185,129,0.04); }
.dataflow-step-icon { font-size: 1.3rem; margin-bottom: 6px; }
.dataflow-step-name { font-size: 0.72rem; font-weight: 600; color: var(--text-primary); }
.dataflow-step-type { font-size: 0.62rem; color: var(--text-muted); margin-top: 2px; }
.dataflow-content { margin-top: 16px; padding: 14px; background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); }

/* SCORE BREAKDOWN */
.score-breakdown { display: flex; flex-direction: column; gap: 6px; }
.score-dim { display: flex; align-items: center; gap: 8px; }
.score-dim-name { font-size: 0.72rem; color: var(--text-secondary); min-width: 150px; }
.score-dim-bar { flex: 1; height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
.score-dim-fill { height: 100%; background: var(--gradient-purple); border-radius: 2px; transition: width 0.8s ease; }
.score-dim-val { font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-primary); min-width: 35px; text-align: right; }
.score-total { display: flex; justify-content: space-between; align-items: center; padding-top: 8px; border-top: 1px solid var(--border-subtle); margin-top: 4px; }
.score-total-label { font-size: 0.72rem; font-weight: 700; color: var(--text-secondary); }
.score-total-val { font-size: 1rem; font-weight: 800; color: var(--accent-purple-light); font-family: var(--font-mono); }

/* MODAL */
.modal-backdrop { position: fixed; inset: 0; z-index: 500; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; padding: 24px; }
.modal-backdrop.active { display: flex; }
.modal { background: var(--bg-secondary); border: 1px solid var(--border-strong); border-radius: var(--radius-xl); padding: 24px; max-width: 560px; width: 100%; max-height: 80vh; overflow-y: auto; box-shadow: var(--shadow-lg); animation: bounce-in 0.3s ease; }
.modal-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
.modal-title { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.modal-close { background: none; border: none; color: var(--text-muted); cursor: pointer; font-size: 1.2rem; padding: 0 4px; }
.modal-close:hover { color: var(--text-primary); }

/* NO MATCH */
.no-match-panel { text-align: center; padding: 40px 24px; }
.no-match-icon { font-size: 3rem; margin-bottom: 16px; opacity: 0.4; }
.no-match-title { font-size: 1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 8px; }
.no-match-desc { font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 24px; }
.relax-options { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }

/* RESPONSIVE */
@media (max-width: 900px) {
  .two-col { grid-template-columns: 1fr; }
  .pipeline-track { position: static; }
  .api-explorer { grid-template-columns: 1fr; }
  .api-sidebar { border-right: none; border-bottom: 1px solid var(--border-subtle); display: flex; overflow-x: auto; padding: 8px; }
  .api-endpoint { white-space: nowrap; }
  .capability-grid { grid-template-columns: 1fr; }
  .neg-icon { display: none; }
}
@media (max-width: 600px) {
  .top-nav { padding: 0 12px; }
  .nav-tabs { display: none; }
  .section-container { padding: 20px 14px; }
  .three-col { grid-template-columns: 1fr; }
  .hero-title { font-size: 2.5rem; }
  .hero-indicators { gap: 10px; }
  .metrics-grid { grid-template-columns: repeat(2, 1fr); }
  .checkout-state-name { font-size: 0.5rem; }
}
</style>
</head>
<body>
<div class="app-container">

<!-- TOP NAV -->
<nav class="top-nav" role="navigation" aria-label="Main navigation">
  <div class="nav-logo" aria-label="CommerceOS home">
    <div class="nav-logo-mark" aria-hidden="true">C</div>
    <div class="nav-logo-text">Commerce<span>OS</span></div>
  </div>
  <div class="nav-tabs" role="tablist" aria-label="Application modes">
    <button class="nav-tab active" role="tab" aria-selected="true" data-page="shopper" id="tab-shopper">🛍 Shopper</button>
    <button class="nav-tab" role="tab" aria-selected="false" data-page="developer" id="tab-developer">⌨ Developer</button>
    <button class="nav-tab" role="tab" aria-selected="false" data-page="architecture" id="tab-architecture">🔮 Architecture</button>
    <button class="nav-tab" role="tab" aria-selected="false" data-page="ucp" id="tab-ucp">⚡ UCP Explorer</button>
  </div>
  <div class="nav-status" aria-label="System status">
    <div class="status-badge"><span class="status-dot" aria-hidden="true"></span>AGENT READY</div>
    <div class="status-badge"><span class="status-dot blue" aria-hidden="true"></span>MERCHANTS: 3</div>
    <div class="ucp-version-badge" title="UCP Specification Version">UCP 2026-08-25</div>
    <div class="sim-badge" title="This is a simulated commerce environment">SIMULATED</div>
  </div>
</nav>

<!-- MOBILE NAV -->
<div style="background:var(--bg-secondary);border-bottom:1px solid var(--border-subtle);padding:8px 12px;display:none;gap:4px;overflow-x:auto;" id="mobile-nav" aria-label="Mobile navigation">
  <button class="nav-tab active" data-page="shopper" style="font-size:0.7rem;">🛍 Shopper</button>
  <button class="nav-tab" data-page="developer" style="font-size:0.7rem;">⌨ Dev</button>
  <button class="nav-tab" data-page="architecture" style="font-size:0.7rem;">🔮 Arch</button>
  <button class="nav-tab" data-page="ucp" style="font-size:0.7rem;">⚡ UCP</button>
</div>

<!-- ===============================================
     PAGE: SHOPPER MODE
     =============================================== -->
<div class="page active" id="page-shopper">

  <!-- HERO -->
  <section class="hero" id="hero-section" aria-label="CommerceOS Agent Interface">
    <div class="hero-mesh" aria-hidden="true"></div>
    <div class="hero-grid" aria-hidden="true"></div>
    <div class="hero-content">
      <div class="hero-eyebrow" aria-label="Status">
        <span>🧪</span> Agentic Commerce Lab — v2026
      </div>
      <h1 class="hero-title">CommerceOS</h1>
      <p class="hero-subtitle">Agentic Commerce Lab</p>
      <p class="hero-tagline">
        Give an AI agent a shopping goal.<br>
        <strong>Watch it turn intent into a transaction.</strong>
      </p>
      <p class="hero-secondary-tagline">
        Discover <span>·</span> Compare <span>·</span> Decide <span>·</span> Cart <span>·</span> Checkout <span>·</span> Order
      </p>

      <div class="hero-indicators" role="status" aria-live="polite">
        <div class="hero-indicator"><span class="dot" aria-hidden="true"></span>AGENT READY</div>
        <div class="hero-indicator"><span class="dot" aria-hidden="true"></span>MERCHANTS: <span class="value">3</span></div>
        <div class="hero-indicator"><span class="dot" aria-hidden="true"></span>PRODUCTS: <span class="value">120</span></div>
        <div class="hero-indicator"><span class="dot blue" aria-hidden="true"></span>UCP: <span class="value">2026-08-25</span></div>
      </div>

      <div class="main-input-wrapper">
        <label for="main-query-input" class="hidden">What are you looking for?</label>
        <input
          type="text"
          id="main-query-input"
          class="main-input"
          placeholder="What are you looking for? e.g. running shoes under ₹8,000, size 7"
          aria-label="Shopping query input"
          autocomplete="off"
        >
        <button class="run-btn" id="run-agent-btn" aria-label="Run AI Agent">
          RUN AGENT ▶
        </button>
      </div>

      <div class="demo-scenarios" role="list" aria-label="Demo scenarios">
        <button class="scenario-chip" role="listitem" data-query="Find running shoes under ₹8,000, size 7, for daily road running">🏃 Running shoes under ₹8k</button>
        <button class="scenario-chip" role="listitem" data-query="Find a laptop under ₹80,000 for Python and machine learning">💻 ML laptop under ₹80k</button>
        <button class="scenario-chip" role="listitem" data-query="Find wireless headphones under ₹10,000 with excellent battery life">🎧 Headphones under ₹10k</button>
        <button class="scenario-chip" role="listitem" data-query="Find a black formal shirt, size M, under ₹2,500">👔 Formal shirt under ₹2.5k</button>
        <button class="scenario-chip" role="listitem" data-query="Find perfect diamond running shoes size 13 under ₹500">⚠ No match scenario</button>
      </div>
    </div>
  </section>

  <!-- AGENT WORKSPACE -->
  <section class="section-container" id="agent-workspace" style="display:none;" aria-label="Agent execution workspace">
    <div class="two-col">

      <!-- LEFT: Pipeline + Cart -->
      <div>
        <!-- Pipeline Track -->
        <div class="card mb-2" style="margin-bottom:16px;">
          <div class="card-header">
            <span class="card-title">Agent Pipeline</span>
            <div style="display:flex;gap:6px;align-items:center;">
              <span class="spinner hidden" id="pipeline-spinner" aria-label="Running"></span>
              <button class="btn btn-ghost btn-sm" id="reset-agent-btn" aria-label="Reset agent">↩ Reset</button>
            </div>
          </div>
          <div style="padding:8px;" id="pipeline-stages" role="list" aria-label="Agent pipeline stages">
            <!-- Populated by JS -->
          </div>
          <div class="progress-bar" style="margin:0 8px 8px;" aria-label="Pipeline progress">
            <div class="progress-fill" id="pipeline-progress" style="width:0%;" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
          </div>
        </div>

        <!-- Cart -->
        <div class="card" id="cart-card">
          <div class="card-header">
            <span class="card-title">🛒 Cart</span>
            <button class="btn btn-ghost btn-sm" id="clear-cart-btn" aria-label="Clear cart">Clear</button>
          </div>
          <div id="cart-body">
            <div class="cart-empty"><span class="cart-empty-icon" aria-hidden="true">🛒</span>Cart is empty</div>
          </div>
          <div class="cart-totals hidden" id="cart-totals">
            <div class="cart-total-row"><span>Subtotal</span><span id="cart-subtotal" class="text-mono">₹0</span></div>
            <div class="cart-total-row"><span>Shipping</span><span id="cart-shipping" class="text-mono">₹0</span></div>
            <div class="cart-total-row"><span>Tax (18% GST)</span><span id="cart-tax" class="text-mono">₹0</span></div>
            <div class="cart-total-row grand"><span>Total</span><span id="cart-total" class="text-mono">₹0</span></div>
            <div style="margin-top:12px;">
              <button class="btn btn-primary w-full btn-lg" id="proceed-checkout-btn" aria-label="Proceed to checkout">Proceed to Checkout →</button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Main Content Area -->
      <div id="agent-right-panel">

        <!-- TRACE + INTENT (shown after run) -->
        <div id="trace-intent-row" style="display:none;margin-bottom:16px;">
          <!-- Agent Trace -->
          <div class="trace-panel" style="margin-bottom:16px;">
            <div class="trace-header">
              <span class="trace-title">Agent Trace</span>
              <span class="text-xs text-muted" id="trace-run-id"></span>
            </div>
            <div class="trace-log" id="trace-log" role="log" aria-label="Agent trace events" aria-live="polite"></div>
            <div class="trace-detail" id="trace-detail-panel">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div>
                  <div class="section-label">Input</div>
                  <div class="json-viewer" id="trace-detail-input" style="max-height:120px;font-size:0.7rem;"></div>
                </div>
                <div>
                  <div class="section-label">Output</div>
                  <div class="json-viewer" id="trace-detail-output" style="max-height:120px;font-size:0.7rem;"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Intent Panel -->
          <div class="intent-panel">
            <div class="card-header">
              <span class="card-title">Extracted Intent</span>
              <div style="display:flex;gap:6px;">
                <button class="btn btn-secondary btn-sm" id="edit-intent-btn" aria-label="Edit intent JSON">Edit</button>
                <button class="btn btn-primary btn-sm hidden" id="rerun-intent-btn" aria-label="Re-run with edited intent">Re-run</button>
              </div>
            </div>
            <div class="json-viewer" id="intent-json-display" aria-label="Extracted intent JSON">
              <span class="text-muted">Run the agent to see extracted intent...</span>
            </div>
            <!-- Constraints -->
            <div style="padding:10px 14px;border-top:1px solid var(--border-subtle);">
              <div class="section-label" style="margin-bottom:8px;">Constraints</div>
              <div class="constraint-list" id="constraints-list"></div>
            </div>
          </div>
        </div>

        <!-- PRODUCTS AREA -->
        <div id="products-area" style="display:none;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px;">
            <div>
              <div class="section-label">Results</div>
              <h2 class="section-title" id="results-title" style="font-size:1.1rem;"></h2>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <button class="btn btn-secondary btn-sm" id="compare-btn" aria-label="Compare selected products" disabled>⊞ Compare (<span id="compare-count">0</span>)</button>
              <button class="btn btn-secondary btn-sm" id="sort-btn" aria-label="Sort products">↕ Sort</button>
            </div>
          </div>
          <div class="products-grid" id="products-grid" role="list" aria-label="Product results"></div>
        </div>

        <!-- NO MATCH PANEL -->
        <div id="no-match-panel" class="no-match-panel hidden">
          <div class="no-match-icon" aria-hidden="true">🔍</div>
          <h2 class="no-match-title">No Perfect Match Found</h2>
          <p class="no-match-desc" id="no-match-desc">The agent could not find products matching all your constraints.</p>
          <div class="relax-options" id="relax-options" role="group" aria-label="Constraint relaxation options"></div>
        </div>

        <!-- COMPARISON TABLE -->
        <div id="comparison-area" style="display:none;margin-top:20px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <h2 class="section-title" style="font-size:1rem;">Product Comparison</h2>
            <button class="btn btn-ghost btn-sm" id="close-comparison-btn" aria-label="Close comparison">✕ Close</button>
          </div>
          <div style="overflow-x:auto;">
            <table class="comparison-table" id="comparison-table" role="table" aria-label="Product comparison">
              <thead id="comparison-thead"></thead>
              <tbody id="comparison-tbody"></tbody>
            </table>
          </div>
          <div style="margin-top:12px;padding:12px;background:rgba(124,58,237,0.06);border:1px solid rgba(124,58,237,0.15);border-radius:var(--radius-md);">
            <div style="font-size:0.75rem;font-weight:600;color:var(--text-muted);margin-bottom:6px;">ASK AGENT</div>
            <div style="display:flex;gap:8px;">
              <input type="text" id="ask-agent-input" placeholder='e.g. "Which one is best for daily running?"' style="flex:1;background:var(--bg-tertiary);border:1px solid var(--border-default);border-radius:var(--radius-sm);padding:6px 10px;font-size:0.78rem;color:var(--text-primary);font-family:var(--font-sans);outline:none;" aria-label="Ask agent about comparison">
              <button class="btn btn-primary btn-sm" id="ask-agent-btn" aria-label="Submit question to agent">Ask</button>
            </div>
            <div id="ask-agent-response" style="margin-top:8px;font-size:0.78rem;color:var(--text-secondary);display:none;" role="status" aria-live="polite"></div>
          </div>
        </div>

        <!-- CHECKOUT SECTION -->
        <div id="checkout-section" style="display:none;margin-top:20px;">
          <h2 class="section-title" style="font-size:1rem;margin-bottom:14px;">Checkout Session</h2>
          <!-- State Machine -->
          <div class="checkout-states" id="checkout-states" role="list" aria-label="Checkout state machine">
            <!-- Populated by JS -->
          </div>
          <div style="margin-top:14px;" id="checkout-form-area">
            <!-- Dynamic checkout form -->
          </div>
        </div>

        <!-- ORDER SECTION -->
        <div id="order-section" style="display:none;margin-top:20px;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
            <h2 class="section-title" style="font-size:1rem;">Order Lifecycle</h2>
            <div style="display:flex;gap:8px;">
              <span class="text-mono text-xs text-muted" id="order-id-display"></span>
              <button class="btn btn-secondary btn-sm" id="advance-order-btn" aria-label="Advance order state">Advance State →</button>
            </div>
          </div>
          <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-lg);overflow:hidden;">
            <div class="order-timeline" id="order-timeline" role="list" aria-label="Order timeline"></div>
          </div>
        </div>

      </div><!-- end agent-right-panel -->
    </div><!-- end two-col -->
  </section>
</div><!-- end page-shopper -->

<!-- ===============================================
     PAGE: DEVELOPER MODE
     =============================================== -->
<div class="page" id="page-developer">
  <div class="section-container">
    <div class="section-header">
      <div class="section-label">⌨ Mode</div>
      <h1 class="section-title">Developer Mode</h1>
      <p class="section-subtitle">Interactive API explorer, protocol inspector, and agent telemetry</p>
    </div>

    <!-- Observability -->
    <div class="card" style="margin-bottom:20px;">
      <div class="card-header">
        <span class="card-title">Observability Dashboard</span>
        <button class="btn btn-ghost btn-sm" id="refresh-metrics-btn" aria-label="Refresh metrics">↻ Refresh</button>
      </div>
      <div class="card-body">
        <div class="metrics-grid" id="obs-metrics-grid"></div>
      </div>
    </div>

    <!-- API Explorer -->
    <div class="section-header" style="margin-bottom:12px;">
      <div class="section-label">UCP-Aligned</div>
      <h2 class="section-title" style="font-size:1.1rem;">API Explorer</h2>
      <p class="section-subtitle">Execute simulated UCP endpoints against the local commerce engine</p>
    </div>
    <div class="api-explorer" style="margin-bottom:20px;">
      <div class="api-sidebar" id="api-endpoint-list" role="list" aria-label="API endpoints">
        <!-- Populated by JS -->
      </div>
      <div class="api-main" id="api-main-panel">
        <div style="padding:40px;text-align:center;color:var(--text-muted);font-size:0.82rem;">
          Select an endpoint from the left to explore
        </div>
      </div>
    </div>

    <!-- Protocol Inspector -->
    <div class="section-header" style="margin-bottom:12px;">
      <div class="section-label">Last Request</div>
      <h2 class="section-title" style="font-size:1.1rem;">Protocol Inspector</h2>
    </div>
    <div class="card" style="margin-bottom:20px;">
      <div class="card-body" id="protocol-inspector">
        <div style="color:var(--text-muted);font-size:0.82rem;">Execute an API request to see protocol details here.</div>
      </div>
    </div>

    <!-- Agent State Viewer -->
    <div class="section-header" style="margin-bottom:12px;">
      <div class="section-label">Session Memory</div>
      <h2 class="section-title" style="font-size:1.1rem;">Agent State</h2>
    </div>
    <div class="card">
      <div class="card-header">
        <span class="card-title">Current Session</span>
        <button class="btn btn-ghost btn-sm" id="copy-state-btn" aria-label="Copy agent state as JSON">Copy JSON</button>
      </div>
      <div class="json-viewer" id="agent-state-viewer" style="max-height:300px;" aria-label="Agent state JSON">
        <span class="text-muted">Run agent in Shopper Mode to see state...</span>
      </div>
    </div>
  </div>
</div>

<!-- ===============================================
     PAGE: ARCHITECTURE MODE
     =============================================== -->
<div class="page" id="page-architecture">
  <div class="section-container">
    <div class="section-header">
      <div class="section-label">🔮 Mode</div>
      <h1 class="section-title">Architecture Mode</h1>
      <p class="section-subtitle">Interactive system diagram and data flow visualization</p>
    </div>

    <div class="two-col-equal" style="margin-bottom:20px;">
      <!-- Architecture Diagram -->
      <div class="arch-container">
        <div class="card-header">
          <span class="card-title">System Architecture</span>
          <span class="text-xs text-muted">Click any node for details</span>
        </div>
        <div class="arch-canvas" id="arch-canvas" role="img" aria-label="Interactive system architecture diagram">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- Component Detail -->
      <div class="card" style="min-height:300px;">
        <div class="card-header">
          <span class="card-title" id="arch-detail-title">Component Details</span>
        </div>
        <div class="card-body" id="arch-detail-body">
          <p class="text-muted text-sm">Click any component in the diagram to learn about it.</p>
        </div>
      </div>
    </div>

    <!-- Data Flow Stepper -->
    <div class="section-header" style="margin-bottom:12px;">
      <div class="section-label">Step-by-Step</div>
      <h2 class="section-title" style="font-size:1.1rem;">Data Flow Visualization</h2>
      <p class="section-subtitle">How a single shopping request moves through the entire system</p>
    </div>
    <div class="dataflow-panel">
      <div class="dataflow-steps" id="dataflow-steps" role="list" aria-label="Data flow steps"></div>
      <div style="display:flex;gap:8px;justify-content:center;margin:14px 0;">
        <button class="btn btn-secondary btn-sm" id="df-prev-btn" aria-label="Previous step" disabled>← Prev</button>
        <span class="text-mono text-xs text-muted" id="df-step-indicator">Step 0 / 9</span>
        <button class="btn btn-secondary btn-sm" id="df-next-btn" aria-label="Next step">Next →</button>
        <button class="btn btn-ghost btn-sm" id="df-reset-btn" aria-label="Reset data flow">Reset</button>
      </div>
      <div class="dataflow-content" id="dataflow-content">
        <p class="text-muted text-sm">Click "Next →" to begin the data flow walkthrough.</p>
      </div>
    </div>
  </div>
</div>

<!-- ===============================================
     PAGE: UCP EXPLORER
     =============================================== -->
<div class="page" id="page-ucp">
  <div class="section-container">
    <div class="section-header">
      <div class="section-label">⚡ Universal Commerce Protocol</div>
      <h1 class="section-title">UCP Explorer</h1>
      <p class="section-subtitle">Explore the business profile, capabilities, educational content, failure scenarios, and evaluation suite</p>
    </div>

    <!-- Sub-nav -->
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:24px;padding-bottom:16px;border-bottom:1px solid var(--border-subtle);">
      <button class="btn btn-primary btn-sm ucp-subnav" data-sub="profile" aria-label="Business Profile" id="ucpsub-profile">Business Profile</button>
      <button class="btn btn-secondary btn-sm ucp-subnav" data-sub="capabilities" aria-label="Capabilities" id="ucpsub-capabilities">Capabilities</button>
      <button class="btn btn-secondary btn-sm ucp-subnav" data-sub="learn" aria-label="Learn UCP" id="ucpsub-learn">Learn UCP</button>
      <button class="btn btn-secondary btn-sm ucp-subnav" data-sub="failure" aria-label="Failure Lab" id="ucpsub-failure">Failure Lab</button>
      <button class="btn btn-secondary btn-sm ucp-subnav" data-sub="eval" aria-label="Evaluation Lab" id="ucpsub-eval">Evaluation Lab</button>
      <button class="btn btn-secondary btn-sm ucp-subnav" data-sub="trust" aria-label="Trust Layer" id="ucpsub-trust">Trust Layer</button>
      <button class="btn btn-secondary btn-sm ucp-subnav" data-sub="presentation" aria-label="Presentation Mode" id="ucpsub-presentation">🎬 Present</button>
    </div>

    <!-- UCP Sub-sections -->
    <div id="ucp-sub-profile">
      <!-- Business Profile -->
      <div class="two-col-equal" style="align-items:start;">
        <div>
          <div class="section-label" style="margin-bottom:8px;">UCP-Inspired Simulation</div>
          <h2 class="section-title" style="font-size:1rem;margin-bottom:12px;">Business Profile</h2>
          <p class="text-sm text-muted" style="margin-bottom:12px;line-height:1.6;">
            In UCP, merchants publish their capabilities at <code class="text-mono" style="background:rgba(0,0,0,0.4);padding:1px 5px;border-radius:3px;">/.well-known/ucp</code>. 
            This allows AI agents to discover what commerce operations a merchant supports.
          </p>
          <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
            <button class="btn btn-primary btn-sm" id="copy-profile-btn" aria-label="Copy business profile JSON">📋 Copy JSON</button>
            <button class="btn btn-secondary btn-sm" id="validate-profile-btn" aria-label="Validate business profile">✓ Validate Profile</button>
            <a href="https://ucp.dev/specification/overview/" target="_blank" rel="noopener noreferrer" class="btn btn-ghost btn-sm">↗ Official Spec</a>
          </div>
          <div id="profile-validation-results" style="display:flex;flex-direction:column;gap:6px;margin-bottom:12px;"></div>
        </div>
        <div>
          <div class="json-toolbar">
            <span class="json-label">GET /.well-known/ucp</span>
            <div style="display:flex;gap:6px;align-items:center;">
              <span class="status-pill status-200">200 OK</span>
              <span class="latency-pill">12ms</span>
            </div>
          </div>
          <div class="json-viewer" id="profile-json-viewer" aria-label="Business profile JSON" style="max-height:400px;border-top:none;border-top-left-radius:0;border-top-right-radius:0;"></div>
        </div>
      </div>
    </div>

    <div id="ucp-sub-capabilities" class="hidden">
      <h2 class="section-title" style="font-size:1rem;margin-bottom:6px;">Capability Negotiation</h2>
      <p class="text-sm text-muted" style="margin-bottom:16px;">Toggle agent and merchant capabilities to see how negotiation works in UCP. The intersection determines what commerce operations are possible.</p>
      <div class="capability-grid" id="capability-grid">
        <!-- Populated by JS -->
      </div>
    </div>

    <div id="ucp-sub-learn" class="hidden">
      <h2 class="section-title" style="font-size:1rem;margin-bottom:6px;">Learn UCP</h2>
      <p class="text-sm text-muted" style="margin-bottom:16px;">Interactive educational cards covering the Universal Commerce Protocol concepts.</p>
      <div class="learn-cards" id="learn-cards"></div>
    </div>

    <div id="ucp-sub-failure" class="hidden">
      <h2 class="section-title" style="font-size:1rem;margin-bottom:6px;">Failure Lab</h2>
      <p class="text-sm text-muted" style="margin-bottom:16px;">Explore 10 failure scenarios with agent recovery strategies. Click any card to simulate the failure.</p>
      <div class="failure-grid" id="failure-grid"></div>
    </div>

    <div id="ucp-sub-eval" class="hidden">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:8px;">
        <div>
          <h2 class="section-title" style="font-size:1rem;margin-bottom:4px;">Agent Evaluation Lab</h2>
          <p class="text-sm text-muted">Computed from a fixed test suite of <span class="text-mono text-green">47 test cases</span>. Results are deterministic, not fabricated.</p>
        </div>
        <button class="btn btn-primary" id="run-eval-btn" aria-label="Run evaluation suite">▶ Run Evaluation Suite</button>
      </div>
      <div class="eval-grid" id="eval-grid"></div>
      <div style="margin-top:16px;padding:14px;background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:var(--radius-md);" id="eval-detail-panel">
        <p class="text-muted text-sm">Click "Run Evaluation Suite" to compute scores from test cases.</p>
      </div>
    </div>

    <div id="ucp-sub-trust" class="hidden">
      <h2 class="section-title" style="font-size:1rem;margin-bottom:6px;">Trust &amp; Security Layer</h2>
      <p class="text-sm text-muted" style="margin-bottom:16px;">How UCP maintains trust boundaries between agents, merchants, and payment systems.</p>
      <div class="trust-grid" id="trust-grid"></div>
    </div>

    <div id="ucp-sub-presentation" class="hidden">
      <h2 class="section-title" style="font-size:1rem;margin-bottom:6px;">Presentation Mode</h2>
      <p class="text-sm text-muted" style="margin-bottom:16px;">A clean guided demo ideal for LinkedIn videos, portfolio presentations, and interviews.</p>
      <div style="text-align:center;padding:40px;">
        <div style="font-size:3rem;margin-bottom:16px;">🎬</div>
        <h3 style="font-size:1.2rem;margin-bottom:8px;color:var(--text-primary);">Start Presentation Mode</h3>
        <p class="text-muted text-sm" style="margin-bottom:24px;max-width:400px;margin-left:auto;margin-right:auto;">9-step guided demo with clean visuals, agent reasoning, and technical explanation. Perfect for recording.</p>
        <button class="btn btn-primary btn-lg" id="start-presentation-btn" aria-label="Start presentation mode">🎬 Launch Presentation Mode</button>
      </div>
    </div>

  </div>
</div>

<!-- ===============================================
     MODALS
     =============================================== -->
<!-- Score Breakdown Modal -->
<div class="modal-backdrop" id="score-modal" role="dialog" aria-modal="true" aria-labelledby="score-modal-title">
  <div class="modal">
    <div class="modal-header">
      <h2 class="modal-title" id="score-modal-title">Why This Product?</h2>
      <button class="modal-close" id="score-modal-close" aria-label="Close score breakdown">✕</button>
    </div>
    <div id="score-modal-body"></div>
  </div>
</div>

<!-- Presentation Overlay -->
<div class="presentation-overlay" id="presentation-overlay" role="dialog" aria-modal="true" aria-label="Presentation mode">
  <div class="presentation-header">
    <div class="nav-logo">
      <div class="nav-logo-mark">C</div>
      <div class="nav-logo-text">Commerce<span>OS</span></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <span class="ucp-version-badge">UCP 2026-08-25</span>
      <span class="sim-badge">SIMULATED</span>
      <button class="btn btn-ghost btn-sm" id="exit-presentation-btn" aria-label="Exit presentation mode">✕ Exit</button>
    </div>
  </div>
  <div class="presentation-content" id="presentation-content"></div>
  <div class="presentation-footer">
    <button class="btn btn-secondary" id="pres-prev-btn" aria-label="Previous slide" disabled>← Previous</button>
    <span class="pres-step-indicator" id="pres-step-indicator">Step 1 / 9</span>
    <button class="btn btn-primary" id="pres-next-btn" aria-label="Next slide">Next →</button>
  </div>
</div>

<!-- Toast -->
<div class="toast" id="toast" role="alert" aria-live="assertive"></div>

</div><!-- end app-container -->
</body>
</html>'''

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'w') as f:
    f.write(HTML_PART1)
print("Part 1 written: HTML structure + CSS design system")
