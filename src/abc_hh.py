from abc import ABC, abstractmethod


class AbstractHH(ABC):
    """
    Абстрактный класс для работы с API HeadHunter.

    Атрибуты:
    ----------
    file_worker : FileWorker
        Экземпляр класса FileWorker для работы с файлами.
    """

    def __init__(self, file_worker):
        self.file_worker = file_worker

    @abstractmethod
    def load_vacancies(self, keyword):
        # Загружает вакансии по ключевому слову
        pass

    @abstractmethod
    def save_vacancies(self):
        # Сохраняет загруженные вакансии в файл
        pass

    @abstractmethod
    def get_vacancies(self, keyword, salary=None):
        # Получает вакансии по ключевому слову и зарплате
        pass

    @abstractmethod
    def filter_vacancies(self, salary=None):
        # Фильтрует вакансии по указанной зарплате
        pass

    @abstractmethod
    def check_salary(self, vacancy, min_salary, max_salary):
        # Проверяет соответствие зарплаты вакансии указанному диапазону
        pass