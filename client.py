import os
import time

class Client:
    def __init__(self, descriptor_path="channel.txt"):
        self.descriptor_path = descriptor_path
        if not os.path.exists(self.descriptor_path):
            with open(self.descriptor_path, 'w') as f:
                self.fd = f.fileno()
    
    def send_request(self, request_data):
        """Отправляет запрос серверу"""
        try:
            with open(self.descriptor_path, 'w') as f:
                f.write(str(request_data))
        except Exception as e:
            self.handle_error(e)
    
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
        if response_data == "pong":
            print(f"LOG: Успех! Сервер подтвердил связь.")
            return True
        elif response_data is None:
            print("LOG: Ошибка. Ответ не получен (Timeout).")
            return False
        else:
            print(f"LOG: Ошибка протокола. Получено: {response_data}")
            return False
    
    def handle_error(self, error):
        """Обрабатывает ошибки"""
        print(f"Ошибка: {type(error).__name__} - {error}")
    
        if hasattr(self, '_attempted_fix') and self._attempted_fix:
            print("Уже была попытка исправления. Работа завершена.")
            return "fatal"
    
        error_type = type(error).__name__
        
        if error_type == 'FileNotFoundError':
            print("Попытка создать файл.")
            try:
                with open(self.descriptor_path, 'w') as f:
                    pass
                print("Файл создан.")
                self._attempted_fix = True
                return "retry"
            except Exception as e:
                print(f"Не удалось создать файл: {e}")
                return "fatal"
        
        elif error_type == 'TimeoutError':
            print("Сервер не отвечает. Ожидание 5 секунд.")
            time.sleep(5)
            self._attempted_fix = True
            return "retry"
        
        elif error_type == 'PermissionError':
            print("Возникла проблема доступа. Попытка восстановить.")
            try:
                if os.path.exists(self.descriptor_path):
                    os.remove(self.descriptor_path)
                with open(self.descriptor_path, 'w') as f:
                    pass
                print("Доступ восстановлен.")
                self._attempted_fix = True
                return "retry"
            except Exception as e:
                print(f"Не удалось восстановить доступ: {e}")
                return "fatal"
        print("Критическая ошибка. Работа завершена.")
        return "fatal"
        
    def run(self):
        """Основной цикл клиента"""
    

if __name__ == "__main__":
    client = Client()
    client.run()
