class Parser:
    def __init__(self, file_worker):
        self.file_worker = file_worker

    def save_data(self, data):
        # Сохраняем данные с помощью FileWorker
        self.file_worker.write_json(data)
