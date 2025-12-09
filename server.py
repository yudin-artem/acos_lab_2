import time

class Server:
    def __init__(self, descriptor_path="channel.txt"):
        try:
            self.descriptor_path = descriptor_path
            self.file = open(self.descriptor_path, 'w+')
            self.timeout = 5
        except Exception as e:
            print(f"Сервер: ошибка инициализации: {e}")
            raise
    
    def get_request(self, request_data):
        """Обрабатывает запрос от клиента"""
        data = request_data.strip().lower()

        if data == "ping":
            return "pong"
        else:
            return self.handle_error(Exception(f"Сервер: Неожиданный запрос от клиента: {data}"))
        
    def send_response(self, response_data):
        """Отправляет ответ клиенту"""
        try:
            print(f"Сервер: Отправляю ответ клиенту '{response_data}'")
            self.clear_file()
            self.file.write(response_data)
            self.file.flush()  
            return "ok"
        except Exception as e:
            return self.handle_error(e)
    
    def handle_error(self, error):
        """Обрабатывает ошибки"""
        print(f"--- Сервер ОШИБКА: {type(error).__name__} ---")
        if isinstance(error, (IOError, OSError)):
            print(f"Ошибка ввода/вывода или IPC: {error}")
            print("------------------------------------------------")
            return "fatal"
        else:
            print(f"Непредвиденная ошибка: {error}")
            print("------------------------------------------------")
            return "retry"
    
    def wait_for_request(self, timeout):
        """Ожидает запрос от клиента"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.file.seek(0)
                content = self.file.read().strip().lower()
                if content and content != "":  
                    print(f"Сервер: Получен запрос '{content}'")
                    return content
                time.sleep(0.5)
            except Exception as e:
                return self.handle_error(e)
        return self.handle_error(TimeoutError("Сервер: Таймаут ожидания запроса"))

    def run(self):
        """Основной цикл сервера"""
        while True:
            req = self.wait_for_request(self.timeout)
            if req == "retry": 
                time.sleep(2)
                continue 
            elif req == "fatal": 
                print("Клиент: Завершение работы")
                break
            self.clear_file()

            resp = self.get_request(req)
            if resp == "fatal": 
                print("Сервер: Завершение работы")
                break
            elif resp == "retry": 
                time.sleep(2)
                continue

            res = self.send_response(resp)
            if res == "fatal":
                print("Сервер: Завершение работы")
                break
            elif res == "retry":
                time.sleep(2)
                continue

            time.sleep(2)

        self.file.close()

    def clear_file(self):
        self.file.seek(0)
        self.file.truncate(0)

if __name__ == "__main__":
    server = Server()
    server.run()
