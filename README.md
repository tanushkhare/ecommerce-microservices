# ⚡ E-Commerce Microservices

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://ecommerce-microservices-web.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://ecommerce-microservices-web.vercel.app](https://ecommerce-microservices-web.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
High-concurrency order dispatch service protected by per-product asyncio.Lock mutexes and atomic inventory decrements.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** FastAPI, AsyncIO Mutex, PostgreSQL
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🚀 API Contracts
```http
POST /api/v1/orders/checkout
GET /health
```

---

## 💻 Local Quickstart
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v
```
