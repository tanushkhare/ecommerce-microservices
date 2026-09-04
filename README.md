# ⚡ E-Commerce Microservices

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://ecommerce-microservices-web.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://ecommerce-microservices-web.vercel.app](https://ecommerce-microservices-web.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
High-concurrency checkout and order dispatch engine protected by per-product `asyncio.Lock` mutexes and atomic SQL inventory decrements to prevent overselling.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** FastAPI, AsyncIO Mutex, PostgreSQL, Pydantic
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Mutex Serialization:** Scopes locks per product ID to resolve TOCTOU race conditions under parallel requests.
* **Atomic Mutation:** Enforces `UPDATE inventory SET stock = stock - qty WHERE stock >= qty`.
* **Concurrency Tested:** Verified against 50-thread concurrent stress suites with zero oversell events.

---

## 🚀 API Contracts
```http
POST /api/v1/orders/checkout
Request:
{
  "product_id": "PROD-01",
  "quantity": 1
}

Response (200 OK):
{
  "order_id": "ORD-94281",
  "status": "CONFIRMED",
  "remaining_stock": 11,
  "mutex_latency_ms": 1.1
}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart

Bash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v