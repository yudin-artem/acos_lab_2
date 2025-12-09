from server import Server
from client import Client
from threading import Thread

if __name__ == "__main__":
    file_path = input("Введите путь до желаемого файла(оставьте пустым если хотите использовать стандартный): ")
    if file_path == "":
        server, client = Server(), Client()
    else:
        server, client = Server(descriptor_path=file_path), Client(descriptor_path=file_path)
    
    tr_1 = Thread(target = server.run)  
    tr_2 = Thread(target = client.run)

    tr_1.start()
    tr_2.start()

    tr_1.join()
    tr_2.join()