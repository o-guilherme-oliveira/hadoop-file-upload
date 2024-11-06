from hdfs import InsecureClient
import os

HADOOP_URL = os.getenv("HADOOP_URL")
client = InsecureClient(HADOOP_URL, user="hadoop_user")


def upload_to_hadoop(file, filename):
    hadoop_path = f"/uploads/{filename}"
    client.write(hadoop_path, file, overwrite=True)
    return hadoop_path


def download_from_hadoop(hadoop_path: str):
    with client.read(hadoop_path) as file:
        return file.read()
