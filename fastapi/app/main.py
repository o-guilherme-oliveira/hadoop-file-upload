from fastapi import FastAPI, UploadFile, HTTPException
from pywebhdfs.webhdfs import PyWebHdfsClient
import os

app = FastAPI()

# Configurações do cliente HDFS
hdfs_host = os.getenv("HADOOP_HOST", "hadoop")
hdfs_port = os.getenv("HADOOP_PORT", "9000")
hdfs = PyWebHdfsClient(host=hdfs_host, port=hdfs_port)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    file_data = await file.read()
    file_path = f"/{file.filename}"

    try:
        # Carregar o arquivo para o HDFS
        hdfs.create_file(file_path, file_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

    return {"message": f"Arquivo '{file.filename}' carregado com sucesso"}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"/{filename}"

    try:
        # Ler o arquivo do HDFS
        file_data = hdfs.read_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Arquivo não encontrado: {str(e)}")

    return {"filename": filename, "content": file_data.decode("utf-8")}
