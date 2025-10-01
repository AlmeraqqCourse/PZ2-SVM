import time
from datetime import datetime

class LoggingMixin:
    """Миксин для логирования событий игры"""
    
    def __init__(self):
        self.log_file = "game_log.txt"
    
    def log_event(self, event):
        """Логирует событие с временной меткой"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event}\n"
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"📝 {event}")

class GameSessionManager:
    """Контекстный менеджер для игровой сессии"""
    
    def __enter__(self):
        self.start_time = time.time()
        print("🎮 Начало игровой сессии...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"⏰ Игровая сессия завершена. Продолжительность: {duration:.2f} секунд")
        
        if exc_type:
            print(f"⚠️ Произошла ошибка: {exc_val}")
        
        return False  # Не подавляем исключения