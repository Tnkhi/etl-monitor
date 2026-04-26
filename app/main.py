from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.api.routes import upload, dashboard
from pathlib import Path

app = FastAPI(
    title="ETL Monitor",
    description="Pipeline ETL avec dashboard de KPIs automatique.",
    version="1.0.0"
)

app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])

@app.get("/", response_class=HTMLResponse)
async def home():
    html = Path("app/templates/index.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)