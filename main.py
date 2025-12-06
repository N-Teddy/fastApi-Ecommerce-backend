from fastapi import FastAPI
from src.middleware.timing_middleware import TimingMiddleware
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(tite="E-Commerce", version="1.0.0")

app.add_middleware(TimingMiddleware)

@app.get("/")
def home():
    return {"message": "Hello Teddy! FastAPI is running 🚀"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)