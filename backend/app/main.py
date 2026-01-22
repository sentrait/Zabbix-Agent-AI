from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(title="Zabbix AI Agent API")

# CORS
origins = [
    "http://localhost:5173", # Vite Dev Server
    "http://localhost:80",
    "http://localhost",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Zabbix AI Agent API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Mount static files (Frontend build)
# We will create this directory later
if os.path.exists("static"):
    app.mount("/app", StaticFiles(directory="static", html=True), name="static")

from .api.routes import router as api_router
from .api.summary import router as summary_router
from .api.settings import router as settings_router
app.include_router(api_router, prefix="/api")
app.include_router(summary_router, prefix="/api")
app.include_router(settings_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
