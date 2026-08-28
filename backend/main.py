from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import ecommerce_router
import uvicorn

app = FastAPI(
    title="E-Commerce Distributed Microservices API",
    description="Concurrency-locked inventory checkout and decoupled ordering pipeline.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ecommerce_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ecommerce-microservices"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
