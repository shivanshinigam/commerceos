# CommerceOS — Autonomous AI Commerce Agent & Google UCP Protocol Lab

> **"An interactive laboratory and server implementation for AI-native agentic commerce."**

[![Live Demo on Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Space-blue?style=for-the-badge)](https://huggingface.co/spaces/ShivanshiNigam/commerceos)
[![Google UCP](https://img.shields.io/badge/Google%20UCP-v2026--04--08-7c3aed?style=for-the-badge)](https://developers.google.com/merchant/ucp)
[![FastAPI Backend](https://img.shields.io/badge/Backend-FastAPI%20%2B%20SQLite-10b981?style=for-the-badge)](#backend-server)

---

## 📸 Visual Showcase

### 1. Main Agentic Commerce Interface (`Try It Live`)
Natural language intent extraction, 6-dimensional candidate ranking, real-time AI Brain execution trace, and mobile buying simulator.

![CommerceOS Main UI](https://raw.githubusercontent.com/shivanshinigam/commerceos/main/docs/images/main_demo.png)

---

### 2. Dual Smartphone Payment & Checkout Simulation
Watch Gemini AI discover inventory via UCP endpoints, request session locks, and complete settlement via Google Pay tokens in real-time.

![UCP Phone Simulation](https://raw.githubusercontent.com/shivanshinigam/commerceos/main/docs/images/ucp_phone_simulation.png)

---

### 3. Google UCP Protocol Explorer & Live Payload Inspector
Inspect raw UCP JSON payloads (`GET /.well-known/ucp`, `POST /checkout-sessions`), capability negotiation profiles, and API specifications.

![UCP Explorer Spec](https://raw.githubusercontent.com/shivanshinigam/commerceos/main/docs/images/ucp_explorer_spec.png)

---

### 4. Architecture & Component Topology
Full system component interaction map linking AI intent parsing, multi-constraint boundary filtering, and merchant API connectors.

![Architecture Topology](https://raw.githubusercontent.com/shivanshinigam/commerceos/main/docs/images/architecture_topology.png)

---

## 🌟 What is CommerceOS?

CommerceOS is a production-grade demonstration and implementation of agentic commerce built on Google's **Universal Commerce Protocol (UCP v2026-04-08)** standard. It enables LLMs (such as Gemini) to execute transactions directly with merchants without leaving the conversational interface.

### Key Capabilities:
1. **Natural Language Intent Parsing**: Extracts budget boundaries (e.g. ₹10k, ₹80k, ₹5L), brand constraints, and product specs.
2. **Multi-Constraint Filtering & 6D Ranking**: Evaluates candidates across Requirement Overlap, Budget Fit, Suitability, Stock, Rating, and Delivery Speed.
3. **Google UCP Direct Buying Execution**: Follows Google's protocol pipeline:
   - `GET /.well-known/ucp` — Discovery & Merchant Capability Negotiation
   - `POST /checkout-sessions` — Session Locking & Tax/Shipping calculation
   - `POST /pay` — Direct Settlement via Google Pay Tokens
4. **Dual Mobile & Observability Suite**: Real-time side-by-side execution trace for shoppers and developers.

> **Notice**: Operating on a simulated demonstration catalog dataset and live DummyJSON API endpoints for educational & protocol demonstration.

---

## 🛠 Project Structure

```
commerceos/
├── index.html                 # Single-page web application (compiled shell)
├── build_part1_v2.py          # Core UI & Main Page builder
├── build_part2.py             # Product Catalog & DummyJSON API connector
├── build_part3.py             # AI Agent Pipeline Engine & 6D Ranking
├── build_part4_v2.py          # Mobile Phone Payment Controller
├── build_part5_v2.py          # Navigation Tabs & UCP Protocol Explorer
├── deploy.py                  # Automatic deployment script to Hugging Face
├── docs/images/               # UI screenshots & architectural diagrams
└── ucp_server/                # Production Python FastAPI UCP Backend Server
    ├── main.py                # FastAPI entry point
    ├── database.py            # SQLAlchemy SQLite ORM & tables
    ├── models.py              # Pydantic schemas for UCP payloads
    └── test_ucp_api.py        # Automated Pytest suite
```

---

## 🚀 Running the Production Python UCP Server

CommerceOS includes a standalone, production-ready Python FastAPI server for local development and backend integration testing:

```bash
# Navigate to UCP Server directory
cd ucp_server

# Install Python dependencies
pip install -r requirements.txt

# Launch FastAPI Server
python3 -m uvicorn main:app --reload --port 8000
```

### Verified Endpoints:
- `GET http://127.0.0.1:8000/.well-known/ucp` — Google UCP Discovery JSON
- `POST http://127.0.0.1:8000/ucp/v1/checkout-sessions` — Session creation
- `POST http://127.0.0.1:8000/ucp/v1/pay` — Google Pay token settlement

---

## 📊 Ranking Algorithm Breakdown

| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Requirement Overlap** | 30% | Category, brand, and feature keyword matching |
| **Budget Adherence** | 20% | Penalty curve for exceeding budget limits |
| **Use-Case Suitability** | 20% | Alignment with target activity (e.g. ML, Running) |
| **Stock Availability** | 10% | Real-time merchant inventory verification |
| **Rating Score** | 10% | Verified customer review score weighting |
| **Delivery Speed** | 10% | Fulfillment timeframe preference |

---

## 🔗 Links & Resources

* **Live Interactive Space**: [https://huggingface.co/spaces/ShivanshiNigam/commerceos](https://huggingface.co/spaces/ShivanshiNigam/commerceos)
* **Official Google UCP Specification**: [developers.google.com/merchant/ucp](https://developers.google.com/merchant/ucp)

---

*Built with ❤ by **Shivanshi Nigam** — Agentic Commerce & AI Engineering.*
