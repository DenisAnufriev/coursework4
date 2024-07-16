from src.file_worker import FileWorker
from src.parser import HH
from src.abc_methods import MethodsAbc

class Vacancy:
    def __init__(self, vacancy_data):
        self.name = vacancy_data.get('name', 'Не указано')
        self.employer = vacancy_data.get('employer', {}).get('name', 'Не указан')
        self.salary_info = vacancy_data.get('salary', {})
        self.url = vacancy_data.get('alternate_url', 'Не указана')

    def format_salary(self):
        if self.salary_info is None:
            return 'Зарплата не указана'

        salary_from = self.salary_info.get('from')
        salary_to = self.salary_info.get('to')
        currency = self.salary_info.get('currency', 'Не указана')

        if salary_from is not None and salary_to is not None:
            return f"от {salary_from} до {salary_to} {currency}"
        elif salary_from is not None:
            return f"от {salary_from} {currency}"
        elif salary_to is not None:
            return f"до {salary_to} {currency}"
        else:
            return 'Зарплата не указана'

    def __str__(self):
        return (
            f"Название: {self.name}\n"
            f"Работодатель: {self.employer}\n"
            f"Зарплата: {self.format_salary()}\n"
            f"Ссылка: {self.url}\n"
            "---------------------"
        )

    def get_max_salary(self):
        if self.salary_info is None:
            return 0
        salary_from = self.salary_info.get('from') or 0
        salary_to = self.salary_info.get('to') or 0
        return max(salary_from, salary_to)

    def __lt__(self, other):
        if self.salary_info is None or other.salary_info is None:
            return False

        # Сравниваем по минимальной зарплате (если указана) или по максимальной
        salary_from_self = self.salary_info.get('from', float('inf'))
        salary_from_other = other.salary_info.get('from', float('inf'))
        salary_to_self = self.salary_info.get('to', float('inf'))
        salary_to_other = other.salary_info.get('to', float('inf'))

        min_salary_self = min(salary_from_self, salary_to_self)
        min_salary_other = min(salary_from_other, salary_to_other)

        return min_salary_self < min_salary_other


class Vacancies(MethodsAbc):
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

    def limit_advertisements(self, advertisements=None):
        # количество вакансий для вывода, сортировка по убыванию зарплаты
        if advertisements:
            self.items = sorted(self.items, key=lambda x: x.get_max_salary(), reverse=True)[:advertisements]
        else:
            self.items.sort(key=lambda x: x.get_max_salary(), reverse=True)

    def del_files(self):
        pass

    def __str__(self):
        return "\n".join(str(vacancy) for vacancy in self.items)
