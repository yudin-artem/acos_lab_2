import os
import time

class Client:
    def __init__(self, descriptor_path="channel.txt"):
        try:
            self.descriptor_path = descriptor_path
            self.file = open(self.descriptor_path, 'a+')
            self.timeout = 15
            self.attempted_fix = False
        except Exception as e:
            print(f"client: error initiallization: {e}")
            raise
    
    def send_request(self, request_data):
        """Отправляет запрос серверу"""
        try:
            print(f"client: send request '{request_data}'")
            self.clear_file()
            self.file.write(str(request_data))
            self.file.flush()
            return 'ok'
        except Exception as e:
            return self.handle_error(e)
    
    def wait_for_response(self, timeout):
        """Ожидает ответ от сервера"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                self.file.seek(0)
                content = self.file.read().strip().lower()
                if content and content != "": 
                    print(f"client: get response '{content}'")
                    return content
                time.sleep(0.5) 
            except Exception as e:
                return self.handle_error(e)
        return self.handle_error(TimeoutError("client: timeout"))
    
    def get_response(self, response_data):
        """Обрабатывает ответ от сервера"""
        if response_data == "pong":
            print(f"success!\n")
            return "ok"
        elif response_data is None:
            return self.handle_error(TimeoutError("client: timeput"))
        else:
            return self.handle_error(Exception(f"unexpected response: {response_data}"))
    
    def handle_error(self, error):
        """Обрабатывает ошибки"""
        print(f"error: {type(error).__name__} - {error}")
    
        if self.attempted_fix:
            print("error. stoping client.")
            return "fatal"
    
        error_type = type(error).__name__
        
        if error_type == 'FileNotFoundError':
            print("attempt to create file.")
            try:
                self.file = open(self.descriptor_path, 'w+')
                print("file created.")
                self.attempted_fix = True
                return "retry"
            except Exception as e:
                print(f"file can not be created: {e}")
                return "fatal"
        
        elif error_type == 'PermissionError':
            print("access deny. retrying.")
            try:
                if os.path.exists(self.descriptor_path):
                    self.file.close()
                    os.remove(self.descriptor_path)
                self.file = open(self.descriptor_path, 'a+')
                print("success.")
                self.attempted_fix = True
                return "retry"
            except Exception as e:
                print(f"unsuccess: {e}")
                return "fatal"
        print("fatal error. stoping client.")
        return "fatal"
        
    def run(self):
        """Основной цикл клиента"""
        print("Клиент работает")
        while True:
            req = input("enter request: ")
            if req == "" or req == "retry":
                print("unexpected request!\n")
                continue
            res = self.send_request(req)
            if res == "retry": 
                continue 
            if res == "fatal": 
                print("client: client shutown")
                break

            time.sleep(0.5)
            resp = self.wait_for_response(self.timeout)
            if resp == "retry": 
                continue 
            if resp == "fatal": 
                print("client: client shutown")
                break
            self.clear_file()

            res = self.get_response(resp)
            if res == "retry":
                continue
            if res == "fatal":
                print("client: client shutown")
                break

        self.file.close()

    def clear_file(self):
        self.file.seek(0)
        self.file.truncate(0)
    

if __name__ == "__main__":
    client = Client()
    client.run()
