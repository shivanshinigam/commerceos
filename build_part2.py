#!/usr/bin/env python3
"""Build Part 2: Product catalog, merchants, scenarios, and rich real-world catalog"""

import os

CATALOG_JS = r'''
<!-- PART 2: PRODUCT CATALOG + CORE DATA -->
<script>
'use strict';
/* ================================================
   COMMERCEOS — DATA LAYER
   UCP Version: 2026-08-25
   Environment: SIMULATED COMMERCE ENVIRONMENT
   ================================================ */

const UCP_VERSION = '2026-08-25';
const APP_VERSION = '1.0.0';
const ENV_LABEL = 'SIMULATED_COMMERCE_ENVIRONMENT';

// ---- MERCHANTS ----
const MERCHANTS = {
  nova: {
    id: 'nova',
    name: 'NOVA',
    tagline: 'Premium. Fast. Reliable.',
    emoji: '⚡',
    color: '#7c3aed',
    specialty: 'Electronics & Premium Footwear',
    shipping_base: 99,
    shipping_free_threshold: 5000,
    policy: { returns: '30 days', warranty: '1 year', cod: false },
    capabilities: ['product_discovery','cart','checkout','order_management','fulfillment'],
    rating: 4.7
  },
  velomart: {
    id: 'velomart',
    name: 'VeloMart',
    tagline: 'Sports. Performance. Value.',
    emoji: '🏃',
    color: '#10b981',
    specialty: 'Sports & Fitness',
    shipping_base: 49,
    shipping_free_threshold: 3000,
    policy: { returns: '15 days', warranty: '6 months', cod: true },
    capabilities: ['product_discovery','cart','checkout','order_management'],
    rating: 4.4
  },
  urbancart: {
    id: 'urbancart',
    name: 'UrbanCart',
    tagline: 'Style. Variety. Everyday.',
    emoji: '🏙',
    color: '#f59e0b',
    specialty: 'Fashion & Lifestyle',
    shipping_base: 79,
    shipping_free_threshold: 4000,
    policy: { returns: '21 days', warranty: '1 year', cod: true },
    capabilities: ['product_discovery','cart','checkout','order_management','discount','fulfillment'],
    rating: 4.2
  }
};

// ---- RICH REAL-WORLD CURATED CATALOG ----
// Real products with accurate Indian Rupee prices across all budgets
const CURATED_CATALOG = [
  // --- DATASET FROM GenAI-Product-Recommender (Product_data.csv) ---
    {
        "id": "APP-0001",
        "title": "Flying Machine Red Stripped Sweatshirt (Women's, Size L)",
        "brand": "Flying Machine",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine red stripped sweatshirt women size l a red sweatshirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0002",
        "title": "Myntra Red Checked Sweatshirt (Men's, Size M)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1500,
        "rating": 4.2,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra red checked sweatshirt men size m a red sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0003",
        "title": "Puma White Stripped T-Shirt (Men's, Size L)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 816,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma white stripped t-shirt men size l a white t-shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0004",
        "title": "Myntra Black Checked Sweatshirt (Men's, Size M)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2412,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra black checked sweatshirt men size m a black sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0005",
        "title": "Wrangler Blue Checked Shirt (Kids's, Size XXL)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 2060,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "wrangler blue checked shirt kids size xxl a blue shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0006",
        "title": "Scullers Red Printed Sweatshirt (Kids's, Size XXL)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 2412,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers red printed sweatshirt kids size xxl a red sweatshirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0007",
        "title": "Benetton White Stripped Sweatshirt (Men's, Size S)",
        "brand": "Benetton",
        "category": "sweatshirt",
        "best_price": 1918,
        "rating": 4.6,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "benetton white stripped sweatshirt men size s a white sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0008",
        "title": "Lee White Stripped Shirt (Women's, Size M)",
        "brand": "Lee",
        "category": "shirt",
        "best_price": 1946,
        "rating": 4.7,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee white stripped shirt women size m a white shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0009",
        "title": "Highlander Green Printed Shirt (Women's, Size XXL)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1319,
        "rating": 4.8,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green printed shirt women size xxl a green shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0010",
        "title": "Benetton Green Printed Sweatshirt (Men's, Size XL)",
        "brand": "Benetton",
        "category": "sweatshirt",
        "best_price": 2336,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "benetton green printed sweatshirt men size xl a green sweatshirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0011",
        "title": "Myntra Red Stripped Shirt (Kids's, Size M)",
        "brand": "Myntra",
        "category": "shirt",
        "best_price": 1946,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "myntra red stripped shirt kids size m a red shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0012",
        "title": "Myntra Blue Checked Shirt (Women's, Size XXL)",
        "brand": "Myntra",
        "category": "shirt",
        "best_price": 1576,
        "rating": 4.2,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "myntra blue checked shirt women size xxl a blue shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0013",
        "title": "Highlander Red Checked T-Shirt (Women's, Size XL)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 778,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander red checked t-shirt women size xl a red t-shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0014",
        "title": "Scullers Blue Checked Shirt (Men's, Size S)",
        "brand": "Scullers",
        "category": "shirt",
        "best_price": 1576,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "scullers blue checked shirt men size s a blue shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0015",
        "title": "Flying Machine Black Checked T-Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1272,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine black checked t-shirt women size xl a black t-shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0016",
        "title": "Lee White Printed Sweatshirt (Men's, Size M)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 2602,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee white printed sweatshirt men size m a white sweatshirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0017",
        "title": "Myntra Blue Printed T-Shirt (Women's, Size XL)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 702,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra blue printed t-shirt women size xl a blue t-shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0018",
        "title": "Scullers Green Checked T-Shirt (Men's, Size S)",
        "brand": "Scullers",
        "category": "t_shirt",
        "best_price": 949,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers green checked t-shirt men size s a green t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0019",
        "title": "Lee Black Stripped T-Shirt (Men's, Size M)",
        "brand": "Lee",
        "category": "t_shirt",
        "best_price": 1367,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee black stripped t-shirt men size m a black t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0020",
        "title": "Scullers White Printed T-Shirt (Women's, Size L)",
        "brand": "Scullers",
        "category": "t_shirt",
        "best_price": 1405,
        "rating": 4.0,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers white printed t-shirt women size l a white t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0021",
        "title": "Scullers Green Checked Sweatshirt (Women's, Size L)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 2602,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers green checked sweatshirt women size l a green sweatshirt with a checked design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0022",
        "title": "Puma Green Checked T-Shirt (Men's, Size S)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 873,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma green checked t-shirt men size s a green t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0023",
        "title": "Scullers White Stripped Sweatshirt (Women's, Size XL)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 1614,
        "rating": 4.3,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers white stripped sweatshirt women size xl a white sweatshirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0024",
        "title": "Myntra Red Checked Sweatshirt (Men's, Size XXL)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2032,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra red checked sweatshirt men size xxl a red sweatshirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0025",
        "title": "Myntra White Printed Shirt (Women's, Size XL)",
        "brand": "Myntra",
        "category": "shirt",
        "best_price": 1034,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra white printed shirt women size xl a white shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0026",
        "title": "Highlander Green Stripped T-Shirt (Men's, Size L)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1367,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green stripped t-shirt men size l a green t-shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0027",
        "title": "Highlander Red Stripped T-Shirt (Women's, Size M)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1120,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander red stripped t-shirt women size m a red t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0028",
        "title": "Wrangler White Checked Shirt (Women's, Size XL)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 2089,
        "rating": 4.7,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "wrangler white checked shirt women size xl a white shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0029",
        "title": "Puma Blue Checked Shirt (Men's, Size XXL)",
        "brand": "Puma",
        "category": "shirt",
        "best_price": 1661,
        "rating": 4.8,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "puma blue checked shirt men size xxl a blue shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0030",
        "title": "Wrangler White Printed T-Shirt (Men's, Size L)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 835,
        "rating": 4.0,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "wrangler white printed t-shirt men size l a white t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0031",
        "title": "Wrangler Blue Checked Shirt (Men's, Size M)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 977,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "wrangler blue checked shirt men size m a blue shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0032",
        "title": "Highlander White Printed T-Shirt (Men's, Size M)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 835,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander white printed t-shirt men size m a white t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0033",
        "title": "Scullers Green Checked Shirt (Kids's, Size XL)",
        "brand": "Scullers",
        "category": "shirt",
        "best_price": 1661,
        "rating": 4.3,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "scullers green checked shirt kids size xl a green shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0034",
        "title": "Benetton Green Stripped T-Shirt (Men's, Size XL)",
        "brand": "Benetton",
        "category": "t_shirt",
        "best_price": 797,
        "rating": 4.4,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "benetton green stripped t-shirt men size xl a green t-shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0035",
        "title": "Myntra Red Checked T-Shirt (Women's, Size S)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1006,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra red checked t-shirt women size s a red t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0036",
        "title": "Myntra White Stripped Sweatshirt (Kids's, Size XXL)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1804,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra white stripped sweatshirt kids size xxl a white sweatshirt with a stripped design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0037",
        "title": "Lee Red Stripped Shirt (Men's, Size S)",
        "brand": "Lee",
        "category": "shirt",
        "best_price": 1177,
        "rating": 4.6,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee red stripped shirt men size s a red shirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0038",
        "title": "Scullers White Checked Sweatshirt (Men's, Size XXL)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 1804,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers white checked sweatshirt men size xxl a white sweatshirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0039",
        "title": "Highlander Red Printed T-Shirt (Men's, Size S)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1006,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander red printed t-shirt men size s a red t-shirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0040",
        "title": "Flying Machine Red Stripped Shirt (Kids's, Size L)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.0,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine red stripped shirt kids size l a red shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0041",
        "title": "Puma Green Checked T-Shirt (Women's, Size M)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 930,
        "rating": 4.1,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma green checked t-shirt women size m a green t-shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0042",
        "title": "Myntra Blue Printed T-Shirt (Men's, Size S)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1177,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra blue printed t-shirt men size s a blue t-shirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0043",
        "title": "Puma Black Checked T-Shirt (Kids's, Size L)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 1386,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma black checked t-shirt kids size l a black t-shirt with a checked design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0044",
        "title": "Flying Machine Blue Printed Shirt (Men's, Size L)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1234,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine blue printed shirt men size l a blue shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0045",
        "title": "Wrangler White Printed Sweatshirt (Men's, Size S)",
        "brand": "Wrangler",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "wrangler white printed sweatshirt men size s a white sweatshirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0046",
        "title": "Flying Machine Green Stripped T-Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1215,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine green stripped t-shirt women size xl a green t-shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0047",
        "title": "Highlander Blue Printed Shirt (Women's, Size M)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1490,
        "rating": 4.6,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander blue printed shirt women size m a blue shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0048",
        "title": "Flying Machine Green Printed T-Shirt (Kids's, Size M)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 721,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine green printed t-shirt kids size m a green t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0049",
        "title": "Benetton Blue Checked Shirt (Kids's, Size L)",
        "brand": "Benetton",
        "category": "shirt",
        "best_price": 1433,
        "rating": 4.8,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "benetton blue checked shirt kids size l a blue shirt with a checked design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0050",
        "title": "Lee Green Printed T-Shirt (Kids's, Size L)",
        "brand": "Lee",
        "category": "t_shirt",
        "best_price": 1310,
        "rating": 4.0,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee green printed t-shirt kids size l a green t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0051",
        "title": "Flying Machine Blue Checked Sweatshirt (Women's, Size M)",
        "brand": "Flying Machine",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine blue checked sweatshirt women size m a blue sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0052",
        "title": "Highlander Black Checked Shirt (Men's, Size XXL)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1063,
        "rating": 4.2,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "highlander black checked shirt men size xxl a black shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0053",
        "title": "Flying Machine Blue Stripped T-Shirt (Kids's, Size M)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1386,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine blue stripped t-shirt kids size m a blue t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0054",
        "title": "Lee Red Checked Shirt (Men's, Size M)",
        "brand": "Lee",
        "category": "shirt",
        "best_price": 2003,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "lee red checked shirt men size m a red shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0055",
        "title": "Flying Machine Blue Stripped Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1433,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine blue stripped shirt women size xl a blue shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0056",
        "title": "Lee Red Stripped Sweatshirt (Women's, Size M)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 1842,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee red stripped sweatshirt women size m a red sweatshirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0057",
        "title": "Lee Red Checked T-Shirt (Women's, Size XXL)",
        "brand": "Lee",
        "category": "t_shirt",
        "best_price": 1481,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee red checked t-shirt women size xxl a red t-shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0058",
        "title": "Benetton Green Printed Sweatshirt (Kids's, Size XL)",
        "brand": "Benetton",
        "category": "sweatshirt",
        "best_price": 1424,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "benetton green printed sweatshirt kids size xl a green sweatshirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0059",
        "title": "Puma White Stripped T-Shirt (Kids's, Size XXL)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 1234,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma white stripped t-shirt kids size xxl a white t-shirt with a stripped design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0060",
        "title": "Puma Green Stripped Sweatshirt (Men's, Size S)",
        "brand": "Puma",
        "category": "sweatshirt",
        "best_price": 2260,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma green stripped sweatshirt men size s a green sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0061",
        "title": "Flying Machine Green Printed Sweatshirt (Kids's, Size S)",
        "brand": "Flying Machine",
        "category": "sweatshirt",
        "best_price": 2906,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine green printed sweatshirt kids size s a green sweatshirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0062",
        "title": "Puma White Checked T-Shirt (Kids's, Size XXL)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 1443,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma white checked t-shirt kids size xxl a white t-shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0063",
        "title": "Highlander Green Printed Sweatshirt (Kids's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 1842,
        "rating": 4.3,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green printed sweatshirt kids size m a green sweatshirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0064",
        "title": "Myntra Red Printed T-Shirt (Women's, Size L)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1443,
        "rating": 4.4,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra red printed t-shirt women size l a red t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0065",
        "title": "Scullers Red Stripped Sweatshirt (Women's, Size S)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 1766,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "scullers red stripped sweatshirt women size s a red sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0066",
        "title": "Puma Green Stripped Sweatshirt (Kids's, Size XL)",
        "brand": "Puma",
        "category": "sweatshirt",
        "best_price": 3096,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma green stripped sweatshirt kids size xl a green sweatshirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0067",
        "title": "Lee Blue Printed Sweatshirt (Women's, Size L)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 2108,
        "rating": 4.6,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee blue printed sweatshirt women size l a blue sweatshirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0068",
        "title": "Highlander Green Checked Sweatshirt (Women's, Size S)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 3172,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green checked sweatshirt women size s a green sweatshirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0069",
        "title": "Highlander Black Checked Sweatshirt (Kids's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 2678,
        "rating": 4.8,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander black checked sweatshirt kids size m a black sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0070",
        "title": "Highlander Green Checked Sweatshirt (Kids's, Size XL)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 2184,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green checked sweatshirt kids size xl a green sweatshirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0071",
        "title": "Benetton Red Checked Shirt (Men's, Size S)",
        "brand": "Benetton",
        "category": "shirt",
        "best_price": 1832,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "benetton red checked shirt men size s a red shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0072",
        "title": "Myntra Blue Stripped T-Shirt (Kids's, Size M)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1367,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra blue stripped t-shirt kids size m a blue t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0073",
        "title": "Highlander Green Stripped T-Shirt (Men's, Size S)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1158,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green stripped t-shirt men size s a green t-shirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0074",
        "title": "Myntra Black Printed Sweatshirt (Women's, Size S)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2032,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra black printed sweatshirt women size s a black sweatshirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0075",
        "title": "Highlander Red Checked T-Shirt (Kids's, Size S)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 664,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander red checked t-shirt kids size s a red t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0076",
        "title": "Flying Machine Black Printed Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 2203,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine black printed shirt women size xl a black shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0077",
        "title": "Wrangler Black Stripped T-Shirt (Men's, Size M)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 626,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "wrangler black stripped t-shirt men size m a black t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0078",
        "title": "Wrangler Black Printed T-Shirt (Women's, Size M)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 1329,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "wrangler black printed t-shirt women size m a black t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0079",
        "title": "Myntra Black Stripped Sweatshirt (Kids's, Size S)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1462,
        "rating": 4.8,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra black stripped sweatshirt kids size s a black sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0080",
        "title": "Puma Green Printed Shirt (Women's, Size L)",
        "brand": "Puma",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.0,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "puma green printed shirt women size l a green shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0081",
        "title": "Highlander Red Stripped T-Shirt (Women's, Size L)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1082,
        "rating": 4.1,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander red stripped t-shirt women size l a red t-shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0082",
        "title": "Highlander White Printed Sweatshirt (Kids's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 1956,
        "rating": 4.2,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander white printed sweatshirt kids size m a white sweatshirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0083",
        "title": "Highlander Black Checked Sweatshirt (Men's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 1462,
        "rating": 4.3,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander black checked sweatshirt men size m a black sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0084",
        "title": "Wrangler Blue Printed Shirt (Women's, Size XL)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=60",
        "search_text": "wrangler blue printed shirt women size xl a blue shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0085",
        "title": "Scullers White Checked Shirt (Kids's, Size M)",
        "brand": "Scullers",
        "category": "shirt",
        "best_price": 2345,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "scullers white checked shirt kids size m a white shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0086",
        "title": "Highlander Green Printed Shirt (Kids's, Size XXL)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "highlander green printed shirt kids size xxl a green shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0087",
        "title": "Highlander Green Checked Sweatshirt (Men's, Size XXL)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 3286,
        "rating": 4.6,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "highlander green checked sweatshirt men size xxl a green sweatshirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0088",
        "title": "Benetton Green Stripped T-Shirt (Women's, Size XXL)",
        "brand": "Benetton",
        "category": "t_shirt",
        "best_price": 759,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=60",
        "search_text": "benetton green stripped t-shirt women size xxl a green t-shirt with a stripped design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0089",
        "title": "Myntra Blue Printed T-Shirt (Men's, Size M)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 968,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra blue printed t-shirt men size m a blue t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0090",
        "title": "Lee Black Printed Sweatshirt (Men's, Size XXL)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee black printed sweatshirt men size xxl a black sweatshirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0091",
        "title": "Puma Green Checked Shirt (Kids's, Size XXL)",
        "brand": "Puma",
        "category": "shirt",
        "best_price": 1490,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "puma green checked shirt kids size xxl a green shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0092",
        "title": "Puma Black Printed T-Shirt (Women's, Size XXL)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 683,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma black printed t-shirt women size xxl a black t-shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0093",
        "title": "Wrangler Red Stripped T-Shirt (Kids's, Size XL)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 1424,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "wrangler red stripped t-shirt kids size xl a red t-shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0094",
        "title": "Myntra Black Stripped Sweatshirt (Women's, Size XL)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1652,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra black stripped sweatshirt women size xl a black sweatshirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0095",
        "title": "Lee Green Printed Sweatshirt (Men's, Size L)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 1576,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee green printed sweatshirt men size l a green sweatshirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0096",
        "title": "Flying Machine Red Printed T-Shirt (Men's, Size XXL)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1215,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=60",
        "search_text": "flying machine red printed t-shirt men size xxl a red t-shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0097",
        "title": "Flying Machine Black Checked Shirt (Kids's, Size XXL)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1547,
        "rating": 4.6,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png",
        "search_text": "flying machine black checked shirt kids size xxl a black shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0098",
        "title": "Lee Green Stripped Sweatshirt (Women's, Size S)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 1994,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=60",
        "search_text": "lee green stripped sweatshirt women size s a green sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0099",
        "title": "Puma White Checked Sweatshirt (Kids's, Size M)",
        "brand": "Puma",
        "category": "sweatshirt",
        "best_price": 1994,
        "rating": 4.8,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60",
        "search_text": "puma white checked sweatshirt kids size m a white sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0100",
        "title": "Myntra Green Stripped Sweatshirt (Kids's, Size L)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2488,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=500&auto=format&fit=crop&q=60",
        "search_text": "myntra green stripped sweatshirt kids size l a green sweatshirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    }
,

  // --- DATASET FROM GenAI-Product-Recommender (Product_data.csv) ---
    {
        "id": "APP-0001",
        "title": "Flying Machine Red Stripped Sweatshirt (Women's, Size L)",
        "brand": "Flying Machine",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine red stripped sweatshirt women size l a red sweatshirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0002",
        "title": "Myntra Red Checked Sweatshirt (Men's, Size M)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1500,
        "rating": 4.2,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra red checked sweatshirt men size m a red sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0003",
        "title": "Puma White Stripped T-Shirt (Men's, Size L)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 816,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma white stripped t-shirt men size l a white t-shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0004",
        "title": "Myntra Black Checked Sweatshirt (Men's, Size M)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2412,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra black checked sweatshirt men size m a black sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0005",
        "title": "Wrangler Blue Checked Shirt (Kids's, Size XXL)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 2060,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler blue checked shirt kids size xxl a blue shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0006",
        "title": "Scullers Red Printed Sweatshirt (Kids's, Size XXL)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 2412,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers red printed sweatshirt kids size xxl a red sweatshirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0007",
        "title": "Benetton White Stripped Sweatshirt (Men's, Size S)",
        "brand": "Benetton",
        "category": "sweatshirt",
        "best_price": 1918,
        "rating": 4.6,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton white stripped sweatshirt men size s a white sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0008",
        "title": "Lee White Stripped Shirt (Women's, Size M)",
        "brand": "Lee",
        "category": "shirt",
        "best_price": 1946,
        "rating": 4.7,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee white stripped shirt women size m a white shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0009",
        "title": "Highlander Green Printed Shirt (Women's, Size XXL)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1319,
        "rating": 4.8,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green printed shirt women size xxl a green shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0010",
        "title": "Benetton Green Printed Sweatshirt (Men's, Size XL)",
        "brand": "Benetton",
        "category": "sweatshirt",
        "best_price": 2336,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton green printed sweatshirt men size xl a green sweatshirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0011",
        "title": "Myntra Red Stripped Shirt (Kids's, Size M)",
        "brand": "Myntra",
        "category": "shirt",
        "best_price": 1946,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra red stripped shirt kids size m a red shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0012",
        "title": "Myntra Blue Checked Shirt (Women's, Size XXL)",
        "brand": "Myntra",
        "category": "shirt",
        "best_price": 1576,
        "rating": 4.2,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra blue checked shirt women size xxl a blue shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0013",
        "title": "Highlander Red Checked T-Shirt (Women's, Size XL)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 778,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander red checked t-shirt women size xl a red t-shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0014",
        "title": "Scullers Blue Checked Shirt (Men's, Size S)",
        "brand": "Scullers",
        "category": "shirt",
        "best_price": 1576,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers blue checked shirt men size s a blue shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0015",
        "title": "Flying Machine Black Checked T-Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1272,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine black checked t-shirt women size xl a black t-shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0016",
        "title": "Lee White Printed Sweatshirt (Men's, Size M)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 2602,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee white printed sweatshirt men size m a white sweatshirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0017",
        "title": "Myntra Blue Printed T-Shirt (Women's, Size XL)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 702,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra blue printed t-shirt women size xl a blue t-shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0018",
        "title": "Scullers Green Checked T-Shirt (Men's, Size S)",
        "brand": "Scullers",
        "category": "t_shirt",
        "best_price": 949,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers green checked t-shirt men size s a green t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0019",
        "title": "Lee Black Stripped T-Shirt (Men's, Size M)",
        "brand": "Lee",
        "category": "t_shirt",
        "best_price": 1367,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee black stripped t-shirt men size m a black t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0020",
        "title": "Scullers White Printed T-Shirt (Women's, Size L)",
        "brand": "Scullers",
        "category": "t_shirt",
        "best_price": 1405,
        "rating": 4.0,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers white printed t-shirt women size l a white t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0021",
        "title": "Scullers Green Checked Sweatshirt (Women's, Size L)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 2602,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers green checked sweatshirt women size l a green sweatshirt with a checked design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0022",
        "title": "Puma Green Checked T-Shirt (Men's, Size S)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 873,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma green checked t-shirt men size s a green t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0023",
        "title": "Scullers White Stripped Sweatshirt (Women's, Size XL)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 1614,
        "rating": 4.3,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers white stripped sweatshirt women size xl a white sweatshirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0024",
        "title": "Myntra Red Checked Sweatshirt (Men's, Size XXL)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2032,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra red checked sweatshirt men size xxl a red sweatshirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0025",
        "title": "Myntra White Printed Shirt (Women's, Size XL)",
        "brand": "Myntra",
        "category": "shirt",
        "best_price": 1034,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra white printed shirt women size xl a white shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0026",
        "title": "Highlander Green Stripped T-Shirt (Men's, Size L)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1367,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green stripped t-shirt men size l a green t-shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0027",
        "title": "Highlander Red Stripped T-Shirt (Women's, Size M)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1120,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander red stripped t-shirt women size m a red t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0028",
        "title": "Wrangler White Checked Shirt (Women's, Size XL)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 2089,
        "rating": 4.7,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler white checked shirt women size xl a white shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0029",
        "title": "Puma Blue Checked Shirt (Men's, Size XXL)",
        "brand": "Puma",
        "category": "shirt",
        "best_price": 1661,
        "rating": 4.8,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma blue checked shirt men size xxl a blue shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0030",
        "title": "Wrangler White Printed T-Shirt (Men's, Size L)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 835,
        "rating": 4.0,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler white printed t-shirt men size l a white t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0031",
        "title": "Wrangler Blue Checked Shirt (Men's, Size M)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 977,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler blue checked shirt men size m a blue shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0032",
        "title": "Highlander White Printed T-Shirt (Men's, Size M)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 835,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander white printed t-shirt men size m a white t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0033",
        "title": "Scullers Green Checked Shirt (Kids's, Size XL)",
        "brand": "Scullers",
        "category": "shirt",
        "best_price": 1661,
        "rating": 4.3,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers green checked shirt kids size xl a green shirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0034",
        "title": "Benetton Green Stripped T-Shirt (Men's, Size XL)",
        "brand": "Benetton",
        "category": "t_shirt",
        "best_price": 797,
        "rating": 4.4,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton green stripped t-shirt men size xl a green t-shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0035",
        "title": "Myntra Red Checked T-Shirt (Women's, Size S)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1006,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra red checked t-shirt women size s a red t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0036",
        "title": "Myntra White Stripped Sweatshirt (Kids's, Size XXL)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1804,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra white stripped sweatshirt kids size xxl a white sweatshirt with a stripped design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0037",
        "title": "Lee Red Stripped Shirt (Men's, Size S)",
        "brand": "Lee",
        "category": "shirt",
        "best_price": 1177,
        "rating": 4.6,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee red stripped shirt men size s a red shirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0038",
        "title": "Scullers White Checked Sweatshirt (Men's, Size XXL)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 1804,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers white checked sweatshirt men size xxl a white sweatshirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0039",
        "title": "Highlander Red Printed T-Shirt (Men's, Size S)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1006,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander red printed t-shirt men size s a red t-shirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0040",
        "title": "Flying Machine Red Stripped Shirt (Kids's, Size L)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.0,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine red stripped shirt kids size l a red shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0041",
        "title": "Puma Green Checked T-Shirt (Women's, Size M)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 930,
        "rating": 4.1,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma green checked t-shirt women size m a green t-shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0042",
        "title": "Myntra Blue Printed T-Shirt (Men's, Size S)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1177,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra blue printed t-shirt men size s a blue t-shirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0043",
        "title": "Puma Black Checked T-Shirt (Kids's, Size L)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 1386,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma black checked t-shirt kids size l a black t-shirt with a checked design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0044",
        "title": "Flying Machine Blue Printed Shirt (Men's, Size L)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1234,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine blue printed shirt men size l a blue shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0045",
        "title": "Wrangler White Printed Sweatshirt (Men's, Size S)",
        "brand": "Wrangler",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler white printed sweatshirt men size s a white sweatshirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0046",
        "title": "Flying Machine Green Stripped T-Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1215,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine green stripped t-shirt women size xl a green t-shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0047",
        "title": "Highlander Blue Printed Shirt (Women's, Size M)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1490,
        "rating": 4.6,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander blue printed shirt women size m a blue shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0048",
        "title": "Flying Machine Green Printed T-Shirt (Kids's, Size M)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 721,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine green printed t-shirt kids size m a green t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0049",
        "title": "Benetton Blue Checked Shirt (Kids's, Size L)",
        "brand": "Benetton",
        "category": "shirt",
        "best_price": 1433,
        "rating": 4.8,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton blue checked shirt kids size l a blue shirt with a checked design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0050",
        "title": "Lee Green Printed T-Shirt (Kids's, Size L)",
        "brand": "Lee",
        "category": "t_shirt",
        "best_price": 1310,
        "rating": 4.0,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee green printed t-shirt kids size l a green t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0051",
        "title": "Flying Machine Blue Checked Sweatshirt (Women's, Size M)",
        "brand": "Flying Machine",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine blue checked sweatshirt women size m a blue sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0052",
        "title": "Highlander Black Checked Shirt (Men's, Size XXL)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1063,
        "rating": 4.2,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander black checked shirt men size xxl a black shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0053",
        "title": "Flying Machine Blue Stripped T-Shirt (Kids's, Size M)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1386,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine blue stripped t-shirt kids size m a blue t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0054",
        "title": "Lee Red Checked Shirt (Men's, Size M)",
        "brand": "Lee",
        "category": "shirt",
        "best_price": 2003,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee red checked shirt men size m a red shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0055",
        "title": "Flying Machine Blue Stripped Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1433,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine blue stripped shirt women size xl a blue shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0056",
        "title": "Lee Red Stripped Sweatshirt (Women's, Size M)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 1842,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee red stripped sweatshirt women size m a red sweatshirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0057",
        "title": "Lee Red Checked T-Shirt (Women's, Size XXL)",
        "brand": "Lee",
        "category": "t_shirt",
        "best_price": 1481,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee red checked t-shirt women size xxl a red t-shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0058",
        "title": "Benetton Green Printed Sweatshirt (Kids's, Size XL)",
        "brand": "Benetton",
        "category": "sweatshirt",
        "best_price": 1424,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton green printed sweatshirt kids size xl a green sweatshirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0059",
        "title": "Puma White Stripped T-Shirt (Kids's, Size XXL)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 1234,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma white stripped t-shirt kids size xxl a white t-shirt with a stripped design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0060",
        "title": "Puma Green Stripped Sweatshirt (Men's, Size S)",
        "brand": "Puma",
        "category": "sweatshirt",
        "best_price": 2260,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma green stripped sweatshirt men size s a green sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0061",
        "title": "Flying Machine Green Printed Sweatshirt (Kids's, Size S)",
        "brand": "Flying Machine",
        "category": "sweatshirt",
        "best_price": 2906,
        "rating": 4.1,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine green printed sweatshirt kids size s a green sweatshirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0062",
        "title": "Puma White Checked T-Shirt (Kids's, Size XXL)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 1443,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma white checked t-shirt kids size xxl a white t-shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0063",
        "title": "Highlander Green Printed Sweatshirt (Kids's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 1842,
        "rating": 4.3,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green printed sweatshirt kids size m a green sweatshirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0064",
        "title": "Myntra Red Printed T-Shirt (Women's, Size L)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1443,
        "rating": 4.4,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra red printed t-shirt women size l a red t-shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0065",
        "title": "Scullers Red Stripped Sweatshirt (Women's, Size S)",
        "brand": "Scullers",
        "category": "sweatshirt",
        "best_price": 1766,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers red stripped sweatshirt women size s a red sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0066",
        "title": "Puma Green Stripped Sweatshirt (Kids's, Size XL)",
        "brand": "Puma",
        "category": "sweatshirt",
        "best_price": 3096,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma green stripped sweatshirt kids size xl a green sweatshirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0067",
        "title": "Lee Blue Printed Sweatshirt (Women's, Size L)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 2108,
        "rating": 4.6,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee blue printed sweatshirt women size l a blue sweatshirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0068",
        "title": "Highlander Green Checked Sweatshirt (Women's, Size S)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 3172,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green checked sweatshirt women size s a green sweatshirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0069",
        "title": "Highlander Black Checked Sweatshirt (Kids's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 2678,
        "rating": 4.8,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander black checked sweatshirt kids size m a black sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0070",
        "title": "Highlander Green Checked Sweatshirt (Kids's, Size XL)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 2184,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green checked sweatshirt kids size xl a green sweatshirt with a checked design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0071",
        "title": "Benetton Red Checked Shirt (Men's, Size S)",
        "brand": "Benetton",
        "category": "shirt",
        "best_price": 1832,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton red checked shirt men size s a red shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0072",
        "title": "Myntra Blue Stripped T-Shirt (Kids's, Size M)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 1367,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra blue stripped t-shirt kids size m a blue t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0073",
        "title": "Highlander Green Stripped T-Shirt (Men's, Size S)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1158,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green stripped t-shirt men size s a green t-shirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0074",
        "title": "Myntra Black Printed Sweatshirt (Women's, Size S)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2032,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra black printed sweatshirt women size s a black sweatshirt with a printed design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0075",
        "title": "Highlander Red Checked T-Shirt (Kids's, Size S)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 664,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander red checked t-shirt kids size s a red t-shirt with a checked design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0076",
        "title": "Flying Machine Black Printed Shirt (Women's, Size XL)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 2203,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine black printed shirt women size xl a black shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0077",
        "title": "Wrangler Black Stripped T-Shirt (Men's, Size M)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 626,
        "rating": 4.6,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler black stripped t-shirt men size m a black t-shirt with a stripped design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0078",
        "title": "Wrangler Black Printed T-Shirt (Women's, Size M)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 1329,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler black printed t-shirt women size m a black t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0079",
        "title": "Myntra Black Stripped Sweatshirt (Kids's, Size S)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1462,
        "rating": 4.8,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra black stripped sweatshirt kids size s a black sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0080",
        "title": "Puma Green Printed Shirt (Women's, Size L)",
        "brand": "Puma",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.0,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma green printed shirt women size l a green shirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0081",
        "title": "Highlander Red Stripped T-Shirt (Women's, Size L)",
        "brand": "Highlander",
        "category": "t_shirt",
        "best_price": 1082,
        "rating": 4.1,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander red stripped t-shirt women size l a red t-shirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0082",
        "title": "Highlander White Printed Sweatshirt (Kids's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 1956,
        "rating": 4.2,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander white printed sweatshirt kids size m a white sweatshirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0083",
        "title": "Highlander Black Checked Sweatshirt (Men's, Size M)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 1462,
        "rating": 4.3,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander black checked sweatshirt men size m a black sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0084",
        "title": "Wrangler Blue Printed Shirt (Women's, Size XL)",
        "brand": "Wrangler",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.4,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler blue printed shirt women size xl a blue shirt with a printed design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0085",
        "title": "Scullers White Checked Shirt (Kids's, Size M)",
        "brand": "Scullers",
        "category": "shirt",
        "best_price": 2345,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "scullers white checked shirt kids size m a white shirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0086",
        "title": "Highlander Green Printed Shirt (Kids's, Size XXL)",
        "brand": "Highlander",
        "category": "shirt",
        "best_price": 1291,
        "rating": 4.5,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green printed shirt kids size xxl a green shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0087",
        "title": "Highlander Green Checked Sweatshirt (Men's, Size XXL)",
        "brand": "Highlander",
        "category": "sweatshirt",
        "best_price": 3286,
        "rating": 4.6,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "highlander green checked sweatshirt men size xxl a green sweatshirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0088",
        "title": "Benetton Green Stripped T-Shirt (Women's, Size XXL)",
        "brand": "Benetton",
        "category": "t_shirt",
        "best_price": 759,
        "rating": 4.7,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "benetton green stripped t-shirt women size xxl a green t-shirt with a stripped design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0089",
        "title": "Myntra Blue Printed T-Shirt (Men's, Size M)",
        "brand": "Myntra",
        "category": "t_shirt",
        "best_price": 968,
        "rating": 4.8,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra blue printed t-shirt men size m a blue t-shirt with a printed design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0090",
        "title": "Lee Black Printed Sweatshirt (Men's, Size XXL)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 2146,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee black printed sweatshirt men size xxl a black sweatshirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0091",
        "title": "Puma Green Checked Shirt (Kids's, Size XXL)",
        "brand": "Puma",
        "category": "shirt",
        "best_price": 1490,
        "rating": 4.1,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma green checked shirt kids size xxl a green shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0092",
        "title": "Puma Black Printed T-Shirt (Women's, Size XXL)",
        "brand": "Puma",
        "category": "t_shirt",
        "best_price": 683,
        "rating": 4.2,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma black printed t-shirt women size xxl a black t-shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0093",
        "title": "Wrangler Red Stripped T-Shirt (Kids's, Size XL)",
        "brand": "Wrangler",
        "category": "t_shirt",
        "best_price": 1424,
        "rating": 4.3,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "wrangler red stripped t-shirt kids size xl a red t-shirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0094",
        "title": "Myntra Black Stripped Sweatshirt (Women's, Size XL)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 1652,
        "rating": 4.4,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra black stripped sweatshirt women size xl a black sweatshirt with a stripped design in size xl.",
        "sizes": [
            "XL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0095",
        "title": "Lee Green Printed Sweatshirt (Men's, Size L)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 1576,
        "rating": 4.5,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee green printed sweatshirt men size l a green sweatshirt with a printed design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0096",
        "title": "Flying Machine Red Printed T-Shirt (Men's, Size XXL)",
        "brand": "Flying Machine",
        "category": "t_shirt",
        "best_price": 1215,
        "rating": 4.5,
        "emoji": "\ud83d\udc55",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine red printed t-shirt men size xxl a red t-shirt with a printed design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0097",
        "title": "Flying Machine Black Checked Shirt (Kids's, Size XXL)",
        "brand": "Flying Machine",
        "category": "shirt",
        "best_price": 1547,
        "rating": 4.6,
        "emoji": "\ud83d\udc54",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "flying machine black checked shirt kids size xxl a black shirt with a checked design in size xxl.",
        "sizes": [
            "XXL"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0098",
        "title": "Lee Green Stripped Sweatshirt (Women's, Size S)",
        "brand": "Lee",
        "category": "sweatshirt",
        "best_price": 1994,
        "rating": 4.7,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "lee green stripped sweatshirt women size s a green sweatshirt with a stripped design in size s.",
        "sizes": [
            "S"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0099",
        "title": "Puma White Checked Sweatshirt (Kids's, Size M)",
        "brand": "Puma",
        "category": "sweatshirt",
        "best_price": 1994,
        "rating": 4.8,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "puma white checked sweatshirt kids size m a white sweatshirt with a checked design in size m.",
        "sizes": [
            "M"
        ],
        "in_stock": true
    },
    {
        "id": "APP-0100",
        "title": "Myntra Green Stripped Sweatshirt (Kids's, Size L)",
        "brand": "Myntra",
        "category": "sweatshirt",
        "best_price": 2488,
        "rating": 4.0,
        "emoji": "\ud83e\udde5",
        "image": "https://cdn.dummyjson.com/products/images/top-wear/thumbnail.png",
        "search_text": "myntra green stripped sweatshirt kids size l a green sweatshirt with a stripped design in size l.",
        "sizes": [
            "L"
        ],
        "in_stock": true
    }
,

  // SMARTPHONES
  {
    id: 'IPHONE-15-PRO-MAX',
    title: 'Apple iPhone 15 Pro Max (256GB, Natural Titanium)',
    brand: 'Apple',
    category: 'smartphones',
    best_price: 159900,
    rating: 4.8,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/iPhone%206/thumbnail.png',
    search_text: 'apple iphone 15 pro max natural titanium 256gb 5g ios mobile phone smartphone',
    sizes: ['128GB', '256GB', '512GB', '1TB'],
    in_stock: true
  },
  {
    id: 'IPHONE-15',
    title: 'Apple iPhone 15 (128GB, Black)',
    brand: 'Apple',
    category: 'smartphones',
    best_price: 79900,
    rating: 4.7,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/iPhone%2013%20Pro/thumbnail.png',
    search_text: 'apple iphone 15 128gb black 5g ios mobile phone smartphone',
    sizes: ['128GB', '256GB', '512GB'],
    in_stock: true
  },
  {
    id: 'IPHONE-14',
    title: 'Apple iPhone 14 (128GB, Blue)',
    brand: 'Apple',
    category: 'smartphones',
    best_price: 69900,
    rating: 4.6,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/iPhone%20X/thumbnail.png',
    search_text: 'apple iphone 14 128gb blue 5g ios mobile phone smartphone',
    sizes: ['128GB', '256GB'],
    in_stock: true
  },
  {
    id: 'IPHONE-13',
    title: 'Apple iPhone 13 (128GB, Midnight)',
    brand: 'Apple',
    category: 'smartphones',
    best_price: 52900,
    rating: 4.7,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/iPhone%2013%20Pro/thumbnail.png',
    search_text: 'apple iphone 13 128gb midnight 5g ios mobile phone smartphone',
    sizes: ['128GB', '256GB'],
    in_stock: true
  },
  {
    id: 'SAMSUNG-S24-ULTRA',
    title: 'Samsung Galaxy S24 Ultra (5G, 256GB, Titanium Gray)',
    brand: 'Samsung',
    category: 'smartphones',
    best_price: 129999,
    rating: 4.8,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/Samsung%20Galaxy%20S10/thumbnail.png',
    search_text: 'samsung galaxy s24 ultra 5g titanium gray 256gb android mobile phone smartphone',
    sizes: ['256GB', '512GB'],
    in_stock: true
  },
  {
    id: 'SAMSUNG-S23-FE',
    title: 'Samsung Galaxy S23 FE (8GB RAM, 128GB, Mint)',
    brand: 'Samsung',
    category: 'smartphones',
    best_price: 49999,
    rating: 4.4,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/Samsung%20Galaxy%20S8/thumbnail.png',
    search_text: 'samsung galaxy s23 fe mint 128gb 5g android mobile phone smartphone',
    sizes: ['128GB', '256GB'],
    in_stock: true
  },
  {
    id: 'ONEPLUS-12',
    title: 'OnePlus 12 (16GB RAM, 512GB, Silky Black)',
    brand: 'OnePlus',
    category: 'smartphones',
    best_price: 64999,
    rating: 4.6,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/Realme%20XT/thumbnail.png',
    search_text: 'oneplus 12 16gb 512gb silky black 5g android mobile phone smartphone',
    sizes: ['256GB', '512GB'],
    in_stock: true
  },
  {
    id: 'PIXEL-8-PRO',
    title: 'Google Pixel 8 Pro (128GB, Bay Blue)',
    brand: 'Google',
    category: 'smartphones',
    best_price: 93999,
    rating: 4.5,
    emoji: '📱',
    image: 'https://cdn.dummyjson.com/products/images/smartphones/Oppo%20F19%20Pro%20Plus/thumbnail.png',
    search_text: 'google pixel 8 pro bay blue 128gb tensor g3 5g android mobile phone smartphone',
    sizes: ['128GB', '256GB'],
    in_stock: true
  },

  // LAPTOPS
  {
    id: 'MACBOOK-AIR-M3',
    title: 'Apple MacBook Air M3 (15-inch, 16GB RAM, 512GB SSD, Starlight)',
    brand: 'Apple',
    category: 'laptops',
    best_price: 134900,
    rating: 4.9,
    emoji: '💻',
    image: 'https://cdn.dummyjson.com/products/images/laptops/Apple%20MacBook%20Pro%2014%20Inch%20Space%20Grey/thumbnail.png',
    search_text: 'apple macbook air m3 15-inch 16gb 512gb starlight laptop notebook computer python machine learning',
    sizes: ['13-inch', '15-inch'],
    in_stock: true
  },
  {
    id: 'MACBOOK-AIR-M2',
    title: 'Apple MacBook Air M2 (13.6-inch, 8GB RAM, 256GB SSD, Space Grey)',
    brand: 'Apple',
    category: 'laptops',
    best_price: 89900,
    rating: 4.8,
    emoji: '💻',
    image: 'https://cdn.dummyjson.com/products/images/laptops/Apple%20MacBook%20Pro%2014%20Inch%20Space%20Grey/thumbnail.png',
    search_text: 'apple macbook air m2 13-inch 8gb 256gb space grey laptop notebook computer python ml',
    sizes: ['13-inch'],
    in_stock: true
  },
  {
    id: 'ASUS-ROG-G16',
    title: 'ASUS ROG Zephyrus G16 (Intel Core i9, RTX 4070, 32GB RAM, 1TB SSD)',
    brand: 'Asus',
    category: 'laptops',
    best_price: 189990,
    rating: 4.7,
    emoji: '💻',
    image: 'https://cdn.dummyjson.com/products/images/laptops/Asus%20Zenbook%20Pro%20Dual%20Screen%20Laptop/thumbnail.png',
    search_text: 'asus rog zephyrus g16 intel core i9 rtx 4070 32gb gaming machine learning python gpu laptop',
    sizes: ['16-inch'],
    in_stock: true
  },
  {
    id: 'LENOVO-LEGION-5',
    title: 'Lenovo Legion Slim 5 (AMD Ryzen 7 7840HS, RTX 4060, 16GB, 1TB SSD)',
    brand: 'Lenovo',
    category: 'laptops',
    best_price: 98990,
    rating: 4.6,
    emoji: '💻',
    image: 'https://cdn.dummyjson.com/products/images/laptops/Lenovo%20IdeaPad%20Flex%205/thumbnail.png',
    search_text: 'lenovo legion slim 5 ryzen 7 rtx 4060 16gb gaming python machine learning ai gpu laptop',
    sizes: ['16-inch'],
    in_stock: true
  },
  {
    id: 'ACER-SWIFT-GO',
    title: 'Acer Swift Go 14 (OLED, Intel Core Ultra 5, 16GB RAM, 512GB SSD)',
    brand: 'Acer',
    category: 'laptops',
    best_price: 62990,
    rating: 4.4,
    emoji: '💻',
    image: 'https://cdn.dummyjson.com/products/images/laptops/Huawei%20MateBook%20X%20Pro/thumbnail.png',
    search_text: 'acer swift go 14 oled intel core ultra 5 16gb 512gb python data science student laptop',
    sizes: ['14-inch'],
    in_stock: true
  },

  // HEADPHONES & AUDIO
  {
    id: 'SONY-WH1000XM5',
    title: 'Sony WH-1000XM5 Premium Wireless Noise Cancelling Headphones (Black)',
    brand: 'Sony',
    category: 'mobile-accessories',
    best_price: 29990,
    rating: 4.8,
    emoji: '🎧',
    image: 'https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20AirPods%20Max%20Silver/thumbnail.png',
    search_text: 'sony wh-1000xm5 wireless noise cancelling anc over-ear headphones long battery 30hr audio',
    sizes: ['One Size'],
    in_stock: true
  },
  {
    id: 'AIRPODS-PRO-2',
    title: 'Apple AirPods Pro (2nd Generation) with MagSafe Case (USB-C)',
    brand: 'Apple',
    category: 'mobile-accessories',
    best_price: 24900,
    rating: 4.8,
    emoji: '🎧',
    image: 'https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20Airpods/thumbnail.png',
    search_text: 'apple airpods pro 2 2nd gen tws earbuds wireless noise cancelling anc ios',
    sizes: ['One Size'],
    in_stock: true
  },
  {
    id: 'BOSE-QC-ULTRA',
    title: 'Bose QuietComfort Ultra Wireless Headphones (Spatial Audio)',
    brand: 'Bose',
    category: 'mobile-accessories',
    best_price: 35900,
    rating: 4.7,
    emoji: '🎧',
    image: 'https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20AirPods%20Max%20Silver/thumbnail.png',
    search_text: 'bose quietcomfort ultra wireless anc noise cancelling headphones premium audio',
    sizes: ['One Size'],
    in_stock: true
  },
  {
    id: 'SONY-WF1000XM5',
    title: 'Sony WF-1000XM5 Truly Wireless Noise Cancelling Earbuds',
    brand: 'Sony',
    category: 'mobile-accessories',
    best_price: 19990,
    rating: 4.6,
    emoji: '🎧',
    image: 'https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20Airpods/thumbnail.png',
    search_text: 'sony wf-1000xm5 tws wireless noise cancelling earbuds long battery high res audio',
    sizes: ['One Size'],
    in_stock: true
  },
  {
    id: 'ONEPLUS-BUDS-PRO-2',
    title: 'OnePlus Buds Pro 2 TWS Earbuds (Dynaudio, Obsidian Black)',
    brand: 'OnePlus',
    category: 'mobile-accessories',
    best_price: 9999,
    rating: 4.4,
    emoji: '🎧',
    image: 'https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20Airpods/thumbnail.png',
    search_text: 'oneplus buds pro 2 tws wireless earbuds anc noise cancelling under 10k 10000',
    sizes: ['One Size'],
    in_stock: true
  },
  {
    id: 'BOAT-AIRDOPES-141',
    title: 'boAt Airdopes 141 Bluetooth Truly Wireless Earbuds (42H Playback)',
    brand: 'boAt',
    category: 'mobile-accessories',
    best_price: 1299,
    rating: 4.1,
    emoji: '🎧',
    image: 'https://cdn.dummyjson.com/products/images/mobile-accessories/Apple%20Airpods/thumbnail.png',
    search_text: 'boat airdopes 141 bluetooth tws wireless earbuds 42h battery fast charge cheap budget under 2000',
    sizes: ['One Size'],
    in_stock: true
  },

  // RUNNING SHOES
  {
    id: 'NIKE-PEGASUS-40',
    title: 'Nike Air Zoom Pegasus 40 Road Running Shoes (Black/White)',
    brand: 'Nike',
    category: 'mens-shoes',
    best_price: 11895,
    rating: 4.7,
    emoji: '🏃',
    image: 'https://cdn.dummyjson.com/products/images/mens-shoes/Nike%20Air%20Jordan%201%20Retro%20High%20Imperial%20Purple/thumbnail.png',
    search_text: 'nike air zoom pegasus 40 road daily running shoes mens cushion size 7 8 9 10',
    sizes: ['7', '8', '9', '10', '11'],
    in_stock: true
  },
  {
    id: 'ADIDAS-ULTRABOOST-LIGHT',
    title: 'Adidas Ultraboost Light Running Shoes (Core Black)',
    brand: 'Adidas',
    category: 'mens-shoes',
    best_price: 18999,
    rating: 4.8,
    emoji: '🏃',
    image: 'https://cdn.dummyjson.com/products/images/mens-shoes/Sports%20Sneakers%20Off%20White%20Red/thumbnail.png',
    search_text: 'adidas ultraboost light core black mens daily road running boost shoes cushion size 7 8 9 10',
    sizes: ['7', '8', '9', '10', '11'],
    in_stock: true
  },
  {
    id: 'ASICS-NIMBUS-26',
    title: 'Asics Gel-Nimbus 26 Max Cushioning Road Running Shoes',
    brand: 'Asics',
    category: 'mens-shoes',
    best_price: 15999,
    rating: 4.9,
    emoji: '🏃',
    image: 'https://cdn.dummyjson.com/products/images/mens-shoes/Sports%20Sneakers%20Off%20White%20Red/thumbnail.png',
    search_text: 'asics gel-nimbus 26 max cushion road running shoes marathon training size 7 8 9 10',
    sizes: ['7', '8', '9', '10'],
    in_stock: true
  },
  {
    id: 'PUMA-VELOCITY-NITRO-3',
    title: 'Puma Velocity Nitro 3 Running Shoes (Fire Orchid)',
    brand: 'Puma',
    category: 'mens-shoes',
    best_price: 8999,
    rating: 4.5,
    emoji: '🏃',
    image: 'https://cdn.dummyjson.com/products/images/mens-shoes/Sports%20Sneakers%20Off%20White%20Red/thumbnail.png',
    search_text: 'puma velocity nitro 3 road running shoes nitro foam light weight under 10000 8000 size 7 8 9',
    sizes: ['7', '8', '9', '10'],
    in_stock: true
  },
  {
    id: 'NIKE-REVOLUTION-6',
    title: 'Nike Revolution 6 Next Nature Road Running Shoes',
    brand: 'Nike',
    category: 'mens-shoes',
    best_price: 3695,
    rating: 4.3,
    emoji: '🏃',
    image: 'https://cdn.dummyjson.com/products/images/mens-shoes/Nike%20Air%20Jordan%201%20Retro%20High%20Imperial%20Purple/thumbnail.png',
    search_text: 'nike revolution 6 next nature mens road running shoes under 8000 5000 4000 size 7 8 9',
    sizes: ['7', '8', '9', '10'],
    in_stock: true
  },

  // SHIRTS & APPAREL
  {
    id: 'PETER-ENGLAND-FORMAL-SHIRT',
    title: "Peter England Men's Cotton Formal Shirt (Black, Size M)",
    brand: 'Peter England',
    category: 'mens-shirts',
    best_price: 1899,
    rating: 4.4,
    emoji: '👔',
    image: 'https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png',
    search_text: 'peter england mens black formal dress shirt cotton office work size M under 2500 2000',
    sizes: ['S', 'M', 'L', 'XL'],
    in_stock: true
  },
  {
    id: 'VAN-HEUSEN-SLIM-SHIRT',
    title: "Van Heusen Men's Slim Fit Cotton Dress Shirt (White, Size L)",
    brand: 'Van Heusen',
    category: 'mens-shirts',
    best_price: 2499,
    rating: 4.6,
    emoji: '👔',
    image: 'https://cdn.dummyjson.com/products/images/mens-shirts/Blue%20&%20Black%20Check%20Shirt/thumbnail.png',
    search_text: 'van heusen mens white slim fit formal dress shirt cotton office meeting size L under 2500',
    sizes: ['S', 'M', 'L', 'XL'],
    in_stock: true
  }
];

const RAW_CATALOG = CURATED_CATALOG;
const CATALOG = CURATED_CATALOG;

// ---- DEMO SCENARIOS ----
const SCENARIOS = [
  {
    id: 'iphones',
    query: 'Find iphones under 90k',
    description: 'Apple iPhones under ₹90,000',
    expectedMatch: true
  },
  {
    id: 'running_shoes',
    query: 'Find running shoes under ₹8,000, size 7, for daily road running',
    description: 'Daily road running shoes',
    expectedMatch: true
  },
  {
    id: 'ml_laptop',
    query: 'Find a laptop under ₹80,000 for Python and machine learning',
    description: 'ML development laptop',
    expectedMatch: true
  },
  {
    id: 'headphones',
    query: 'Find wireless headphones under ₹10,000 with excellent battery life',
    description: 'Long-battery wireless headphones',
    expectedMatch: true
  }
];

console.log(`CommerceOS Data Layer Loaded: ${CURATED_CATALOG.length} Rich Curated Products + DummyJSON Live API, ${Object.keys(MERCHANTS).length} merchants`);
</script>
'''

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'a') as f:
    content = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')).read()
    idx = content.rfind('</body>')
    new_content = content[:idx] + CATALOG_JS + '\n' + content[idx:]

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), 'w') as f:
    f.write(new_content)

print("Part 2 written: Rich Curated Catalog + Live API integration")
print(f"File size: {len(new_content):,} bytes")
