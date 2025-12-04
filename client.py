import os

class Client:
    def __init__(self, descriptor_path="channel.txt"):
        self.descriptor_path = descriptor_path
        if not os.path.exists(self.descriptor_path):
            with open(self.descriptor_path, 'w') as f:
                self.fd = f.fileno()
    
    def send_request(self, request_data):
        """Отправляет запрос серверу"""
    
    def wait_for_response(self, timeout=5):
        """Ожидает ответ от сервера"""
        print("Клиент: Ожидаю ответ от сервера")
        start_time = time.time()
        last_content = ""
        
        while time.time() - start_time < timeout:
            try:
                with open(self.descriptor_path, 'r') as f:
                    content = f.read().strip()
                    if content and content != last_content: 
                        print(f"Клиент: Получен ответ '{content}'")
                        return content
                time.sleep(0.1) 
            except Exception as e:
                result = self.handle_error(e)
                if result == "fatal":

    
    def get_response(self, response_data):
        """Обрабатывает ответ от сервера"""
    
    def handle_error(self, error):
        """Обрабатывает ошибки"""
    
    def run(self):
        """Основной цикл клиента"""
    

if __name__ == "__main__":
    client = Client()
    client.run()
