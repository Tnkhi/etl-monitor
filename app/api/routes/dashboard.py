from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.config import get_db
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetOut
from pathlib import Path

router = APIRouter()

@router.get("/datasets", response_model=list[DatasetOut])
def list_datasets(db: Session = Depends(get_db)):
    datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).limit(20).all()
    return datasets

@router.get("/datasets/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    return dataset

@router.get("/dashboard/{dataset_id}", response_class=HTMLResponse)
def dashboard(dataset_id: str, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset introuvable")
    html = Path("app/templates/dashboard.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)