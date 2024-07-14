import os
import json

class FileWorker:
    def __init__(self, filename):
        self.filename = filename

    def write_json(self, data):
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        # Записываем данные в JSON файл
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def read_json(self):
        # Читаем данные из JSON файла, если он существует
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data