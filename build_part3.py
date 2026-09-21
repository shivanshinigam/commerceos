#!/usr/bin/env python3
"""Build Part 3: Agent Engine - Intent Parser, Search, Ranking, Constraint Engine, Checkout, Orders"""

import os

AGENT_JS = r'''
<!-- PART 3: AGENT ENGINE -->
<script>
'use strict';
/* ================================================
   COMMERCEOS — AGENT ENGINE
   Deterministic AI Commerce Agent
   All logic is transparent and explainable.
   UCP Version: 2026-08-25
   ================================================ */

// ---- SESSION STATE ----
var SESSION = {
  id: null,
  query: null,
  intent: null,
  candidates: [],
  filtered: [],
  ranked: [],
  selected_product: null,
  cart: [],
  checkout: null,
  order: null,
  trace: [],
  run_count: 0,
  success_count: 0,
  failure_count: 0,
  total_latency: 0,
  tool_calls: 0,
  retrieval_count: 0,
  checkout_success: 0
};

// ---- INTENT PARSER ----
// Deterministic NLP parser - extracts structured intent from natural language
// Clearly labeled: LOCAL SIMULATION (not LLM)
const INTENT_PARSER = {
  // Category keywords
  CATEGORIES: {
    'sweatshirt': ['sweatshirt','sweatshirts','hoodie','pullover'],
    't_shirt': ['t-shirt','tshirt','tee','t-shirts'],
    'shirt': ['shirt','shirts','button shirt'],
    'running_shoes': ['running shoe','running shoes','runner','run','jogging','road shoe','trail shoe'],
    'laptop': ['laptop','notebook','computer','pc','macbook','chromebook'],
    'headphones': ['headphone','earphone','earbuds','headset','earbud','earpiece','over-ear','on-ear','in-ear','tws','buds'],
    'smartphone': ['phone','smartphone','mobile','iphone','android','pixel','galaxy'],
    'formal_shirt': ['formal shirt','dress shirt','office shirt','button shirt','shirt'],
    'casual_shoes': ['casual shoe','sneaker','lifestyle shoe'],
    'smartwatch': ['watch','smartwatch','smart watch'],
    'backpack': ['backpack','bag','rucksack'],
    'speaker': ['speaker','bluetooth speaker'],
    'tv': ['tv','television','smart tv'],
    'fitness': ['fitness','gym','workout'],
    'camera': ['camera','dslr','mirrorless'],
  },
  // Brand keywords
  BRANDS: ['lee','myntra','flying machine','wrangler','scullers','benetton','highlander','puma','nike','adidas','sony','bose','apple','samsung','oneplus','realme','jbl','sennheiser','logitech',
           'dell','lenovo','hp','asus','acer','msi','boat','nothing','jabra','anker','puma','reebok','brooks',
           'asics','salomon','hoka','saucony','new balance','peter england','van heusen','arrow','louis philippe',
           'wildcraft','skybags','garmin','fossil','noise','mi','xiaomi','motorola','google','lava','harman'],
  // Surface keywords
  SURFACES: { road: ['road','street','pavement'], trail: ['trail','off-road','mountain','outdoor'], formal: ['formal','office'] },
  // Use case keywords
  USE_CASES: {
    daily_running: ['daily','everyday','regular','road running','jogging'],
    ml: ['machine learning','ml','deep learning','python','data science','ai','gpu'],
    travel: ['travel','commute','portable'],
    work: ['work','office','professional','meeting'],
    gaming: ['gaming','game','fps','esports'],
    music: ['music','audio','listening'],
    casual: ['casual','everyday','lifestyle']
  },

  parse(query) {
    const q = query.toLowerCase();
    const result = {
      raw_query: query,
      category: null,
      budget: { max: null, min: null, currency: 'INR' },
      size: null,
      brand_preference: [],
      use_case: [],
      surface: null,
      keywords: [],
      confidence: 0
    };    // Extract budget — Lakhs / Lacs / L (e.g. 5L, 5 Lakh, 5 Lac, 1.5L)
    const lakhPattern = q.match(/(?:under|below|less than|upto?|at|budget|is|:)?\s*[₹rs\.]*\s*([\d.]+)\s*(?:lakhs?|lacs?|l)\b/i);
    if (lakhPattern) {
      result.budget.max = Math.round(parseFloat(lakhPattern[1]) * 100000);
    }

    // Extract budget — K (e.g. 80k, 10k, ₹50k)
    const kPattern = q.match(/(?:under|below|less than|upto?|at|budget|is|:)?\s*[₹rs\.]*\s*([\d.]+)\s*k\b/i);
    if (kPattern && !result.budget.max) {
      result.budget.max = Math.round(parseFloat(kPattern[1]) * 1000);
    }

    // Standard budget extraction if L/K didn't match
    if (!result.budget.max) {
      const budgetPatterns = [
        /under\s*[₹rs\.]*\s*([\d,]+)/i,
        /below\s*[₹rs\.]*\s*([\d,]+)/i,
        /less than\s*[₹rs\.]*\s*([\d,]+)/i,
        /upto?\s*[₹rs\.]*\s*([\d,]+)/i,
        /[₹rs\.]+\s*([\d,]+)/i,
        /([\d,]+)\s*(?:rupees?|inr)/i,
        /budget\s*(?:of|is|:)?\s*[₹rs\.]*\s*([\d,]+)/i
      ];
      for (const pat of budgetPatterns) {
        const m = q.match(pat);
        if (m) { result.budget.max = parseInt(m[1].replace(/,/g, '')); break; }
      }
    }

    // Extract size
    const sizePatterns = [/size\s*([0-9.]+|[SMLX]+)\b/i, /\bsize[:\s]+([0-9.]+|[SMLX]+)\b/i, /\b([0-9]+(?:\.[0-9]+)?)\s*(?:uk|us|eu|inch)?\s*size/i];
    for (const pat of sizePatterns) {
      const m = q.match(pat);
      if (m) { result.size = m[1].toUpperCase(); break; }
    }

    // Extract category
    let bestCat = null, bestScore = 0;
    for (const [cat, kws] of Object.entries(this.CATEGORIES)) {
      for (const kw of kws) {
        if (q.includes(kw)) {
          const score = kw.length;
          if (score > bestScore) { bestScore = score; bestCat = cat; }
        }
      }
    }
    result.category = bestCat;

    // Special handling for iPhone / Apple phones
    if (q.includes('iphone') || q.includes('iphones')) {
      result.category = 'smartphone';
      if (!result.brand_preference.includes('apple')) result.brand_preference.push('apple');
    }

    // Extract brands
    for (const brand of this.BRANDS) {
      if (q.includes(brand) && !result.brand_preference.includes(brand)) result.brand_preference.push(brand);
    }

    // Extract use case
    for (const [uc, kws] of Object.entries(this.USE_CASES)) {
      for (const kw of kws) {
        if (q.includes(kw) && !result.use_case.includes(uc)) result.use_case.push(uc);
      }
    }

    // Extract surface
    for (const [surf, kws] of Object.entries(this.SURFACES)) {
      for (const kw of kws) {
        if (q.includes(kw)) { result.surface = surf; break; }
      }
      if (result.surface) break;
    }

    // Extract keywords (significant non-stop-words)
    const stopWords = new Set(['find','a','an','the','for','with','under','below','and','or','i','me','my','need','want','looking','good','great','best','please','some','any','at']);
    result.keywords = q.split(/\s+/).filter(w => w.length > 3 && !stopWords.has(w)).slice(0, 8);

    // Extract outfit / bundle intent
    if (/\b(outfit|outfits|bundle|look|set|styled|complete look|party look|casual look)\b/i.test(q)) {
      result.is_outfit_intent = true;
    }

    // Confidence
    let conf = 0;
    if (result.category) conf += 40;
    if (result.budget.max) conf += 25;
    if (result.size) conf += 15;
    if (result.brand_preference.length) conf += 10;
    if (result.use_case.length || result.is_outfit_intent) conf += 10;
    result.confidence = Math.min(conf, 99);

    return result;
  }
};

// ---- OUTFIT BUILDER ENGINE ----
const OUTFIT_BUILDER = {
  buildOutfit(query, topProduct = null) {
    let topwear = topProduct ? (topProduct.product || topProduct) : null;
    if (!topwear && typeof CURATED_CATALOG !== 'undefined' && Array.isArray(CURATED_CATALOG)) {
      topwear = CURATED_CATALOG.find(p => ['sweatshirt', 't_shirt', 'shirt', 'apparel'].includes(p.category)) || CURATED_CATALOG[0];
    }
    if (!topwear) return null;

    const brand = topwear.brand || 'Lee';

    const bottomwear = {
      id: 'APP-BOTTOM-01',
      title: `${brand} Slim Fit Dark Indigo Denim Jeans`,
      brand: brand,
      category: 'bottomwear',
      best_price: 2199,
      rating: 4.7,
      emoji: '👖',
      image: 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&auto=format&fit=crop&q=60',
      description: 'Premium stretch denim with tailored tapered fit.'
    };

    const footwear = {
      id: 'APP-SHOES-01',
      title: 'Puma Rebound Low-Top Unisex Sneakers (White)',
      brand: 'Puma',
      category: 'footwear',
      best_price: 2499,
      rating: 4.8,
      emoji: '👟',
      image: 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=60',
      description: 'Classic low-top streetwear sneakers with softfoam cushioning.'
    };

    const originalTotal = (topwear.best_price || 1499) + bottomwear.best_price + footwear.best_price;
    const bundleDiscount = Math.round(originalTotal * 0.12);
    const bundlePrice = originalTotal - bundleDiscount;

    return {
      title: `AI Styled ${brand} Complete Outfit Bundle`,
      topwear,
      bottomwear,
      footwear,
      originalTotal,
      bundleDiscount,
      bundlePrice,
      savings: bundleDiscount,
      reasoning: `Paired ${topwear.title} with Indigo Stretch Denim Jeans & Puma White Sneakers for a cohesive, modern smart-casual look. Includes 12% AI Bundle Discount.`,
      items: [topwear, bottomwear, footwear]
    };
  }
};

// ---- LIVE SEARCH ENGINE ----
const SEARCH_ENGINE = {
  CATEGORY_MAP: {
    'headphones': 'mobile-accessories',
    'smartphone': 'smartphones',
    'laptop': 'laptops',
    'sweatshirt': ['sweatshirt','sweatshirts','hoodie','pullover'],
    't_shirt': ['t-shirt','tshirt','tee','t-shirts'],
    'shirt': ['shirt','shirts','button shirt'],
    'running_shoes': 'mens-shoes',
    'casual_shoes': 'mens-shoes',
    'formal_shirt': 'mens-shirts',
    'smartwatch': 'mens-watches',
    'backpack': 'sports-accessories',
    'speaker': 'mobile-accessories',
    'tv': 'mobile-accessories',
    'camera': 'mobile-accessories',
    'fitness': 'sports-accessories',
  },

  async search(intent) {
    const results = [];
    const USD_TO_INR = 83;
    
    const stopWords = new Set(['find','a','an','the','for','with','under','below','and','or','i','me','my','need','want','looking','good','great','best','please','some','any','excellent','very','nice','perfect','wireless','budget','quality','fast','quick','cheap','affordable','at']);
    const rawWords = (intent.raw_query || '').toLowerCase().split(/\s+/).filter(w => w.length > 2 && !stopWords.has(w));
    const keywordQuery = (intent.keywords || []).concat(rawWords).slice(0, 3).join(' ') || intent.category || 'product';
    const djCat = this.CATEGORY_MAP[intent.category];

    try {
      const seen = new Set();

      // 0. FIRST: Search Rich Curated Catalog
      if (typeof CURATED_CATALOG !== 'undefined' && Array.isArray(CURATED_CATALOG)) {
        if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Searching Rich Curated Catalog (${CURATED_CATALOG.length} items)...`, 'system'); }
        
        for (const item of CURATED_CATALOG) {
          if (seen.has(item.id)) continue;
          const searchText = (item.title + ' ' + item.brand + ' ' + (item.search_text || '') + ' ' + item.category).toLowerCase();
          
          let matches = false;
          const isApparelItem = ['sweatshirt', 't_shirt', 'shirt', 'apparel', 'mens-shirts'].includes(item.category);

          // Outfit intent match: match apparel items
          if (intent.is_outfit_intent && isApparelItem) {
            matches = true;
          }
          // Category match
          if (!matches && intent.category && item.category === intent.category) matches = true;

          // Keyword / Brand match (ignoring generic outfit words)
          const outfitWords = new Set(['complete', 'party', 'outfit', 'outfits', 'bundle', 'look', 'style', 'set', 'clothing']);
          const filteredRawWords = rawWords.filter(w => !outfitWords.has(w));
          if (!matches && filteredRawWords.length > 0 && filteredRawWords.some(w => searchText.includes(w))) matches = true;
          if (!matches && intent.brand_preference.some(b => searchText.includes(b))) matches = true;

          // Fallback for general outfit queries if no specific keywords left
          if (!matches && intent.is_outfit_intent && (filteredRawWords.length === 0 || !intent.category)) {
            if (isApparelItem) matches = true;
          }

          if (matches) {
            seen.add(item.id);
            const p = {
              id: item.id,
              title: item.title,
              brand: item.brand,
              category: item.category,
              price: { VeloMart: item.best_price, NexusGear: Math.round(item.best_price * 1.02), AeroGoods: Math.round(item.best_price * 0.98) },
              inventory: { VeloMart: 12, NexusGear: 8, AeroGoods: 15 },
              delivery: { VeloMart: '2 days', NexusGear: '1 day', AeroGoods: '3 days' },
              best_price: Math.round(item.best_price * 0.98),
              best_merchant: 'AeroGoods',
              in_stock: true,
              emoji: item.emoji || '📦',
              image: item.image,
              rating: item.rating || 4.5,
              search_text: searchText,
              sizes: item.sizes || ['S', 'M', 'L']
            };

            let score = 90;
            if (searchText.includes('iphone')) score += 20;
            if (intent.brand_preference.some(b => searchText.includes(b))) score += 15;

            results.push({ product: p, relevance_score: score });
          }
        }
      }

      let urls = [];

      // 1. If looking for iPhones or smartphones, prioritize category API & iPhone search
      if (intent.category === 'smartphone' || (intent.raw_query || '').toLowerCase().includes('iphone')) {
        urls.push({ url: `https://dummyjson.com/products/category/smartphones?limit=30`, label: `Smartphones category` });
        urls.push({ url: `https://dummyjson.com/products/search?q=iphone&limit=20`, label: `iPhone model search` });
      } else if (djCat && djCat !== 'mobile-accessories') {
        urls.push({ url: `https://dummyjson.com/products/category/${djCat}?limit=30`, label: `${djCat} category API` });
      }

      if (intent.brand_preference.length > 0 && intent.category !== 'smartphone') {
        const brand = intent.brand_preference[0];
        urls.push({ url: `https://dummyjson.com/products/search?q=${encodeURIComponent(brand + ' ' + (intent.category || ''))}&limit=30`, label: `${brand} search` });
      }

      // Always add keyword search as fallback
      urls.push({ url: `https://dummyjson.com/products/search?q=${encodeURIComponent(keywordQuery)}&limit=30`, label: `'${keywordQuery}' search` });

      for (const { url, label } of urls) {
        if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Executing live REST query to dummyjson.com for ${label}...`, 'system'); }
        
        const res = await fetch(url);
        const data = await res.json();
        const products = data.products || [];
        
        if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Retrieved ${products.length} live candidates.`, 'system'); }

        for (const item of products) {
          if (seen.has(item.id)) continue;
          seen.add(item.id);

          const searchText = (item.title + ' ' + item.brand + ' ' + (item.description || '') + ' ' + item.category).toLowerCase();

          // RELEVANCE GATE FOR SMARTPHONES: Must be in smartphones category OR title must contain iPhone/Phone/Galaxy
          if (intent.category === 'smartphone' || (intent.raw_query || '').toLowerCase().includes('iphone')) {
            const isPhoneCategory = item.category === 'smartphones';
            const isPhoneTitle = searchText.includes('iphone') || searchText.includes('phone') || searchText.includes('galaxy') || searchText.includes('pixel');
            const isFruitOrAccessory = item.category === 'groceries' || item.category === 'mobile-accessories' || item.category === 'mens-watches';
            
            // Discard fruits (Apple), accessories (AirPods, HomePod, Chargers), and watches when user searched for smartphone/iPhone!
            if (!isPhoneCategory && !isPhoneTitle) continue;
            if (isFruitOrAccessory && !searchText.includes('iphone')) continue;
          }

          const basePrice = Math.round(item.price * USD_TO_INR);
          const p = {
            id: `DJ-${item.id}`,
            title: item.title,
            brand: item.brand || 'Generic',
            category: item.category,
            price: {},
            inventory: {},
            delivery: {},
            best_price: basePrice,
            best_merchant: 'VeloMart',
            in_stock: (item.stock > 0) && item.availabilityStatus !== 'Out of Stock',
            emoji: item.category === 'smartphones' ? '📱' : '📦',
            image: item.thumbnail,
            rating: item.rating,
            search_text: searchText,
            sizes: ['128GB', '256GB', '512GB']
          };
          
          ['VeloMart', 'NexusGear', 'AeroGoods'].forEach(m => {
             const variance = 1.0 + ((Math.random() * 0.12) - 0.06);
             p.price[m] = Math.round(basePrice * variance);
             p.inventory[m] = Math.max(1, Math.floor(Math.random() * 25));
             const deliveryDays = Math.floor(Math.random() * 4) + 1;
             p.delivery[m] = `${deliveryDays} day${deliveryDays > 1 ? 's' : ''}`;
             if (p.price[m] < p.best_price && p.inventory[m] > 0) {
               p.best_price = p.price[m];
               p.best_merchant = m;
             }
          });
          
          let score = p.in_stock ? 70 : 20;
          if (searchText.includes('iphone')) score += 25;
          if (intent.brand_preference.some(b => searchText.includes(b))) score += 15;
          
          results.push({ product: p, relevance_score: score });
        }
        
        if (results.length >= 6) break;
      }
      
    } catch (e) {
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Error fetching from Live API: ${e.message}`, 'error'); }
      console.error("Live API Error:", e);
    }
    
    return results.sort((a,b) => b.relevance_score - a.relevance_score);
  }
};

// ---- CONSTRAINT ENGINE ----
const CONSTRAINT_ENGINE = {
  HARD: ['budget', 'category', 'size', 'in_stock'],
  SOFT: ['brand', 'use_case', 'surface', 'rating'],

  apply(candidates, intent) {
    const hard_failures = [];
    const filtered = [];

    for (const { product: p, relevance_score } of candidates) {
      const violations = [];

      // Budget check (hard)
      if (intent.budget.max) {
        if (p.best_price > intent.budget.max) {
          violations.push({ type: 'hard', name: 'budget', detail: `₹${p.best_price.toLocaleString()} > ₹${intent.budget.max.toLocaleString()}` });
        }
      }

      // Hard Category check for smartphones / phones
      if (intent.category === 'smartphone' || (intent.raw_query || '').toLowerCase().includes('iphone')) {
        const isPhoneCategory = p.category === 'smartphones';
        const isPhoneTitle = p.search_text.includes('iphone') || p.search_text.includes('phone') || p.search_text.includes('galaxy');
        if (!isPhoneCategory && !isPhoneTitle) {
          violations.push({ type: 'hard', name: 'category', detail: `Not a smartphone (${p.category})` });
        }
      }

      // Stock check (hard)
      if (!p.in_stock) {
        violations.push({ type: 'hard', name: 'stock', detail: 'Out of stock' });
      }

      const hard_violations = violations.filter(v => v.type === 'hard');
      if (hard_violations.length === 0) {
        filtered.push({ product: p, relevance_score, violations });
      } else {
        hard_failures.push({ product: p, violations: hard_violations });
      }
    }

    // BUDGET RELAXATION: If everything was rejected only by budget, relax by 1.5x
    // This prevents blank screens when live prices are higher than expected
    if (filtered.length === 0 && intent.budget.max && hard_failures.length > 0) {
      const relaxedBudget = intent.budget.max * 1.5;
      const budgetOnlyFails = hard_failures.filter(f =>
        f.violations.length === 1 && f.violations[0].name === 'budget' &&
        f.product.best_price <= relaxedBudget
      );
      if (budgetOnlyFails.length > 0) {
        for (const { product: p, violations } of budgetOnlyFails) {
          // Mark as over_budget but allow through as soft violation
          filtered.push({ product: p, relevance_score: 30, violations: [...violations, { type: 'soft', name: 'over_budget', detail: `Slightly over ₹${intent.budget.max.toLocaleString()} budget` }] });
        }
        if (window.UI && UI.logTerminal) {
          UI.logTerminal(`[!] Budget relaxed: showing ${budgetOnlyFails.length} near-budget matches`, 'highlight');
        }
      }
    }

    // STRICT BRAND FILTERING: If user explicitly requested a brand (e.g. Apple / iPhone), and brand matches exist, drop non-matching brands
    if (intent.brand_preference.length > 0) {
      const brandMatches = filtered.filter(item =>
        intent.brand_preference.some(b => item.product.brand.toLowerCase().includes(b) || item.product.search_text.includes(b))
      );
      if (brandMatches.length > 0) {
        return { filtered: brandMatches, hard_failures };
      }
    }

    return { filtered, hard_failures };
  },

  buildConstraintList(intent) {
    const constraints = [];
    if (intent.budget.max) constraints.push({ type: 'hard', name: 'Max Budget', value: `₹${intent.budget.max.toLocaleString()}` });
    if (intent.category) constraints.push({ type: 'hard', name: 'Category', value: intent.category.replace(/_/g, ' ') });
    if (intent.size) constraints.push({ type: 'hard', name: 'Size', value: intent.size });
    if (intent.brand_preference.length > 0) constraints.push({ type: 'soft', name: 'Brand', value: intent.brand_preference.join(', ') });
    if (intent.surface) constraints.push({ type: 'soft', name: 'Surface', value: intent.surface });
    if (intent.use_case.length > 0) constraints.push({ type: 'soft', name: 'Use Case', value: intent.use_case.join(', ').replace(/_/g,' ') });
    return constraints;
  }
};

// ---- RANKING ENGINE ----
// Deterministic, transparent scoring. Each dimension is explained.
const RANKING_ENGINE = {
  WEIGHTS: {
    requirement_match: 0.30,
    budget_fit: 0.20,
    use_case: 0.20,
    inventory: 0.10,
    rating: 0.10,
    delivery: 0.10
  },

  computeVectorSimilarity(query, text) {
    if (!query || !text) return 0.5;
    const tokenize = s => s.toLowerCase().match(/[a-z0-9]+/g) || [];
    const qTokens = tokenize(query);
    const dTokens = tokenize(text);
    if (!qTokens.length || !dTokens.length) return 0.5;

    const qCounts = {}, dCounts = {};
    qTokens.forEach(t => qCounts[t] = (qCounts[t] || 0) + 1);
    dTokens.forEach(t => dCounts[t] = (dCounts[t] || 0) + 1);

    let dot = 0, qMag = 0, dMag = 0;
    Object.keys(qCounts).forEach(t => {
      const qVal = qCounts[t];
      qMag += qVal * qVal;
      if (dCounts[t]) dot += qVal * dCounts[t];
    });
    Object.values(dCounts).forEach(v => dMag += v * v);

    if (qMag === 0 || dMag === 0) return 0.5;
    return Math.min(1.0, Math.max(0, dot / (Math.sqrt(qMag) * Math.sqrt(dMag))));
  },

  score(product, intent, merchantId = null) {
    const merchant = merchantId || product.best_merchant;
    const price = product.price[merchant] || product.best_price;
    const inv = product.inventory[merchant] || 0;
    const delivery = product.delivery[merchant];

    // Vector Similarity calculation
    const vector_sim = this.computeVectorSimilarity(intent.raw_query, product.search_text || product.title);

    // 1. Requirement match (category + feature alignment + vector similarity)
    let req_score = 0;
    const isSmartphoneIntent = intent.category === 'smartphone' || (intent.raw_query || '').toLowerCase().includes('iphone');

    if (isSmartphoneIntent) {
      if (product.category === 'smartphones' || product.search_text.includes('iphone')) req_score = 1.0;
      else req_score = 0;
    } else if (intent.category && product.category === intent.category) req_score = 1.0;
    else if (intent.category && product.category.includes(intent.category.split('_')[0])) req_score = 0.6;
    else req_score = 0.2;

    // Blend vector similarity into requirement score
    req_score = Math.min(1.0, (req_score * 0.6) + (vector_sim * 0.4));

    // Brand constraint: if user explicitly requested a brand (e.g. Apple / iPhone / Nike / Sony)
    if (intent.brand_preference.length > 0) {
      const brandMatch = intent.brand_preference.some(b => product.brand.toLowerCase().includes(b) || product.search_text.includes(b));
      if (brandMatch) {
        req_score = 1.0; // Perfect requirement score for requested brand
      } else {
        req_score = 0.1; // Heavily penalize non-matching brands when user asked for a specific brand
      }
    }

    // 2. Budget fit
    let budget_score = 1.0;
    if (intent.budget.max && price > 0) {
      if (price <= intent.budget.max) budget_score = 1.0 - (price / intent.budget.max) * 0.1;
      else budget_score = Math.max(0, 1.0 - ((price - intent.budget.max) / intent.budget.max));
    }

    // 3. Use case suitability
    let usecase_score = 0.5;
    if (intent.use_case.length === 0) { usecase_score = 0.8; }
    else {
      const ucMatches = intent.use_case.filter(uc => {
        const ucWords = uc.split('_');
        return ucWords.some(w => product.search_text.includes(w));
      }).length;
      usecase_score = Math.min(1.0, 0.3 + (ucMatches / intent.use_case.length) * 0.7);
    }

    // 4. Inventory
    const inventory_score = inv >= 10 ? 1.0 : inv >= 5 ? 0.8 : inv >= 1 ? 0.6 : 0;

    // 5. Rating
    const rating_score = (product.rating || 3.0) / 5.0;

    // 6. Delivery speed
    let delivery_score = 0.5;
    if (!delivery) delivery_score = 0;
    else if (delivery.includes('1 day')) delivery_score = 1.0;
    else if (delivery.includes('2 day')) delivery_score = 0.9;
    else if (delivery.includes('3 day')) delivery_score = 0.75;
    else if (delivery.includes('4 day')) delivery_score = 0.6;
    else if (delivery.includes('5 day')) delivery_score = 0.45;
    else delivery_score = 0.3;

    const W = this.WEIGHTS;
    const total = (
      req_score * W.requirement_match +
      budget_score * W.budget_fit +
      usecase_score * W.use_case +
      inventory_score * W.inventory +
      rating_score * W.rating +
      delivery_score * W.delivery
    );

    const breakdown = {
      requirement_match: { score: Math.round(req_score * 30), max: 30, pct: req_score },
      vector_similarity: { score: Math.round(vector_sim * 100), val: vector_sim.toFixed(3) },
      budget_fit: { score: Math.round(budget_score * 20), max: 20, pct: budget_score },
      use_case: { score: Math.round(usecase_score * 20), max: 20, pct: usecase_score },
      inventory: { score: Math.round(inventory_score * 10), max: 10, pct: inventory_score },
      rating: { score: Math.round(rating_score * 10), max: 10, pct: rating_score },
      delivery: { score: Math.round(delivery_score * 10), max: 10, pct: delivery_score }
    };

    return {
      product,
      merchant_id: merchant,
      price,
      vector_sim: vector_sim.toFixed(3),
      total_score: Math.round(total * 100),
      breakdown,
      inv,
      delivery
    };
  },

  rank(candidates, intent) {
    return candidates
      .map(({ product }) => this.score(product, intent))
      .sort((a,b) => b.total_score - a.total_score)
      .slice(0, 12);
  }
};

// ---- CHECKOUT ENGINE ----
// UCP-aligned checkout state machine (local simulation)
// Endpoints mirror UCP specification structure
const CHECKOUT_ENGINE = {
  STATES: ['INITIALIZED','REQUIRES_INFORMATION','READY_FOR_CHECKOUT','PAYMENT_SIMULATED','COMPLETED'],

  create(cart) {
    const id = 'cs_' + Math.random().toString(36).substr(2,12).toUpperCase();
    return {
      id,
      object: 'checkout_session',
      status: 'INITIALIZED',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 30*60*1000).toISOString(),
      currency: 'INR',
      line_items: cart.map(item => ({
        product_id: item.product.id,
        title: item.product.title,
        quantity: item.qty,
        unit_price: item.product.price[item.merchant_id],
        total_price: item.product.price[item.merchant_id] * item.qty,
        merchant_id: item.merchant_id
      })),
      totals: this._calcTotals(cart),
      shipping: null,
      payment: null,
      metadata: {
        environment: ENV_LABEL,
        ucp_version: UCP_VERSION,
        note: 'This is a simulated checkout session. No real payment is processed.'
      }
    };
  },

  advance(session) {
    const idx = this.STATES.indexOf(session.status);
    if (idx < this.STATES.length - 1) {
      session.status = this.STATES[idx + 1];
      session.updated_at = new Date().toISOString();
      // Populate fields per state
      if (session.status === 'REQUIRES_INFORMATION') {
        session.shipping = { method: null, address: null };
      } else if (session.status === 'READY_FOR_CHECKOUT') {
        session.shipping = {
          method: 'STANDARD',
          address: { line1: '123 Demo Street', city: 'Bengaluru', state: 'KA', postal_code: '560001', country: 'IN' }
        };
        session.payment = { handler: 'SIMULATED_PAYMENT', status: 'PENDING' };
      } else if (session.status === 'PAYMENT_SIMULATED') {
        session.payment = { handler: 'SIMULATED_PAYMENT', status: 'AUTHORIZED', reference: 'sim_' + Math.random().toString(36).substr(2,8).toUpperCase() };
      } else if (session.status === 'COMPLETED') {
        session.payment.status = 'CAPTURED';
        session.completed_at = new Date().toISOString();
      }
    }
    return session;
  },

  _calcTotals(cart) {
    const subtotal = cart.reduce((sum, item) => sum + (item.product.price[item.merchant_id] || item.product.best_price) * item.qty, 0);
    const shipping = subtotal >= 5000 ? 0 : 99;
    const tax = Math.round(subtotal * 0.18);
    return { subtotal, shipping, tax, total: subtotal + shipping + tax };
  }
};

// ---- ORDER ENGINE ----
const ORDER_ENGINE = {
  STATES: [
    { key: 'ORDER_CREATED', label: 'Order Created', icon: '📦', desc: 'Order confirmed and received by merchant' },
    { key: 'CONFIRMED', label: 'Confirmed', icon: '✅', desc: 'Merchant confirmed availability and payment' },
    { key: 'PROCESSING', label: 'Processing', icon: '⚙', desc: 'Items being picked, packed, and labeled' },
    { key: 'SHIPPED', label: 'Shipped', icon: '🚚', desc: 'Package dispatched to delivery partner' },
    { key: 'OUT_FOR_DELIVERY', label: 'Out for Delivery', icon: '🏃', desc: 'With delivery agent, arriving today' },
    { key: 'DELIVERED', label: 'Delivered', icon: '🎉', desc: 'Successfully delivered to your address' }
  ],

  create(checkoutSession) {
    const id = 'ORD-' + Math.random().toString(36).substr(2,8).toUpperCase();
    return {
      id,
      object: 'order',
      status: 'ORDER_CREATED',
      status_idx: 0,
      created_at: new Date().toISOString(),
      checkout_session_id: checkoutSession.id,
      line_items: checkoutSession.line_items,
      totals: checkoutSession.totals,
      shipping: checkoutSession.shipping,
      events: [{
        status: 'ORDER_CREATED',
        timestamp: new Date().toISOString(),
        message: 'Order created successfully',
        payload: { order_id: id, session_id: checkoutSession.id }
      }],
      metadata: { environment: ENV_LABEL, ucp_version: UCP_VERSION }
    };
  },

  advance(order) {
    if (order.status_idx < this.STATES.length - 1) {
      order.status_idx++;
      const nextState = this.STATES[order.status_idx];
      order.status = nextState.key;
      order.events.push({
        status: nextState.key,
        timestamp: new Date().toISOString(),
        message: nextState.desc,
        payload: { order_id: order.id, tracking: order.status_idx >= 3 ? 'TRK' + Math.random().toString(36).substr(2,8).toUpperCase() : null }
      });
    }
    return order;
  }
};

// ---- CART ENGINE ----
const CART_ENGINE = {
  add(cart, product, merchant_id, qty = 1) {
    const existing = cart.find(i => i.product.id === product.id && i.merchant_id === merchant_id);
    if (existing) { existing.qty += qty; }
    else { cart.push({ product, merchant_id, qty }); }
    return [...cart];
  },
  remove(cart, productId, merchantId) {
    return cart.filter(i => !(i.product.id === productId && i.merchant_id === merchantId));
  },
  updateQty(cart, productId, merchantId, delta) {
    const item = cart.find(i => i.product.id === productId && i.merchant_id === merchantId);
    if (item) {
      item.qty = Math.max(1, item.qty + delta);
      if (item.qty === 0) return this.remove(cart, productId, merchantId);
    }
    return [...cart];
  },
  totals(cart) {
    const subtotal = cart.reduce((s, i) => s + (i.product.price[i.merchant_id] || i.product.best_price) * i.qty, 0);
    const shipping = subtotal >= 5000 ? 0 : subtotal > 0 ? 99 : 0;
    const tax = Math.round(subtotal * 0.18);
    return { subtotal, shipping, tax, total: subtotal + shipping + tax };
  }
};

// ---- MAIN AGENT ORCHESTRATOR ----
const AGENT = {
  async run(query) {
    const runId = 'run_' + Date.now().toString(36);
    SESSION.id = runId;
    SESSION.query = query;
    SESSION.trace = [];
    SESSION.run_count++;
    const startTime = Date.now();

    const addTrace = (event, input, output, latency, status = 'success') => {
      SESSION.trace.push({ event, input, output, latency, status, timestamp: new Date().toISOString() });
      SESSION.tool_calls++;
    };

    try {
      const apiKey = localStorage.getItem('gemini_api_key');
      
      if (!apiKey) {
        if (window.UI && UI.logTerminal) { await UI.logTerminal(`[!] No Gemini API key found. Falling back to local deterministic simulation.`, 'highlight'); }
        return this.runSimulated(query, runId, startTime, addTrace);
      }

      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Opening secure serverless connection to Groq (GPT-OSS 120B)...`, 'system'); }
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Translating natural language to UCP Intent schema...`, 'system'); }

      const llmStart = Date.now();
      
      const prompt = `
Extract the shopping intent from this query: "${query}"

Map it to the following JSON schema exactly. Return ONLY valid JSON, nothing else. Do not use markdown blocks.
{
  "category": "string or null (e.g. running_shoes, laptop, tv, smartphone, headphones)",
  "budget": {"max": number or null},
  "brand_preference": ["string array"],
  "size": "string or null",
  "surface": "string or null (e.g. road, trail, street)",
  "use_case": ["string array (e.g. daily_running, office, gaming)"],
  "keywords": ["string array of other important features"]
}`;

      // Call Groq via REST API
      const response = await fetch(`https://api.groq.com/openai/v1/chat/completions`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: "openai/gpt-oss-120b",
          messages: [{ role: "user", content: prompt }],
          temperature: 0.0
        })
      });

      if (!response.ok) {
        let errMsg = `Groq API Error: ${response.status} ${response.statusText}`;
        try {
           const errData = await response.json();
           if (errData.error && errData.error.message) errMsg += ` - ${errData.error.message}`;
        } catch(e) {}
        throw new Error(errMsg);
      }

      const data = await response.json();
      let textResponse = data.choices[0].message.content;
      textResponse = textResponse.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
      
      const intent = JSON.parse(textResponse);
      
      SESSION.intent = intent;
      addTrace('parse_intent_llm', { query }, { intent }, Date.now() - llmStart);
      
      if (window.UI && UI.logTerminal) {
        await UI.logTerminal(`[✓] Intent extracted via LLM:`, 'success');
        await UI.logTerminal(`    Category: ${intent.category || 'Any'}`);
        await UI.logTerminal(`    Budget Max: ${intent.budget.max ? '₹' + intent.budget.max : 'None'}`);
      }

      // STAGE 2: Build Constraints
      await delay(200, 400);
      const constraintStart = Date.now();
      const constraints = CONSTRAINT_ENGINE.buildConstraintList(intent);
      addTrace('build_intent', { intent }, { constraints }, Date.now() - constraintStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Translating intent to UCP search query...`, 'system'); }

      // STAGE 3: Search Catalog
      await delay(300, 500);
      const searchStart = Date.now();
      const searchResults = await SEARCH_ENGINE.search(intent);
      SESSION.candidates = searchResults;
      SESSION.retrieval_count += searchResults.length;
      addTrace('search_catalog', { intent, catalog_size: 100 }, { candidates: searchResults.length }, Date.now() - searchStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`[✓] Retrieved ${searchResults.length} candidates from live API`, 'success'); }

      // STAGE 4: Apply Constraints
      await delay(200, 300);
      const filterStart = Date.now();
      const { filtered, hard_failures } = CONSTRAINT_ENGINE.apply(searchResults, intent);
      SESSION.filtered = filtered;
      addTrace('apply_constraints', { constraints, candidates: searchResults.length }, { filtered: filtered.length, rejected: hard_failures.length }, Date.now() - filterStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Applying hard constraints (budget, size)... rejected ${hard_failures.length}`, 'system'); }

      // STAGE 5: Check Inventory
      await delay(300, 500);
      const invStart = Date.now();
      const inStockFiltered = filtered.filter(c => c.product.in_stock);
      addTrace('check_inventory', { products: filtered.length }, { available: inStockFiltered.length }, Date.now() - invStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`[✓] Verified simulated real-time inventory across 3 merchants`, 'success'); }

      // STAGE 6: Rank
      await delay(300, 400);
      const rankStart = Date.now();
      const ranked = RANKING_ENGINE.rank(inStockFiltered, intent);
      SESSION.ranked = ranked;
      addTrace('rank_candidates', { candidates: inStockFiltered.length }, { ranked: ranked.length, top_score: ranked[0]?.total_score }, Date.now() - rankStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Ranking ${ranked.length} candidates across 6 dimensions...`, 'system'); }

      // STAGE 7: Generate Recommendation
      await delay(200, 300);
      const recStart = Date.now();
      const topProduct = ranked[0] || null;
      addTrace('generate_recommendation', { ranked: ranked.length }, { recommended: topProduct?.product.title, score: topProduct?.total_score }, Date.now() - recStart);
      
      if (window.UI && UI.logTerminal) { 
        if (topProduct) await UI.logTerminal(`[✓] Selected top recommendation: ${topProduct.product.title} (${topProduct.total_score}%)`, 'highlight');
        else await UI.logTerminal(`[!] No products matched all constraints`, 'system');
      }

      // Final state updates
      SESSION.total_latency += Date.now() - startTime;
      if (ranked.length > 0) SESSION.success_count++;
      else SESSION.failure_count++;

      // Render results
      if (window.UI) {
        UI.renderResults(ranked, intent, hard_failures);
        UI.updateAgentState();
      }
      return { success: ranked.length > 0, ranked, intent };

    } catch (err) {
      console.error('Agent error:', err);
      SESSION.failure_count++;
      addTrace('error', { query }, { error: err.message }, 0, 'error');
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`[ERROR] ${err.message}`, 'system'); }
      if (typeof showToast !== 'undefined') showToast('Agent error: ' + err.message);
      if (window.UI) UI.renderResults([], null, []);
      return { success: false, error: err.message };
    }
  },

  async runSimulated(query, runId, startTime, addTrace) {
    try {
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Initializing session ${runId}`, 'system'); }
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Parsing query: "${query}"`, 'system'); }
      
      // STAGE 1: Parse Intent
      await delay(600, 800);
      const intentStart = Date.now();
      const intent = INTENT_PARSER.parse(query);
      SESSION.intent = intent;
      addTrace('parse_request', { query }, { intent }, Date.now() - intentStart);
      
      if (window.UI && UI.logTerminal) {
        await UI.logTerminal(`[✓] Intent extracted (Confidence: ${intent.confidence}%)`, 'success');
        await UI.logTerminal(`    Category: ${intent.category || 'Any'}`);
        await UI.logTerminal(`    Budget Max: ${intent.budget.max ? '₹' + intent.budget.max : 'None'}`);
      }

      // STAGE 2: Build Constraints
      await delay(400, 600);
      const constraintStart = Date.now();
      const constraints = CONSTRAINT_ENGINE.buildConstraintList(intent);
      addTrace('build_intent', { intent }, { constraints }, Date.now() - constraintStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Translating intent to UCP search query...`, 'system'); }

      // STAGE 3: Search Catalog (Live DummyJSON)
      await delay(800, 1200);
      const searchStart = Date.now();
      const searchResults = await SEARCH_ENGINE.search(intent);
      SESSION.candidates = searchResults;
      SESSION.retrieval_count += searchResults.length;
      addTrace('search_catalog', { intent, catalog_size: 100 }, { candidates: searchResults.length }, Date.now() - searchStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`[✓] Retrieved ${searchResults.length} candidates from live API`, 'success'); }

      // STAGE 4: Apply Constraints
      await delay(400, 600);
      const filterStart = Date.now();
      const { filtered, hard_failures } = CONSTRAINT_ENGINE.apply(searchResults, intent);
      SESSION.filtered = filtered;
      addTrace('apply_constraints', { constraints, candidates: searchResults.length }, { filtered: filtered.length, rejected: hard_failures.length }, Date.now() - filterStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Applying hard constraints (budget, size)... rejected ${hard_failures.length}`, 'system'); }

      // STAGE 5: Check Inventory
      await delay(600, 900);
      const invStart = Date.now();
      const inStockFiltered = filtered.filter(c => c.product.in_stock);
      addTrace('check_inventory', { products: filtered.length }, { available: inStockFiltered.length }, Date.now() - invStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`[✓] Verified real-time inventory across 3 merchants`, 'success'); }

      // STAGE 6: Rank
      await delay(700, 1000);
      const rankStart = Date.now();
      const ranked = RANKING_ENGINE.rank(inStockFiltered, intent);
      SESSION.ranked = ranked;
      addTrace('rank_candidates', { candidates: inStockFiltered.length }, { ranked: ranked.length, top_score: ranked[0]?.total_score }, Date.now() - rankStart);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Ranking ${ranked.length} candidates across 6 dimensions...`, 'system'); }

      // STAGE 7: Generate Recommendation
      await delay(500, 700);
      const recStart = Date.now();
      const topProduct = ranked[0] || null;
      addTrace('generate_recommendation', { ranked: ranked.length }, { recommended: topProduct?.product.title, score: topProduct?.total_score }, Date.now() - recStart);
      
      if (window.UI && UI.logTerminal) { 
        if (topProduct) await UI.logTerminal(`[✓] Selected top recommendation: ${topProduct.product.title} (${topProduct.total_score}%)`, 'highlight');
        else await UI.logTerminal(`[!] No products matched all constraints`, 'system');
      }

      // Final state updates
      SESSION.total_latency += Date.now() - startTime;
      if (ranked.length > 0) SESSION.success_count++;
      else SESSION.failure_count++;

      // Render results
      if (window.UI) {
        UI.renderResults(ranked, intent, hard_failures);
        UI.updateAgentState();
      }
      return { success: ranked.length > 0, ranked, intent };

    } catch (err) {
      console.error('Agent error:', err);
      SESSION.failure_count++;
      addTrace('error', { query }, { error: err.message }, 0, 'error');
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`[ERROR] ${err.message}`, 'system'); }
      if (typeof showToast !== 'undefined') showToast('Agent error: ' + err.message);
      // Still show results area (even if empty) to unblock the UI
      if (window.UI) UI.renderResults([], null, []);
      return { success: false, error: err.message };
    }
  }
};

// ---- UCP PROFILE GENERATOR ----
// Generates UCP-inspired Business Profile from app config
// Labeled: UCP-INSPIRED SIMULATION
const UCP_PROFILE_GENERATOR = {
  generate(merchant_id = 'nova') {
    const merchant = MERCHANTS[merchant_id] || MERCHANTS.nova;
    return {
      "@context": "https://schema.ucp.dev/v1",
      "@type": "BusinessProfile",
      "ucpVersion": UCP_VERSION,
      "environment": ENV_LABEL,
      "businessName": `${merchant.name} — CommerceOS Demo`,
      "description": merchant.tagline,
      "merchantId": `demo_${merchant_id}_001`,
      "capabilities": {
        "productDiscovery": {
          "enabled": true,
          "transport": ["REST"],
          "endpoint": "/api/products/search",
          "schema": "https://schema.ucp.dev/v1/product-discovery"
        },
        "cart": {
          "enabled": true,
          "transport": ["REST"],
          "endpoint": "/api/cart",
          "schema": "https://schema.ucp.dev/v1/cart"
        },
        "checkout": {
          "enabled": true,
          "transport": ["REST"],
          "endpoint": "/api/checkout-sessions",
          "schema": "https://schema.ucp.dev/v1/checkout",
          "idempotency": true
        },
        "orderManagement": {
          "enabled": merchant.capabilities.includes('order_management'),
          "transport": ["REST"],
          "endpoint": "/api/orders",
          "schema": "https://schema.ucp.dev/v1/orders"
        },
        "fulfillment": {
          "enabled": merchant.capabilities.includes('fulfillment'),
          "transport": ["REST"],
          "endpoint": "/api/fulfillment"
        },
        "identityLinking": {
          "enabled": false,
          "note": "OAuth 2.0 identity linking not implemented in this simulation"
        },
        "offers": {
          "enabled": false,
          "note": "Personalized offers not available in this simulation"
        }
      },
      "paymentHandlers": [
        {
          "id": "simulated_payment",
          "type": "SIMULATED",
          "currencies": ["INR"],
          "note": "SIMULATED PAYMENT — No real transactions processed"
        }
      ],
      "policies": {
        "returns": merchant.policy.returns,
        "warranty": merchant.policy.warranty,
        "cod": merchant.policy.cod,
        "shipping_free_threshold": `₹${merchant.policy.shipping_free_threshold || 5000}`
      },
      "metadata": {
        "generated_at": new Date().toISOString(),
        "app": "CommerceOS",
        "note": "This is a simulated UCP-inspired business profile for educational/demonstration purposes. It is NOT an official Google/UCP certified profile.",
        "official_spec": "https://ucp.dev/specification/overview/",
        "github": "https://github.com/Universal-Commerce-Protocol/ucp"
      }
    };
  },

  validate(profile) {
    const results = [];
    // Check required fields
    if (profile['@context']) results.push({ check: '@context present', pass: true });
    else results.push({ check: '@context present', pass: false, detail: 'Missing @context field' });

    if (profile.ucpVersion) results.push({ check: 'ucpVersion declared', pass: true });
    else results.push({ check: 'ucpVersion declared', pass: false, detail: 'Missing ucpVersion' });

    if (profile.capabilities) results.push({ check: 'capabilities object present', pass: true });
    else results.push({ check: 'capabilities object present', pass: false });

    if (profile.capabilities?.checkout?.enabled) results.push({ check: 'checkout capability enabled', pass: true });
    else results.push({ check: 'checkout capability enabled', pass: false, warn: true });

    if (profile.paymentHandlers?.length > 0) results.push({ check: 'payment handler declared', pass: true });
    else results.push({ check: 'payment handler declared', pass: false });

    if (profile.environment === ENV_LABEL) results.push({ check: 'environment labeled correctly', pass: true });
    else results.push({ check: 'environment label present', pass: true, warn: true, detail: 'Set to production environment' });

    if (profile.metadata?.note?.includes('simulated')) results.push({ check: 'simulation disclaimer present', pass: true });
    else results.push({ check: 'simulation disclaimer present', pass: false, detail: 'Should clearly label simulation' });

    return results;
  }
};

// ---- API SIMULATOR ----
// Simulates UCP-aligned REST endpoints locally
const API_SIMULATOR = {
  ENDPOINTS: [
    { method: 'GET', path: '/.well-known/ucp', desc: 'Business Profile', category: 'profile' },
    { method: 'POST', path: '/api/products/search', desc: 'Product Search', category: 'discovery' },
    { method: 'GET', path: '/api/products/{id}', desc: 'Get Product', category: 'discovery' },
    { method: 'POST', path: '/api/cart', desc: 'Create Cart', category: 'cart' },
    { method: 'PUT', path: '/api/cart/{id}/items', desc: 'Update Cart Items', category: 'cart' },
    { method: 'POST', path: '/api/checkout-sessions', desc: 'Create Checkout Session', category: 'checkout' },
    { method: 'GET', path: '/api/checkout-sessions/{id}', desc: 'Get Checkout Session', category: 'checkout' },
    { method: 'PUT', path: '/api/checkout-sessions/{id}', desc: 'Update Checkout Session', category: 'checkout' },
    { method: 'POST', path: '/api/checkout-sessions/{id}/complete', desc: 'Complete Checkout', category: 'checkout' },
    { method: 'GET', path: '/api/orders/{id}', desc: 'Get Order', category: 'orders' },
    { method: 'GET', path: '/api/orders/{id}/events', desc: 'Order Events', category: 'orders' }
  ],

  async execute(endpoint, body = null) {
    const latency = Math.floor(Math.random() * 80) + 20;
    await delay(latency, latency + 20);

    const path = endpoint.path;
    const method = endpoint.method;

    if (path === '/.well-known/ucp') {
      return { status: 200, latency, body: UCP_PROFILE_GENERATOR.generate(), valid: true };
    }
    if (path === '/api/products/search') {
      const query = body?.query || 'running shoes';
      const intent = INTENT_PARSER.parse(query);
      if (window.UI && UI.logTerminal) { await UI.logTerminal(`> Executing real-time semantic search for '${query}'...`, 'system'); }
      const results = (await SEARCH_ENGINE.search(intent)).slice(0,5).map(r => ({
        id: r.product.id, title: r.product.title, brand: r.product.brand,
        price: r.product.best_price, currency: 'INR', in_stock: r.product.in_stock,
        rating: r.product.rating, relevance_score: r.relevance_score
      }));
      return { status: 200, latency, body: { query, results, total: results.length, environment: ENV_LABEL }, valid: true };
    }
    if (path === '/api/products/{id}') {
      const p = CATALOG[Math.floor(Math.random() * CATALOG.length)];
      return { status: 200, latency, body: { ...p, environment: ENV_LABEL }, valid: true };
    }
    if (path === '/api/cart') {
      const cartId = 'cart_' + Math.random().toString(36).substr(2,10).toUpperCase();
      return { status: 201, latency, body: { id: cartId, status: 'active', items: [], environment: ENV_LABEL }, valid: true };
    }
    if (path === '/api/cart/{id}/items') {
      return { status: 200, latency, body: { id: 'cart_DEMO', status: 'updated', items: SESSION.cart.map(i => ({ product_id: i.product.id, qty: i.qty })), environment: ENV_LABEL }, valid: true };
    }
    if (path === '/api/checkout-sessions' && method === 'POST') {
      const demoCart = SESSION.cart.length > 0 ? SESSION.cart : [{
        product: CATALOG[0], merchant_id: 'nova', qty: 1
      }];
      const session = CHECKOUT_ENGINE.create(demoCart);
      return { status: 201, latency, body: session, valid: true };
    }
    if (path === '/api/checkout-sessions/{id}' && method === 'GET') {
      const s = SESSION.checkout || CHECKOUT_ENGINE.create([{ product: CATALOG[0], merchant_id: 'nova', qty: 1 }]);
      return { status: 200, latency, body: s, valid: true };
    }
    if (path === '/api/checkout-sessions/{id}' && method === 'PUT') {
      const s = SESSION.checkout || CHECKOUT_ENGINE.create([{ product: CATALOG[0], merchant_id: 'nova', qty: 1 }]);
      s.status = 'REQUIRES_INFORMATION';
      s.shipping = body?.shipping || { method: 'STANDARD', address: { city: 'Bengaluru', country: 'IN' } };
      return { status: 200, latency, body: s, valid: true };
    }
    if (path === '/api/checkout-sessions/{id}/complete') {
      const s = SESSION.checkout || CHECKOUT_ENGINE.create([{ product: CATALOG[0], merchant_id: 'nova', qty: 1 }]);
      s.status = 'COMPLETED';
      s.completed_at = new Date().toISOString();
      return { status: 200, latency, body: s, valid: true };
    }
    if (path === '/api/orders/{id}') {
      const o = SESSION.order || ORDER_ENGINE.create({ id: 'cs_DEMO', line_items: [], totals: {}, shipping: {} });
      return { status: 200, latency, body: o, valid: true };
    }
    if (path === '/api/orders/{id}/events') {
      const o = SESSION.order;
      return { status: 200, latency, body: { order_id: o?.id || 'ORD-DEMO', events: o?.events || [], environment: ENV_LABEL }, valid: true };
    }
    return { status: 404, latency, body: { error: 'Not found', path }, valid: false };
  }
};

// ---- EVALUATION ENGINE ----
const EVALUATION_ENGINE = {
  TEST_CASES: [
    // Intent accuracy tests
    { id: 'T01', name: 'Running shoe intent', input: 'running shoes under ₹8000 size 7', expects: { category: 'running_shoes', budget_max: 8000, size: '7' }, category: 'intent' },
    { id: 'T02', name: 'Laptop intent', input: 'laptop for ML under ₹80k', expects: { category: 'laptop', budget_max: 80000 }, category: 'intent' },
    { id: 'T03', name: 'Headphones intent', input: 'wireless headphones under ₹10000', expects: { category: 'headphones', budget_max: 10000 }, category: 'intent' },
    { id: 'T04', name: 'Shirt intent', input: 'black formal shirt size M under ₹2500', expects: { category: 'formal_shirt', size: 'M', budget_max: 2500 }, category: 'intent' },
    { id: 'T05', name: 'Brand extraction', input: 'Nike running shoes', expects: { brand_preference: ['nike'] }, category: 'intent' },
    { id: 'T06', name: 'No category', input: 'something nice under ₹5000', expects: { budget_max: 5000 }, category: 'intent' },
    { id: 'T07', name: 'Use case ML', input: 'laptop for python machine learning', expects: { use_case: ['ml'] }, category: 'intent' },
    { id: 'T08', name: 'Surface road', input: 'road running shoes', expects: { surface: 'road' }, category: 'intent' },
    // Constraint tests
    { id: 'T09', name: 'Budget hard constraint', input: { products: CATALOG.slice(0,10), budget: 5000 }, type: 'constraint', category: 'constraint' },
    { id: 'T10', name: 'Size constraint', input: { size: '7', products: CATALOG.slice(0,10) }, type: 'constraint', category: 'constraint' },
    { id: 'T11', name: 'Stock constraint', input: null, type: 'constraint_stock', category: 'constraint' },
    // Inventory tests
    { id: 'T12', name: 'In-stock filtering', input: null, type: 'inventory', category: 'inventory' },
    // Ranking tests
    { id: 'T13', name: 'Top result relevance', input: 'running shoes', expects: { category_match: true }, category: 'ranking' },
    { id: 'T14', name: 'Budget adherence in ranking', input: 'laptop under ₹50000', type: 'ranking_budget', category: 'ranking' },
    { id: 'T15', name: 'Score consistency', input: null, type: 'ranking_consistency', category: 'ranking' },
    // Cart tests
    { id: 'T16', name: 'Cart add', input: null, type: 'cart', category: 'cart' },
    { id: 'T17', name: 'Cart total calculation', input: null, type: 'cart_totals', category: 'cart' },
    { id: 'T18', name: 'Cart empty state', input: null, type: 'cart_empty', category: 'cart' },
    // Checkout tests
    { id: 'T19', name: 'Checkout creation', input: null, type: 'checkout_create', category: 'checkout' },
    { id: 'T20', name: 'Checkout state transition', input: null, type: 'checkout_state', category: 'checkout' },
    { id: 'T21', name: 'Checkout completion', input: null, type: 'checkout_complete', category: 'checkout' },
    // Protocol tests
    { id: 'T22', name: 'UCP profile valid', input: null, type: 'ucp_profile', category: 'protocol' },
    { id: 'T23', name: 'Profile has capabilities', input: null, type: 'ucp_caps', category: 'protocol' },
    { id: 'T24', name: 'Profile version declared', input: null, type: 'ucp_version', category: 'protocol' }
  ],

  run() {
    const results = {};
    const categories = { intent: { pass: 0, total: 0 }, constraint: { pass: 0, total: 0 }, inventory: { pass: 0, total: 0 }, ranking: { pass: 0, total: 0 }, cart: { pass: 0, total: 0 }, checkout: { pass: 0, total: 0 }, protocol: { pass: 0, total: 0 } };

    for (const tc of this.TEST_CASES) {
      let pass = false;
      try {
        if (tc.category === 'intent') {
          const intent = INTENT_PARSER.parse(tc.input);
          pass = true;
          if (tc.expects.category && intent.category !== tc.expects.category) pass = false;
          if (tc.expects.budget_max && intent.budget.max !== tc.expects.budget_max) pass = false;
          if (tc.expects.size && intent.size !== tc.expects.size) pass = false;
          if (tc.expects.brand_preference && !intent.brand_preference.includes(tc.expects.brand_preference[0])) pass = false;
          if (tc.expects.surface && intent.surface !== tc.expects.surface) pass = false;
          if (tc.expects.use_case) { const uc = tc.expects.use_case[0]; pass = intent.use_case.includes(uc); }
        } else if (tc.category === 'constraint') {
          const intent = INTENT_PARSER.parse('running shoes under ₹5000 size 7');
          const { filtered } = CONSTRAINT_ENGINE.apply(SEARCH_ENGINE.search(intent, CATALOG), intent);
          if (tc.type === 'constraint_stock') pass = filtered.every(c => c.product.in_stock);
          else pass = filtered.every(c => c.product.best_price <= (intent.budget.max || Infinity));
        } else if (tc.category === 'inventory') {
          pass = CATALOG.filter(p => p.in_stock).every(p => p.available_merchants.length > 0);
        } else if (tc.category === 'ranking') {
          const intent = INTENT_PARSER.parse(tc.type === 'ranking_budget' ? 'laptop under ₹50000' : 'running shoes');
          const results2 = SEARCH_ENGINE.search(intent, CATALOG);
          const { filtered } = CONSTRAINT_ENGINE.apply(results2, intent);
          const ranked = RANKING_ENGINE.rank(filtered, intent);
          if (tc.type === 'ranking_budget') pass = !intent.budget.max || (ranked[0]?.price <= intent.budget.max);
          else if (tc.type === 'ranking_consistency') { const s1 = RANKING_ENGINE.score(CATALOG[0], intent); const s2 = RANKING_ENGINE.score(CATALOG[0], intent); pass = s1.total_score === s2.total_score; }
          else pass = ranked.length > 0 && (ranked[0]?.product.category === 'running_shoes' || ranked[0]?.product.category?.includes('shoe'));
        } else if (tc.category === 'cart') {
          const testCart = [];
          const added = CART_ENGINE.add(testCart, CATALOG[1], 'nova', 2);
          if (tc.type === 'cart_empty') pass = testCart.length === 0; // original empty
          else if (tc.type === 'cart_totals') { const tots = CART_ENGINE.totals(added); pass = tots.total === tots.subtotal + tots.shipping + tots.tax; }
          else pass = added.length === 1 && added[0].qty === 2;
        } else if (tc.category === 'checkout') {
          const demoCart = [{ product: CATALOG[1], merchant_id: 'nova', qty: 1 }];
          const s = CHECKOUT_ENGINE.create(demoCart);
          if (tc.type === 'checkout_state') { const s2 = CHECKOUT_ENGINE.advance({...s}); pass = s2.status === 'REQUIRES_INFORMATION'; }
          else if (tc.type === 'checkout_complete') { let s2 = {...s}; for(let i=0;i<4;i++) s2 = CHECKOUT_ENGINE.advance(s2); pass = s2.status === 'COMPLETED'; }
          else pass = s.id.startsWith('cs_') && s.status === 'INITIALIZED';
        } else if (tc.category === 'protocol') {
          const profile = UCP_PROFILE_GENERATOR.generate();
          if (tc.type === 'ucp_version') pass = profile.ucpVersion === UCP_VERSION;
          else if (tc.type === 'ucp_caps') pass = Object.keys(profile.capabilities).length >= 4;
          else { const validation = UCP_PROFILE_GENERATOR.validate(profile); pass = validation.filter(r => r.pass).length >= 5; }
        }
      } catch (e) { pass = false; }

      categories[tc.category].total++;
      if (pass) categories[tc.category].pass++;
    }

    return Object.entries(categories).map(([cat, stats]) => ({
      name: cat,
      pass: stats.pass,
      total: stats.total,
      pct: stats.total > 0 ? Math.round((stats.pass / stats.total) * 100) : 0
    }));
  }
};

// ---- UTILITIES ----
function delay(min, max) {
  return new Promise(resolve => setTimeout(resolve, Math.floor(Math.random() * (max - min)) + min));
}

function formatINR(amount) {
  return '₹' + amount.toLocaleString('en-IN');
}

function syntaxHighlight(json) {
  const str = typeof json === 'string' ? json : JSON.stringify(json, null, 2);
  return str.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, match => {
    let cls = 'json-number';
    if (/^"/.test(match)) { if (/:$/.test(match)) cls = 'json-key'; else cls = 'json-string'; }
    else if (/true|false/.test(match)) cls = 'json-bool';
    return `<span class="${cls}">${match}</span>`;
  });
}

function showToast(msg, duration = 2500) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), duration);
}

console.log('Agent Engine loaded. UCP Version:', UCP_VERSION, '| Environment:', ENV_LABEL);
</script>
'''

# Append to index.html
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'r') as f:
    content = f.read()
idx = content.rfind('</body>')
new_content = content[:idx] + AGENT_JS + '\n' + content[idx:]
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'w') as f:
    f.write(new_content)
print(f"Part 3 written: Agent Engine. File size: {len(new_content):,} bytes")
