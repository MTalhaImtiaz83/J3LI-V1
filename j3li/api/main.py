from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from j3li.graph.client import graph_client

app = FastAPI(title="J3LI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "cloud-ready"}

@app.get("/api/v1/status")
async def get_status():
    try:
        # Simple query to test graph connection
        graph_client.query("RETURN 1 AS status")
        return {"status": "online", "graph": "connected"}
    except Exception as e:
        return {"status": "online", "graph": "error", "message": str(e)}