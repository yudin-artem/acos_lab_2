import time

class Server:
    def __init__(self, descriptor_path="channel.txt"):
        try:
            self.descriptor_path = descriptor_path
            self.file = open(self.descriptor_path, 'w+')
            self.timeout = 15
        except Exception as e:
            print(f"server: initialization error : {e}")
            raise
    
    def get_request(self, request_data):
        """Обрабатывает запрос от клиента"""
        data = request_data.strip().lower()

        if data == "ping":
            return "pong"
        else:
            return self.handle_error(Exception("unexpected client request"))
        
    def send_response(self, response_data):
        """Отправляет ответ клиенту"""
        try:
            print(f"server: send response '{response_data}'")
            self.clear_file()
            self.file.write(response_data)
            self.file.flush()  
            return "ok"
        except Exception as e:
            return self.handle_error(e)
    
    def handle_error(self, error):
        """Обрабатывает ошибки"""
        print(f"--- server error: {type(error).__name__} ---")
        if isinstance(error, (IOError, OSError)):
            print(f"IO error: {error}")
            print("------------------------------------------------")
            return "fatal"
        else:
            print(f"unexpected error: {error}")
            print("------------------------------------------------")
            return "retry"
    
    def wait_for_request(self, timeout):
        """Ожидает запрос от клиента"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.file.seek(0)
                content = self.file.read().strip().lower()
                if content and content != "" and content != "retry":  
                    print(f"server: get request '{content}'")
                    return content
                time.sleep(0.5)
            except Exception as e:
                return self.handle_error(e)
        return self.handle_error(TimeoutError("server: timeout"))

    def run(self):
        """Основной цикл сервера"""
        print("server in progress")
        while True:
            req = self.wait_for_request(self.timeout)
            if req == "retry": 
                continue 
            elif req == "fatal": 
                print("server: server shutdown")
                break
            self.clear_file()

            resp = self.get_request(req)
            if resp == "fatal": 
                print("server: server shutdown")
                break

            res = self.send_response(resp)
            if res == "fatal":
                print("server: server shutdown")
                break
            elif res == "retry":
                continue

            time.sleep(0.5)

        self.file.close()

    def clear_file(self):
        self.file.seek(0)
        self.file.truncate(0)

if __name__ == "__main__":
    server = Server()
    server.run()
