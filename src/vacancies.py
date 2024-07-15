from src.file_worker import FileWorker
from src.hhru import HH

class Vacancy:
    def __init__(self, vacancy_data):
        self.name = vacancy_data.get('name', 'Не указано')
        self.employer = vacancy_data.get('employer', {}).get('name', 'Не указан')
        self.salary_info = vacancy_data.get('salary', {})
        self.url = vacancy_data.get('alternate_url', 'Не указана')

    def format_salary(self):
        salary_from = self.salary_info.get('from')
        salary_to = self.salary_info.get('to')
        currency = self.salary_info.get('currency', 'Не указана')

        if salary_from and salary_to:
            return f"от {salary_from} до {salary_to} {currency}"
        elif salary_from:
            return f"от {salary_from} {currency}"
        elif salary_to:
            return f"до {salary_to} {currency}"
        else:
            return 'Не указана'

    def __str__(self):
        return (
            f"Название: {self.name}\n"
            f"Работодатель: {self.employer}\n"
            f"Зарплата: {self.format_salary()}\n"
            f"Ссылка: {self.url}\n"
            "---------------------"
        )

    def get_max_salary(self):
        salary_from = self.salary_info.get('from') or 0
        salary_to = self.salary_info.get('to') or 0
        return max(salary_from, salary_to)

    def __lt__(self, other):
        return self.get_max_salary() < other.get_max_salary()


class Vacancies:
    """
    Класс для работы с вакансиями.

    Атрибуты:
    filename : str
        Имя файла для сохранения вакансий
    file_worker : FileWorker
        Объект для работы с файлами
    hh : HH
        Объект для работы с API HeadHunter
    items : list
        Список вакансий
    """

    def __init__(self, filename='data/vacancies.json'):
        self.file_worker = FileWorker(filename)
        self.hh = HH(self.file_worker)
        self.items = []

    def load_vacancies(self, keyword, salary=None):
        # загружает вакансии по ключевому слову и фильтрует по зарплате
        if salary:
            print(f"\nЗапрос: {keyword}, Зарплата: {salary}")
        else:
            print(f"\nЗапрос: {keyword}")

        vacancies_data = self.hh.get_vacancies(keyword, salary)
        self.items = [Vacancy(vacancy) for vacancy in vacancies_data]
        self.save_vacancies()  # Сохраняем вакансии в файл
        print(f"Найдено вакансий: {len(self.items)}")

    def save_vacancies(self):
        # сохраняем вакансии
        self.file_worker.write_json([vars(vacancy) for vacancy in self.items])

    def limit_advertisements(self, advertisements):
        # количество вакансий для вывода
        if advertisements:
            self.items.sort(reverse=True)
            self.items = self.items[:advertisements]

    def __str__(self):
        return "\n".join(str(vacancy) for vacancy in self.items)
