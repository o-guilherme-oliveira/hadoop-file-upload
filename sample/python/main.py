import boto3
from botocore.client import Config


minio_url = "http://localhost:9000"
access_key = "minioadmin"
secret_key = "minioadmin"
bucket_name = "upload"


s3_client = boto3.client(
    's3',
    endpoint_url=minio_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    config=Config(signature_version='s3v4')
)


def upload_file(file_path, object_name):
    s3_client.upload_file(file_path, bucket_name, object_name)
    print(
        f"Arquivo '{object_name}' carregado com sucesso no bucket '{bucket_name}'.")


def download_file(object_name, download_path):
    s3_client.download_file(bucket_name, object_name, download_path)
    print(
        f"Arquivo '{object_name}' baixado com sucesso para '{download_path}'.")


upload_file("local_upload.txt", "uploaded_file.txt")
download_file("uploaded_file.txt", "local_download.txt")
