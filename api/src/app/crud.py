from sqlalchemy.orm import Session
from . import models


def create_file_metadata(db: Session, file_data: models.FileMetadataCreate, hadoop_path: str):
    db_file = models.FileMetadata(
        filename=file_data.filename,
        file_size=file_data.file_size,
        file_type=file_data.file_type,
        hadoop_path=hadoop_path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_file_metadata(db: Session, file_id: int):
    return db.query(models.FileMetadata).filter(models.FileMetadata.id == file_id).first()
