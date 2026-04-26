from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.dataset import DatasetStatus

class DatasetOut(BaseModel):
    id: str
    filename: str
    sector: Optional[str] = None
    status: DatasetStatus
    rows_count: Optional[int] = None
    columns_count: Optional[int] = None
    kpis: Optional[dict] = None
    charts: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True