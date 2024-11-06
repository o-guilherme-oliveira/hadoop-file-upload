from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from . import models, database, crud, hadoop_utils
from hdfs.util import HdfsError
import io

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        file_size = len(content)

        hadoop_path = hadoop_utils.upload_to_hadoop(content, file.filename)
        file_data = models.FileMetadataCreate(
            filename=file.filename,
            file_size=file_size,
            file_type=file.content_type
        )

        db_file = crud.create_file_metadata(db, file_data, hadoop_path)
        return {"file_id": db_file.id, "hadoop_path": hadoop_path}

    except HdfsError as e:
        raise HTTPException(status_code=500, detail=f"Erro no HDFS: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro interno do servidor: {str(e)}")


@app.get("/files/{file_id}")
async def get_file(file_id: int, db: Session = Depends(get_db)):
    file_metadata = crud.get_file_metadata(db, file_id)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        file_content = hadoop_utils.download_from_hadoop(
            file_metadata.hadoop_path)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Error retrieving file from Hadoop")

    file_like = io.BytesIO(file_content)
    return StreamingResponse(file_like, media_type="application/octet-stream", headers={
        "Content-Disposition": f"attachment; filename={file_metadata.filename}"
    })


@app.get("/ping/")
async def ping():
    return "pong"
