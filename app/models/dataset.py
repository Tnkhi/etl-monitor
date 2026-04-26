from sqlalchemy import Column, String, DateTime, JSON, Enum, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class DatasetStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    sector = Column(String, nullable=True)
    status = Column(Enum(DatasetStatus), default=DatasetStatus.PENDING)
    rows_count = Column(Integer, nullable=True)
    columns_count = Column(Integer, nullable=True)
    kpis = Column(JSON, nullable=True)
    charts = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)