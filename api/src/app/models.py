from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FileMetadata(Base):
    __tablename__ = 'file_metadata'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_type = Column(String, nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)
    hadoop_path = Column(String, nullable=False)


class FileMetadataCreate(BaseModel):
    filename: str
    file_size: int
    file_type: str | None = None
