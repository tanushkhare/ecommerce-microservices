from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import store

app = FastAPI(
    title="E-Commerce Microservices Backend",
    version="1.0.0",
    description="Microservice backend for product inventory and order fulfillment."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(store.router)

@app.get("/")
def read_root():
    return {"message": "E-Commerce Microservices Backend is running!"}