import os

class Server:
    def __init__(self, descriptor_path="channel.txt"):
        self.descriptor_path = descriptor_path
        if not os.path.exists(self.descriptor_path):
            with open(self.descriptor_path, 'w') as f:
                self.fd = f.fileno()
    
    def get_request(self, request_data):
        """Обрабатывает запрос от клиента"""
        if not request_data:
            return None
        data = request_data.strip()

        if data == "Ping":
            return "Pong"
        else:
            return f"Server response to {data}"
        
    def send_response(self, response_data):
        """Отправляет ответ клиенту"""
        try:
            with open(self.descriptor_path, 'w') as f:
                f.write(response_data)
                f.flush()  
            return True
        except Exception as e:
            self.handle_error(e)
            return False
    
    def handle_error(self, error):
        """Обрабатывает ошибки"""
    
    def wait_for_request(self):
        """Ожидает запрос от клиента"""
        print("Сервер: Ожидание запрос от клиента")
        start_time = time.time()
        last_content = ""
        while time.time() - start_time < timeout:
            try:
                with open(self.descriptor_path, 'r') as f:
                    content = f.read().strip()
                    if content and content != last_content:  
                        print(f"Сервер: Получен запрос '{content}'")
                        return content
                time.sleep(0.1)  
            except Exception as e:
                result = self.handle_error(e)
                if result == "fatal":
                    raise e
        raise TimeoutError("Сервер: Таймаут ожидания запроса")

    def run(self):
        """Основной цикл сервера"""

if __name__ == "__main__":
    server = Server()
    server.run()
