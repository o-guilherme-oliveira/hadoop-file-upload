from hdfs import InsecureClient

HADOOP_URL = "http://localhost:9864"
client = InsecureClient(HADOOP_URL, user="hadoop_user")


def upload_to_hadoop(file, filename):
    hadoop_path = f"/uploads/{filename}"
    client.write(hadoop_path, file, overwrite=True)
    return hadoop_path


def download_from_hadoop(hadoop_path: str):
    with client.read(hadoop_path) as file:
        return file.read()


def main():
    with open("main.py", "r") as file:
        upload_to_hadoop(file, "teste.txt")


main()
