#!/usr/bin/env python3
"""Build Part 1 (V2): HTML head + Animated Glassmorphic CSS + HTML shell"""

HTML_PART1 = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CommerceOS | Agentic Commerce Lab</title>
  
  <!-- Clear stale Service Workers left over from HF Docker/Gradio spaces to prevent 404 POST interception -->
  <script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.getRegistrations().then(function(registrations) {
        for(let registration of registrations) {
          registration.unregister();
          console.log('Unregistered stale service worker');
        }
      });
    }
  </script>

  <!-- Google Fonts: Inter and JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ============================================================
   COMMERCEOS V2 — ADVANCED ANIMATED DESIGN SYSTEM
   ============================================================ */

:root {
  --bg-primary: #030305;
  --bg-secondary: #0a0a10;
  --bg-tertiary: rgba(20, 20, 35, 0.4);
  --bg-glass: rgba(15, 15, 25, 0.6);
  --bg-glass-hover: rgba(25, 25, 45, 0.8);
  --border-subtle: rgba(255, 255, 255, 0.05);
  --border-default: rgba(124, 58, 237, 0.2);
  --border-strong: rgba(124, 58, 237, 0.5);
  --border-glow: rgba(124, 58, 237, 0.8);
  
  --accent-purple: #8b5cf6;
  --accent-purple-light: #a78bfa;
  --accent-purple-glow: rgba(139, 92, 246, 0.5);
  --accent-blue: #3b82f6;
  --accent-blue-light: #60a5fa;
  --accent-cyan: #06b6d4;
  --accent-green: #10b981;
  --accent-green-glow: rgba(16, 185, 129, 0.4);
  --accent-amber: #f59e0b;
  --accent-red: #ef4444;
  
  --text-primary: #ffffff;
  --text-secondary: #a1a1aa;
  --text-muted: #52525b;
  --text-code: #c4b5fd;
  
  --gradient-purple: linear-gradient(135deg, #7c3aed, #4f46e5);
  --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
  
  --shadow-glow: 0 0 20px var(--accent-purple-glow);
  --shadow-glow-strong: 0 0 40px var(--accent-purple-glow), inset 0 0 10px var(--accent-purple-glow);
  --shadow-glass: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 30px;
  
  --font-sans: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  --transition: 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  --transition-slow: 0.6s cubic-bezier(0.16, 1, 0.3, 1);
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

/* ANIMATED MESH BACKGROUND */
.mesh-bg {
  position: fixed; inset: 0; z-index: -1;
  background: var(--bg-primary);
  overflow: hidden;
}
.mesh-orb {
  position: absolute; border-radius: 50%; filter: blur(120px);
  opacity: 0.4; animation: float 20s infinite ease-in-out alternate;
}
.orb-1 { width: 600px; height: 600px; background: #4c1d95; top: -10%; left: -10%; animation-delay: 0s; }
.orb-2 { width: 500px; height: 500px; background: #1e3a8a; bottom: -20%; right: -10%; animation-delay: -5s; }
.orb-3 { width: 400px; height: 400px; background: #064e3b; top: 40%; left: 40%; animation-delay: -10s; opacity: 0.2; }

/* KEYFRAMES */
@keyframes float { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(100px, 50px) scale(1.2); } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes slideUp { from { opacity:0; transform:translateY(30px); } to { opacity:1; transform:translateY(0); } }
@keyframes slideInRight { from { opacity:0; transform:translateX(30px); } to { opacity:1; transform:translateX(0); } }
@keyframes pulseGlow { 0%,100% { box-shadow: 0 0 15px var(--accent-purple-glow); } 50% { box-shadow: 0 0 30px var(--accent-purple-glow); } }
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }
@keyframes gradientText { 0% { background-position: 0% 50%; } 100% { background-position: 100% 50%; } }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes pulse { 0%,100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.15); opacity: 0.75; } }

/* GLASSMORPHISM CARDS */
.glass-panel {
  background: var(--bg-glass);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-glass);
  transition: all var(--transition);
}
.glass-panel:hover { border-color: var(--border-default); background: var(--bg-glass-hover); }
.card-header { padding: 16px 20px; border-bottom: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; }
.card-title { font-size: 0.85rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-secondary); }

/* TOP NAV */
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(3,3,5,0.7); backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
  padding: 0 24px; display: flex; align-items: center; justify-content: space-between; height: 64px;
}
.nav-logo { display: flex; align-items: center; gap: 12px; font-size: 1.2rem; font-weight: 800; letter-spacing: -0.03em; }
.nav-logo-mark { width: 32px; height: 32px; background: var(--gradient-purple); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 900; color: white; box-shadow: var(--shadow-glow); }
.nav-logo-text { color: var(--text-primary); }
.nav-logo-text span { color: var(--accent-purple-light); }
.nav-tabs { display: flex; gap: 4px; background: var(--bg-tertiary); padding: 4px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); }
.nav-tab { padding: 8px 16px; border-radius: var(--radius-sm); font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); cursor: pointer; transition: all var(--transition); border: none; background: transparent; }
.nav-tab:hover { color: var(--text-primary); }
.nav-tab.active { color: white; background: var(--border-default); box-shadow: var(--shadow-glow); }
.nav-status { display: flex; align-items: center; gap: 16px; }

/* HERO */
.hero { min-height: 50vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 24px; text-align: center; position: relative; }
.hero-title { font-size: clamp(3.5rem, 8vw, 6rem); font-weight: 900; letter-spacing: -0.04em; line-height: 1; margin-bottom: 16px; background: linear-gradient(to right, #fff, #c4b5fd, #60a5fa, #fff); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradientText 5s linear infinite; }
.hero-tagline { font-size: 1.2rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto 32px; line-height: 1.6; }

/* SEARCH BAR */
.search-container { position: relative; width: 100%; max-width: 650px; margin: 0 auto 24px; }
.search-input { width: 100%; background: var(--bg-glass); backdrop-filter: blur(10px); border: 1px solid var(--border-default); border-radius: var(--radius-xl); padding: 20px 150px 20px 24px; font-size: 1.1rem; color: white; outline: none; transition: all var(--transition); box-shadow: 0 4px 20px rgba(0,0,0,0.3); font-family: var(--font-sans); }
.search-input:focus { border-color: var(--accent-purple-light); box-shadow: var(--shadow-glow-strong); background: rgba(20,20,40,0.8); }
.search-btn { position: absolute; right: 8px; top: 8px; bottom: 8px; background: var(--gradient-purple); border: none; border-radius: var(--radius-xl); padding: 0 24px; font-size: 0.9rem; font-weight: 700; color: white; cursor: pointer; transition: all var(--transition); }
.search-btn:hover { box-shadow: var(--shadow-glow); transform: scale(1.02); }

/* SCENARIO CHIPS */
.demo-scenarios { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; max-width: 800px; margin: 0 auto; }
.scenario-chip { background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle); padding: 8px 16px; border-radius: 100px; font-size: 0.75rem; color: var(--text-secondary); cursor: pointer; transition: all var(--transition); backdrop-filter: blur(5px); }
.scenario-chip:hover { border-color: var(--accent-purple-light); color: white; background: rgba(124,58,237,0.1); transform: translateY(-2px); }

/* AGENT TERMINAL (THE BRAIN) */
.agent-terminal { background: #050508; border: 1px solid var(--border-default); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-glow); margin-bottom: 24px; position: relative; }
.terminal-header { background: #0a0a10; padding: 10px 16px; border-bottom: 1px solid var(--border-subtle); display: flex; align-items: center; gap: 8px; }
.term-dot { width: 10px; height: 10px; border-radius: 50%; }
.term-dot.r { background: #ef4444; } .term-dot.y { background: #f59e0b; } .term-dot.g { background: #10b981; }
.terminal-title { font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); margin-left: 8px; letter-spacing: 0.1em; }
.terminal-body { padding: 20px; font-family: var(--font-mono); font-size: 0.85rem; line-height: 1.8; color: var(--text-code); height: 260px; overflow-y: auto; scroll-behavior: smooth; }
.term-line { opacity: 0; animation: slideInRight 0.3s forwards; margin-bottom: 6px; }
.term-system { color: var(--text-secondary); }
.term-success { color: var(--accent-green-light); }
.term-highlight { color: #fcd34d; }
.cursor { display: inline-block; width: 8px; height: 15px; background: var(--accent-purple-light); animation: blink 1s infinite; vertical-align: middle; margin-left: 4px; }

/* PRODUCT CARDS (STAGGERED ANIMATION) */
.products-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.product-card { background: rgba(20,20,30,0.5); backdrop-filter: blur(10px); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 20px; transition: all var(--transition); opacity: 0; position: relative; }
.product-card.reveal { animation: slideUp 0.6s cubic-bezier(0.16,1,0.3,1) forwards; }
.product-card:hover { border-color: var(--accent-purple-light); transform: translateY(-5px); box-shadow: var(--shadow-glass), var(--shadow-glow); background: rgba(30,30,45,0.7); }
.product-emoji { font-size: 3rem; margin-bottom: 12px; display: block; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3)); }
.product-brand { font-size: 0.7rem; font-weight: 800; letter-spacing: 0.15em; text-transform: uppercase; color: var(--accent-blue-light); margin-bottom: 4px; }
.product-title { font-size: 1.05rem; font-weight: 700; color: white; margin-bottom: 12px; line-height: 1.3; }
.product-price { font-size: 1.3rem; font-weight: 800; color: white; margin-bottom: 12px; }
.product-price span { font-size: 0.8rem; color: var(--text-secondary); font-weight: 500; }

/* MATCH SCORE BAR ANIMATED */
.match-score-wrap { background: rgba(0,0,0,0.3); border-radius: var(--radius-sm); padding: 10px; margin-top: 12px; border: 1px solid var(--border-subtle); }
.match-header { display: flex; justify-content: space-between; font-size: 0.7rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 6px; letter-spacing: 0.05em; }
.match-track { height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px; overflow: hidden; position: relative; }
.match-fill { position: absolute; top: 0; left: 0; height: 100%; background: var(--gradient-purple); width: 0%; border-radius: 3px; transition: width 1.2s cubic-bezier(0.16,1,0.3,1); box-shadow: 0 0 10px var(--accent-purple); }

/* BUTTONS */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 18px; border-radius: var(--radius-md); font-size: 0.85rem; font-weight: 700; cursor: pointer; transition: all var(--transition); border: 1px solid transparent; font-family: var(--font-sans); }
.btn-primary { background: var(--gradient-purple); color: white; box-shadow: 0 4px 15px rgba(124,58,237,0.3); }
.btn-primary:hover { box-shadow: var(--shadow-glow); transform: translateY(-2px); }
.btn-glass { background: rgba(255,255,255,0.05); color: white; border-color: var(--border-subtle); backdrop-filter: blur(5px); }
.btn-glass:hover { background: rgba(255,255,255,0.1); border-color: var(--accent-purple-light); }

/* LAYOUT CLASSES */
.section-container { max-width: 1400px; margin: 0 auto; padding: 40px 24px; }
.two-col-layout { display: grid; grid-template-columns: 380px 1fr; gap: 32px; align-items: start; }
.hidden { display: none !important; }
.page { display: none; opacity: 0; transition: opacity 0.4s ease; }
.page.active { display: block; opacity: 1; }

/* MISC */
.text-xs { font-size: 0.7rem; } .text-sm { font-size: 0.85rem; } .text-muted { color: var(--text-muted); }
.font-mono { font-family: var(--font-mono); }

/* CART OVERHAUL */
.cart-panel { padding: 0; overflow: hidden; }
.cart-items { max-height: 400px; overflow-y: auto; padding: 16px; }
.cart-item { display: flex; gap: 12px; padding: 12px; background: rgba(0,0,0,0.2); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); margin-bottom: 8px; }
.cart-totals { padding: 20px; background: rgba(0,0,0,0.3); border-top: 1px solid var(--border-subtle); }
.cart-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 8px; }
.cart-row.grand { font-size: 1.1rem; color: white; font-weight: 800; padding-top: 12px; border-top: 1px solid var(--border-subtle); margin-top: 12px; }

/* CHECKOUT GLOW FLOW */
.checkout-flow { display: flex; flex-direction: column; gap: 0; padding: 20px; }
.chk-node { display: flex; align-items: flex-start; gap: 16px; position: relative; padding-bottom: 24px; transition: opacity 0.3s; }
.chk-node:not(.done):not(.active) { opacity: 0.4; }
.chk-line { position: absolute; left: 15px; top: 32px; bottom: 0; width: 2px; background: rgba(255,255,255,0.05); overflow: hidden; border-radius: 2px; }
.chk-line-fill { position: absolute; top: 0; left: 0; width: 100%; background: var(--accent-cyan); height: 0%; transition: height 0.8s cubic-bezier(0.16,1,0.3,1); box-shadow: 0 0 8px var(--accent-cyan); }
.chk-node.done .chk-line-fill { height: 100%; background: var(--accent-green); box-shadow: 0 0 8px var(--accent-green); }
.chk-node.active .chk-line-fill { height: 50%; animation: pulseFill 0.8s infinite alternate; }
.chk-dot { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: var(--bg-tertiary); border: 2px solid var(--border-default); z-index: 1; font-weight: 700; font-size: 0.8rem; transition: all 0.3s; }
.chk-node.active .chk-dot { background: rgba(6,182,212,0.2); border-color: var(--accent-cyan); box-shadow: 0 0 15px rgba(6,182,212,0.5); color: white; animation: pulseDotCyan 2s infinite; }
.chk-node.done .chk-dot { background: var(--accent-green-glow); border-color: var(--accent-green); color: white; }
.chk-content { flex: 1; padding-top: 4px; }
.chk-title { font-size: 0.95rem; font-weight: 700; color: var(--text-secondary); transition: color 0.3s; }
.chk-node.active .chk-title { color: var(--accent-cyan); }
.chk-node.done .chk-title { color: var(--accent-green); }

@keyframes pulseDotCyan { 0% { box-shadow: 0 0 0 0 rgba(6,182,212,0.4); } 70% { box-shadow: 0 0 0 10px rgba(6,182,212,0); } 100% { box-shadow: 0 0 0 0 rgba(6,182,212,0); } }
@keyframes pulseFill { 0% { opacity: 0.6; } 100% { opacity: 1; } }

/* RESPONSIVE */
@media (max-width: 1000px) { .two-col-layout { grid-template-columns: 1fr; } }
@media (max-width: 600px) { .hero-title { font-size: 3rem; } }

/* ============================================================
   CHAT AGENT INTERFACE
   ============================================================ */
.chat-layout { display:flex; height:calc(100vh - 65px); overflow:hidden; }
.chat-window { flex:1; display:flex; flex-direction:column; min-width:0; }
.chat-messages { flex:1; overflow-y:auto; padding:24px 20px; display:flex; flex-direction:column; gap:12px; scroll-behavior:smooth; }
.chat-messages::-webkit-scrollbar { width:4px; }
.chat-messages::-webkit-scrollbar-thumb { background:rgba(139,92,246,0.3); border-radius:4px; }

/* Chat rows */
.chat-row { display:flex; gap:10px; align-items:flex-start; animation:slideUp 0.3s ease; max-width:100%; }
.chat-row.user-row { flex-direction:row-reverse; }
.chat-avatar { width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:0.8rem; flex-shrink:0; margin-top:2px; }
.agent-avatar { background:linear-gradient(135deg,#7c3aed,#06b6d4); }
.user-avatar { background:rgba(139,92,246,0.25); border:1px solid rgba(139,92,246,0.4); }
.chat-bubble { max-width:76%; padding:10px 14px; border-radius:14px; font-size:0.85rem; line-height:1.6; color:white; }
.agent-bubble { background:rgba(12,12,24,0.9); border:1px solid rgba(255,255,255,0.07); border-top-left-radius:4px; }
.user-bubble { background:linear-gradient(135deg,rgba(124,58,237,0.35),rgba(79,70,229,0.35)); border:1px solid rgba(139,92,246,0.4); border-top-right-radius:4px; }

/* Typing indicator */
.typing-dots { display:flex; gap:4px; padding:2px 0; align-items:center; }
.typing-dot { width:6px; height:6px; background:#a78bfa; border-radius:50%; animation:typingBounce 1.2s infinite; }
.typing-dot:nth-child(2) { animation-delay:0.2s; }
.typing-dot:nth-child(3) { animation-delay:0.4s; }
@keyframes typingBounce { 0%,60%,100% { transform:translateY(0); opacity:0.35; } 30% { transform:translateY(-5px); opacity:1; } }

/* Agent step lines */
.agent-step { font-size:0.75rem; font-family:var(--font-mono); color:var(--text-muted); margin:1px 0; animation:fadeIn 0.25s ease; }
.agent-step.s-success { color:#10b981; }
.agent-step.s-highlight { color:#a78bfa; font-weight:700; }
.agent-step.s-system { color:#60a5fa; }

/* Inline product cards */
.inline-product { display:flex; gap:10px; padding:8px 10px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07); border-radius:10px; align-items:center; margin:3px 0; animation:slideUp 0.3s ease; cursor:pointer; transition:all 0.2s; text-decoration:none; }
.inline-product:hover { background:rgba(139,92,246,0.12); border-color:rgba(139,92,246,0.35); }
.ip-img { width:42px; height:42px; border-radius:7px; object-fit:cover; background:#0d0d18; flex-shrink:0; }
.ip-info { flex:1; min-width:0; }
.ip-title { font-size:0.78rem; font-weight:700; color:white; margin-bottom:1px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.ip-meta { font-size:0.68rem; color:var(--text-muted); }
.ip-score { font-size:0.65rem; color:#a78bfa; font-weight:700; }
.ip-buy { flex-shrink:0; background:#f90; color:#111; font-weight:800; font-size:0.68rem; border:none; padding:5px 9px; border-radius:6px; cursor:pointer; white-space:nowrap; transition:opacity 0.2s; }
.ip-buy:hover { opacity:0.85; }

/* Quick prompt chips */
.quick-prompts { padding:8px 20px; display:flex; gap:6px; flex-wrap:wrap; border-top:1px solid rgba(255,255,255,0.04); }
.qp-chip { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07); color:var(--text-muted); font-size:0.72rem; padding:4px 10px; border-radius:20px; cursor:pointer; font-family:var(--font-sans); transition:all 0.2s; }
.qp-chip:hover { background:rgba(139,92,246,0.15); border-color:rgba(139,92,246,0.4); color:#a78bfa; }
.qp-chip.ucp-chip { border-color:rgba(6,182,212,0.3); color:#06b6d4; }
.qp-chip.ucp-chip:hover { background:rgba(6,182,212,0.15); }

/* MOBILE PHONE MOCKUP FOR UCP KEYNOTE SIMULATOR */
.phone-mockup {
  width: 250px;
  height: 480px;
  background: #080812;
  border-radius: 34px;
  border: 7px solid #1a1a2b;
  box-shadow: 0 0 30px rgba(6,182,212,0.3), inset 0 0 10px rgba(0,0,0,0.9);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}
.phone-notch {
  width: 80px;
  height: 16px;
  background: #000;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
}
.phone-notch-dot { width: 6px; height: 6px; background: #111; border-radius: 50%; border: 1px solid #222; }
.phone-status-bar {
  height: 24px;
  padding: 4px 14px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.58rem;
  color: var(--text-muted);
  font-family: var(--font-sans);
  z-index: 40;
}
.phone-screen {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  background: #0b0b18;
}
.gpay-sheet {
  position: absolute;
  left: 0; right: 0; bottom: -280px;
  background: rgba(16, 16, 28, 0.98);
  border-top-left-radius: 18px;
  border-top-right-radius: 18px;
  border-top: 1px solid rgba(6, 182, 212, 0.5);
  padding: 14px;
  box-shadow: 0 -10px 30px rgba(0,0,0,0.9);
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 30;
}
.gpay-sheet.show {
  transform: translateY(-280px);
}

/* Chat input bar */
.chat-input-bar { padding:10px 16px 14px; border-top:1px solid rgba(255,255,255,0.06); display:flex; gap:8px; background:rgba(8,8,18,0.95); backdrop-filter:blur(20px); align-items:center; }
.chat-input { flex:1; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.09); border-radius:12px; padding:11px 16px; color:white; font-size:0.88rem; font-family:var(--font-sans); outline:none; transition:border-color 0.2s; }
.chat-input:focus { border-color:rgba(139,92,246,0.5); background:rgba(255,255,255,0.07); }
.chat-input::placeholder { color:var(--text-muted); }
.chat-send-btn { background:linear-gradient(135deg,#7c3aed,#4f46e5); color:white; border:none; border-radius:12px; padding:11px 18px; font-weight:800; font-size:0.82rem; cursor:pointer; transition:opacity 0.2s; white-space:nowrap; font-family:var(--font-sans); }
.chat-send-btn:hover { opacity:0.85; }
.chat-send-btn:disabled { opacity:0.4; cursor:not-allowed; }

/* Brain sidebar */
.brain-sidebar { width:260px; flex-shrink:0; border-left:1px solid rgba(255,255,255,0.05); background:rgba(8,8,18,0.7); backdrop-filter:blur(20px); overflow-y:auto; padding:0; display:none; }
.brain-sidebar::-webkit-scrollbar { width:3px; }
.brain-sidebar::-webkit-scrollbar-thumb { background:rgba(139,92,246,0.3); }
.brain-section { padding:14px 14px 10px; border-bottom:1px solid rgba(255,255,255,0.04); }
.brain-label { font-size:0.6rem; font-weight:800; color:var(--text-muted); letter-spacing:1px; margin-bottom:8px; }
.brain-row { display:flex; justify-content:space-between; font-size:0.72rem; margin-bottom:4px; }
.brain-key { color:var(--text-muted); }
.brain-val { color:white; font-weight:600; max-width:130px; text-align:right; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.brain-bar-row { margin-bottom:5px; }
.brain-bar-label { display:flex; justify-content:space-between; font-size:0.66rem; margin-bottom:2px; }
.brain-bar-track { height:3px; background:rgba(255,255,255,0.06); border-radius:3px; overflow:hidden; }
.brain-bar-fill { height:100%; border-radius:3px; transition:width 0.8s ease; }
.step-indicator { display:flex; align-items:center; gap:6px; font-size:0.72rem; margin-bottom:6px; }
.step-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.step-dot.done { background:#10b981; }
.step-dot.active { background:#06b6d4; animation:pulseDotCyan 1.5s infinite; }
.step-dot.pending { background:rgba(255,255,255,0.15); }
</style>
</head>
<body>
<div class="mesh-bg">
  <div class="mesh-orb orb-1"></div>
  <div class="mesh-orb orb-2"></div>
  <div class="mesh-orb orb-3"></div>
</div>

<div class="app-container">

<!-- TOP NAV -->
<nav class="top-nav">
  <div class="nav-logo">
    <div class="nav-logo-mark">C</div>
    <div class="nav-logo-text">Commerce<span>OS</span></div>
  </div>
  <div style="flex:1;"></div>
  <button class="nav-tab active" data-page="shopper">Try It Live</button>
  <button class="nav-tab" data-page="developer">How It Works</button>
  <button class="nav-tab" data-page="architecture">Architecture</button>
  <button class="nav-tab" data-page="ucp">UCP Protocol</button>
  <div style="flex:1;display:flex;justify-content:flex-end;align-items:center;gap:12px;padding-right:16px;">
    <a href="https://huggingface.co/ShivanshiNigam" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:6px;text-decoration:none;background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.3);border-radius:20px;padding:5px 12px;font-size:0.72rem;color:#a78bfa;font-weight:600;white-space:nowrap;transition:0.2s;" onmouseover="this.style.background='rgba(139,92,246,0.3)'" onmouseout="this.style.background='rgba(139,92,246,0.15)'">
      <span style="width:18px;height:18px;background:linear-gradient(135deg,#7c3aed,#06b6d4);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.65rem;font-weight:800;color:white;">S</span>
      Shivanshi Nigam
    </a>
    <button id="settings-btn" style="background:transparent;border:none;color:var(--text-secondary);font-size:0.8rem;cursor:pointer;padding:6px 10px;border:1px solid rgba(255,255,255,0.1);border-radius:6px;transition:0.2s;" title="API Settings">Settings</button>
  </div>
</nav>

<!-- Settings Modal -->
<div id="settings-modal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);backdrop-filter:blur(5px);z-index:9999;align-items:center;justify-content:center;">
  <div style="background:var(--surface);border:1px solid var(--border);padding:24px;border-radius:var(--radius-lg);width:420px;max-width:90%;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
      <h3 style="margin:0;font-size:1.1rem;font-weight:700;">LLM API Key Settings (Optional)</h3>
      <button id="settings-close-btn" style="background:transparent;border:none;color:var(--text);cursor:pointer;font-size:1.2rem;">✕</button>
    </div>
    <div style="padding:8px 12px;background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:8px;color:#10b981;font-size:0.75rem;font-weight:700;margin-bottom:14px;">
      ✓ No API Key Required! CommerceOS works 100% out of the box using built-in NLP intent parsing.
    </div>
    <p style="font-size:0.82rem;color:var(--text-muted);margin-bottom:16px;line-height:1.5;">
      Optional: Enter your Groq/Gemini API Key if you want to test live LLM intent reasoning directly in your browser. Key is stored locally in your browser and never sent to any server.
    </p>
    <div class="input-group" style="margin-bottom:16px;">
      <input type="password" id="gemini-key-input" placeholder="gsk_... (Optional)" style="width:100%;" />
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;">
      <button id="settings-clear-btn" class="btn btn-secondary">Clear</button>
      <button id="settings-save-btn" class="btn btn-primary">Save Key</button>
    </div>
  </div>
</div>

<!-- SHOPPER PAGE — CHAT AGENT INTERFACE -->
<div class="page active" id="page-shopper">

  <!-- GOOGLE UCP PROTOCOL SUMMARY BANNER (TOP) -->
  <div style="max-width:1200px;margin:0 auto 20px;padding:18px 24px;background:linear-gradient(135deg,rgba(15,23,42,0.95),rgba(30,27,75,0.9));border:1px solid rgba(6,182,212,0.4);border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
    <div style="flex:1;min-width:300px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
        <span style="font-size:0.75rem;font-weight:800;color:#06b6d4;background:rgba(6,182,212,0.15);border:1px solid rgba(6,182,212,0.3);padding:3px 10px;border-radius:4px;letter-spacing:0.5px;">GOOGLE UCP ENGINE ACTIVE</span>
        <span style="font-size:1.05rem;font-weight:800;color:white;">Google Universal Commerce Protocol (UCP v2026-04-08)</span>
      </div>
      <div style="font-size:0.8rem;color:var(--text-secondary);line-height:1.55;">
        Enables Gemini AI to discover merchant catalogs (`/.well-known/ucp`), request session locks (`POST /checkout-sessions`), and settle transactions directly via Google Pay tokens.
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
      <button onclick="document.querySelector('[data-page=ucp]').click();" style="background:linear-gradient(135deg,#0891b2,#7c3aed);color:white;border:none;padding:10px 18px;border-radius:10px;font-weight:700;font-size:0.82rem;cursor:pointer;box-shadow:0 0 15px rgba(6,182,212,0.3);transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
        Open Full UCP Protocol Explorer →
      </button>
    </div>
  </div>

  <!-- ONBOARDING HERO CARD -->
  <div class="project-intro-hero" style="max-width:1200px;margin:0 auto 20px;padding:22px 26px;background:linear-gradient(135deg,rgba(15,15,30,0.95),rgba(20,20,45,0.9));border:1px solid rgba(139,92,246,0.3);border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,0.5);">
    
    <!-- HERO HEADER -->
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);">
      <div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
          <span style="font-size:1.4rem;color:white;font-weight:900;letter-spacing:-0.5px;">CommerceOS</span>
          <span style="font-size:0.68rem;background:rgba(6,182,212,0.15);color:#06b6d4;border:1px solid rgba(6,182,212,0.3);padding:2px 8px;border-radius:4px;font-weight:700;">AGENT &amp; UCP DEMONSTRATION LAB</span>
        </div>
        <h1 style="font-size:1.05rem;font-weight:700;color:white;margin:0;line-height:1.4;">
          Autonomous Agentic Commerce Platform &amp; Google UCP Direct Buying Simulator
        </h1>
        <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;">
          Demonstrating natural language intent parsing, multi-constraint ranking, and direct protocol checkout.
          <span style="color:#f59e0b;font-weight:600;">[Notice: Operating on a simulated demonstration catalog &amp; live DummyJSON dataset]</span>
        </div>
      </div>
      
      <!-- ACTION BUTTON -->
      <div>
        <button id="hero-get-started-btn" onclick="document.getElementById('main-query-input')?.focus(); document.querySelector('.chat-layout')?.scrollIntoView({behavior:'smooth'});" style="background:linear-gradient(135deg,#7c3aed,#06b6d4);color:white;border:none;padding:10px 20px;border-radius:10px;font-size:0.85rem;font-weight:700;cursor:pointer;box-shadow:0 0 15px rgba(124,58,237,0.3);transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.03)'" onmouseout="this.style.transform='scale(1)'">
          Start Agent Session →
        </button>
      </div>
    </div>

    <!-- 3 GUIDANCE COLUMNS -->
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;">
      
      <!-- COLUMN 1 -->
      <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;">
        <div style="font-size:0.82rem;font-weight:700;color:white;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
          <span style="color:#a78bfa;font-size:0.75rem;">[1]</span> System Overview
        </div>
        <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.55;">
          • Extracts NLP intent (budget boundaries like ₹50k/5L, brand preferences, categories).<br/>
          • Searches catalog candidates and applies hard/soft constraints.<br/>
          • Ranks products using a 6-dimensional weighted scoring model.<br/>
          • Executes direct checkout via Google Universal Commerce Protocol (UCP).
        </div>
      </div>

      <!-- COLUMN 2 -->
      <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;">
        <div style="font-size:0.82rem;font-weight:700;color:white;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
          <span style="color:#06b6d4;font-size:0.75rem;">[2]</span> Operating Instructions
        </div>
        <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.55;">
          1. Enter a natural language request (e.g. <em>"iPhone 15 under 80k"</em>).<br/>
          2. Inspect intent extraction and ranking details in the AI Brain sidebar.<br/>
          3. Click <strong>Buy via UCP</strong> to trigger the live mobile payment simulation.
        </div>
      </div>

      <!-- COLUMN 3 -->
      <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px;">
        <div style="font-size:0.82rem;font-weight:700;color:white;margin-bottom:8px;display:flex;align-items:center;gap:6px;">
          <span style="color:#10b981;font-size:0.75rem;">[3]</span> Protocol &amp; Data Scope
        </div>
        <div style="font-size:0.75rem;color:var(--text-secondary);line-height:1.55;">
          • <strong>Data Scope</strong>: Uses simulated flagship pricing &amp; live DummyJSON catalog.<br/>
          • <strong>Search Links</strong>: Verified search queries for Amazon &amp; Flipkart.<br/>
          • <strong>UCP Standard</strong>: Real JSON payload structure (`/.well-known/ucp`, tokens).
        </div>
      </div>

    </div>
  </div>

  <div class="chat-layout">

    <!-- MAIN CHAT WINDOW -->
    <div class="chat-window">
      <div id="chat-messages" class="chat-messages">
        <!-- Greeting injected by JS on init -->
      </div>

      <!-- Quick prompts -->
      <div class="quick-prompts">
        <span style="font-size:0.65rem;color:var(--text-muted);margin-right:4px;">Suggested:</span>
        <button class="qp-chip" data-query="Complete party outfit under ₹5,000">✨ Complete Outfit Bundle</button>
        <button class="qp-chip" data-query="Find wireless headphones under ₹10,000 with excellent battery life">Headphones under ₹10k</button>
        <button class="qp-chip" data-query="Find a laptop under ₹80,000 for Python and machine learning">ML laptop under ₹80k</button>
        <button class="qp-chip" data-query="Find running shoes under ₹8,000, size 7, for daily road running">Running shoes under ₹8k</button>
        <button class="qp-chip ucp-chip" id="hero-ucp-chip">Simulate UCP Buy</button>
      </div>

      <!-- Input bar -->
      <div class="chat-input-bar">
        <input type="text" id="main-query-input" class="chat-input" placeholder="Enter query — e.g. 'Sony headphones under ₹10k' or 'iPhone 15 under 80k'" autocomplete="off" />
        <button id="run-agent-btn" class="chat-send-btn">Send →</button>
      </div>
    </div>

    <!-- RIGHT: AI BRAIN SIDEBAR -->
    <div class="brain-sidebar" id="brain-sidebar">
      <div style="padding:12px 14px;background:rgba(124,58,237,0.12);border-bottom:1px solid rgba(124,58,237,0.2);display:flex;align-items:center;gap:8px;">
        <span style="font-size:0.7rem;font-weight:800;color:#a78bfa;letter-spacing:1px;">AI BRAIN TRACE</span>
      </div>


      <div class="brain-section" id="brain-steps">
        <div class="brain-label">PIPELINE STEPS</div>
        <div class="step-indicator"><div class="step-dot pending" id="step-parse"></div><span style="color:var(--text-muted);">Parse Intent</span></div>
        <div class="step-indicator"><div class="step-dot pending" id="step-search"></div><span style="color:var(--text-muted);">Search Catalog</span></div>
        <div class="step-indicator"><div class="step-dot pending" id="step-filter"></div><span style="color:var(--text-muted);">Apply Constraints</span></div>
        <div class="step-indicator"><div class="step-dot pending" id="step-rank"></div><span style="color:var(--text-muted);">Rank Results</span></div>
      </div>

      <div class="brain-section" id="brain-intent-section" style="display:none;">
        <div class="brain-label">INTENT PARSED</div>
        <div id="brain-intent-rows"></div>
      </div>

      <div class="brain-section" id="brain-score-section" style="display:none;">
        <div class="brain-label">TOP PICK SCORES</div>
        <div id="brain-score-name" style="font-size:0.7rem;color:white;font-weight:700;margin-bottom:8px;"></div>
        <div id="brain-score-bars"></div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.05);">
          <span style="font-size:0.65rem;color:var(--text-muted);">Total</span>
          <span id="brain-total-score" style="font-size:0.95rem;font-weight:900;color:#a78bfa;"></span>
        </div>
      </div>

      <div class="brain-section" id="brain-stats-section" style="display:none;">
        <div class="brain-label">RESULTS</div>
        <div id="brain-stats-rows"></div>
      </div>

      <!-- UCP MINI INFO -->
      <div class="brain-section">
        <div class="brain-label">PROTOCOL</div>
        <div style="font-size:0.7rem;color:#06b6d4;font-weight:700;margin-bottom:4px;">Google UCP v2026-04-08</div>
        <div style="font-size:0.65rem;color:var(--text-muted);line-height:1.5;">This agent follows the real Google Universal Commerce Protocol for agentic buying.</div>
        <button onclick="document.querySelector('[data-page=ucp]').click()" style="margin-top:8px;font-size:0.65rem;color:#06b6d4;background:transparent;border:1px solid rgba(6,182,212,0.3);border-radius:6px;padding:3px 8px;cursor:pointer;font-family:var(--font-sans);">View UCP Simulator →</button>
      </div>

      <!-- CTA -->
      <div class="brain-section">
        <div class="brain-label">BUILT BY</div>
        <div style="font-size:0.75rem;font-weight:700;color:white;margin-bottom:4px;">Shivanshi Nigam</div>
        <div style="font-size:0.65rem;color:var(--text-muted);line-height:1.5;margin-bottom:8px;">I build custom AI commerce agents for Shopify, WooCommerce, and custom platforms.</div>
        <a href="https://huggingface.co/ShivanshiNigam" target="_blank" style="display:block;text-align:center;font-size:0.68rem;font-weight:700;background:linear-gradient(135deg,#7c3aed,#4f46e5);color:white;padding:6px 10px;border-radius:8px;text-decoration:none;">🤗 View My Work</a>
      </div>
    </div>

  </div>
</div>

<!-- STUBS FOR OTHER MODES -->
<div class="page" id="page-developer"><div class="section-container"><h2 class="text-primary" style="font-size:2rem;margin-bottom:20px;">Developer Mode</h2><div class="glass-panel" style="padding:20px;height:400px;display:flex;align-items:center;justify-content:center;color:var(--text-muted);">Developer features active in backend</div></div></div>
<div class="page" id="page-architecture"><div class="section-container"><h2 class="text-primary" style="font-size:2rem;margin-bottom:20px;">Architecture</h2><div class="glass-panel" style="padding:20px;height:400px;display:flex;align-items:center;justify-content:center;color:var(--text-muted);">Architecture view active</div></div></div>
<div class="page" id="page-ucp"><div class="section-container"><h2 class="text-primary" style="font-size:2rem;margin-bottom:20px;">UCP Explorer</h2><div class="glass-panel" style="padding:20px;height:400px;display:flex;align-items:center;justify-content:center;color:var(--text-muted);">UCP configuration active</div></div></div>

<!-- TOAST -->
<div id="toast" style="position:fixed;bottom:24px;right:24px;padding:12px 20px;background:var(--accent-purple);color:white;border-radius:var(--radius-sm);box-shadow:var(--shadow-glow);font-weight:700;transform:translateY(100px);opacity:0;transition:all 0.3s;z-index:9999;"></div>

<script>
// Expose simple toast
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.style.transform = 'translateY(0)'; t.style.opacity = '1';
  setTimeout(() => { t.style.transform = 'translateY(100px)'; t.style.opacity = '0'; }, 3000);
  // UCP_VERSION and ENV_LABEL are declared in Part 2 (strict-mode) to avoid duplicate const error
}
</script>
'''

if __name__ == '__main__':
    with open('index.html', 'w') as f:
        f.write(HTML_PART1)
    print("Part 1 V2 generated -> index.html")
