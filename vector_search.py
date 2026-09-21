#!/usr/bin/env python3
"""
Vector Search Engine for CommerceOS & GenAI Product Recommender
Computes semantic vector embeddings and cosine similarity scores
for natural language query matching over catalog items.
"""

import json
import os
import math
from collections import Counter

class VectorSearchEngine:
    def __init__(self, catalog_path=None):
        if catalog_path is None:
            catalog_path = os.path.join(os.path.dirname(__file__), 'catalog.json')
        self.catalog_path = catalog_path
        self.products = []
        self.vocabulary = set()
        self.idf = {}
        self.product_vectors = []
        self.load_catalog()

    def tokenize(self, text):
        if not text:
            return []
        text = str(text).lower()
        # Extract alphanumeric words
        words = []
        word = ""
        for ch in text:
            if ch.isalnum():
                word += ch
            else:
                if len(word) > 1:
                    words.append(word)
                word = ""
        if len(word) > 1:
            words.append(word)
        return words

    def load_catalog(self):
        if not os.path.exists(self.catalog_path):
            return
        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            self.products = json.load(f)

        # Build vocabulary & document frequency
        df = Counter()
        doc_tokens = []
        num_docs = len(self.products)

        for prod in self.products:
            search_str = f"{prod.get('title', '')} {prod.get('brand', '')} {prod.get('category', '')} {prod.get('color', '')} {prod.get('style', '')} {prod.get('size', '')} {prod.get('description', '')}"
            tokens = set(self.tokenize(search_str))
            doc_tokens.append(self.tokenize(search_str))
            for t in tokens:
                df[t] += 1
                self.vocabulary.add(t)

        # Compute IDF
        for term, freq in df.items():
            self.idf[term] = math.log((num_docs + 1) / (freq + 1)) + 1.0

        # Build TF-IDF vectors for products
        for tokens in doc_tokens:
            tf = Counter(tokens)
            total = len(tokens) if len(tokens) > 0 else 1
            vec = {}
            norm_sq = 0.0
            for term, count in tf.items():
                tfidf = (count / total) * self.idf.get(term, 1.0)
                vec[term] = tfidf
                norm_sq += tfidf * tfidf
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            # Normalize vector
            for term in vec:
                vec[term] /= norm
            self.product_vectors.append(vec)

    def query_vector(self, query_str):
        tokens = self.tokenize(query_str)
        tf = Counter(tokens)
        total = len(tokens) if len(tokens) > 0 else 1
        vec = {}
        norm_sq = 0.0
        for term, count in tf.items():
            if term in self.vocabulary:
                tfidf = (count / total) * self.idf.get(term, 1.0)
                vec[term] = tfidf
                norm_sq += tfidf * tfidf
        norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
        for term in vec:
            vec[term] /= norm
        return vec

    def cosine_similarity(self, vec1, vec2):
        score = 0.0
        for term, val1 in vec1.items():
            if term in vec2:
                score += val1 * vec2[term]
        return score

    def search(self, query, top_k=10):
        q_vec = self.query_vector(query)
        results = []
        for idx, p_vec in enumerate(self.product_vectors):
            sim = self.cosine_similarity(q_vec, p_vec)
            if sim > 0.01:
                prod = self.products[idx]
                results.append({
                    "product": prod,
                    "vector_similarity": round(float(sim), 4)
                })

        results.sort(key=lambda x: x["vector_similarity"], reverse=True)
        return results[:top_k]

if __name__ == '__main__':
    engine = VectorSearchEngine()
    test_query = "Wrangler blue shirt for kids"
    matches = engine.search(test_query, top_k=3)
    print(f"Vector Similarity Search Results for '{test_query}':")
    for m in matches:
        p = m['product']
        print(f" - [{m['vector_similarity']:.4f}] {p['title']} (₹{p['best_price']})")
