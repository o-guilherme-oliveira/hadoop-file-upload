from swiftclient import client
from swiftclient.exceptions import ClientException

auth_url = "http://localhost:8080/auth/v1.0"
username = "test:tester"
password = "testing"
container_name = "mycontainer"
object_name = "local_upload.txt"
file_path = object_name

print(f"Autenticando...")
swift = client.Connection(authurl=auth_url, user=username, key=password, auth_version="1")

try:
    swift.head_container(container_name)
    print(f"O container '{container_name}' já existe.")
except ClientException as e:
    if e.http_status == 404:
        print(f"O container '{container_name}' não existe. Criando...")
        swift.put_container(container_name)
    else:
        raise e

with open(file_path, 'rb') as file_data:
    swift.put_object(container_name, object_name, contents=file_data, content_type='text/plain')
    print("Arquivo armazenado com sucesso!")

obj_tuple = swift.get_object(container_name, object_name)
with open("downloaded_example.txt", "wb") as downloaded_file:
    downloaded_file.write(obj_tuple[1])
    print("Arquivo recuperado com sucesso!")
