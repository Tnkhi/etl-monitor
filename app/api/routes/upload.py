import uuid
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config import get_db, engine
from app.models.dataset import Dataset, DatasetStatus, Base
from app.schemas.dataset import DatasetOut
from app.core.pipeline import run_pipeline

Base.metadata.create_all(bind=engine)

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xls", ".xlsx", ".json"}
MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/upload", response_model=DatasetOut)
async def upload_dataset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail=f"Format '{ext}' non supporté.")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Fichier trop volumineux. Maximum 10 MB.")

    dataset_id = str(uuid.uuid4())
    dataset = Dataset(
        id=dataset_id,
        filename=file.filename,
        status=DatasetStatus.PENDING
    )
    db.add(dataset)
    db.commit()

    raw_path = os.path.join(UPLOAD_DIR, f"{dataset_id}{ext}")
    with open(raw_path, "wb") as f:
        f.write(contents)

    try:
        dataset.status = DatasetStatus.PROCESSING
        db.commit()

        result = run_pipeline(raw_path)

        dataset.status = DatasetStatus.DONE
        dataset.sector = result["sector"]
        dataset.rows_count = result["rows_count"]
        dataset.columns_count = result["columns_count"]
        dataset.kpis = result["kpis"]
        dataset.charts = result["charts"]
        db.commit()

    except Exception as e:
        dataset.status = DatasetStatus.FAILED
        dataset.error = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

    db.refresh(dataset)
    return dataset