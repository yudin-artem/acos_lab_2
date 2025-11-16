from server import Server
from client import Client

if __name__ == "__main__":
    file_path = input("Введите путь до желаемого файла(оставьте пустым если хотите использовать стандартный): ")
    if file_path == "":
        server, client = Server(), Client()
    else:
        server, client = Server(descriptor_path=file_path), Client(descriptor_path=file_path)
    server.run()
    client.run()
