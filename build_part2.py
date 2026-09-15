#!/usr/bin/env python3
"""Build Part 2: Product catalog, merchants, scenarios, and rich real-world catalog"""

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

with open('/Users/shivanshinigam/.gemini/antigravity-ide/scratch/commerceos/index.html', 'a') as f:
    content = open('/Users/shivanshinigam/.gemini/antigravity-ide/scratch/commerceos/index.html').read()
    idx = content.rfind('</body>')
    new_content = content[:idx] + CATALOG_JS + '\n' + content[idx:]

with open('/Users/shivanshinigam/.gemini/antigravity-ide/scratch/commerceos/index.html', 'w') as f:
    f.write(new_content)

print("Part 2 written: Rich Curated Catalog + Live API integration")
print(f"File size: {len(new_content):,} bytes")
