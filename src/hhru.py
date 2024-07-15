import requests

from src.abc_api import AbstractApi


class HH(AbstractApi):
    """
    Класс для работы с API HeadHunter.

    Атрибуты:
    url : str
        URL для запроса вакансий
    headers : dict
        Заголовки запроса
    params : dict
        Параметры запроса
    vacancies : list
        Список вакансий
    max_pages : int
        Максимальное количество страниц для загрузки
    """

    def __init__(self, file_worker, max_pages=20):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 20}
        self.vacancies = []
        self.max_pages = max_pages
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        # Загружает вакансии по ключевому слову
        self.params['text'] = keyword
        while self.params['page'] < self.max_pages:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            if response.status_code != 200:
                print(f"Ошибка: не удалось загрузить данные. Код состояния: {response.status_code}")
                break

            data = response.json()
            if 'items' not in data:
                print("Ошибка: ответ API не содержит ключ 'items'.")
                break

            vacancies = data['items']
            if not vacancies:
                break
            self.vacancies.extend(vacancies)
            self.params['page'] += 1

    def save_vacancies(self):
        # Сохраняем загруженные вакансии в файл
        self.save_data(self.vacancies)

    def get_vacancies(self, keyword, salary=None):
        # Получаем вакансии по ключевому слову и зарплате
        self.load_vacancies(keyword)
        filtered_vacancies = self.filter_vacancies(salary)
        return filtered_vacancies if filtered_vacancies else self.vacancies

    def filter_vacancies(self, salary=None):
        # Фильтруем вакансии по указанной зарплате
        if salary:
            min_salary, max_salary = map(int, salary.split(' - '))
            filtered_vacancies = [vacancy for vacancy in self.vacancies if
                                  self.check_salary(vacancy, min_salary, max_salary)]
        else:
            filtered_vacancies = self.vacancies

        return filtered_vacancies

    def check_salary(self, vacancy, min_salary, max_salary):
        # Проверяем соответствие зарплаты вакансии указанному диапазону
        salary = vacancy.get('salary')
        if salary is None:
            return False

        salary_from = salary.get('from', 0)
        salary_to = salary.get('to', 0)

        if salary_from and salary_to:
            return min_salary <= salary_from <= max_salary or min_salary <= salary_to <= max_salary
        elif salary_from:
            return min_salary <= salary_from <= max_salary
        elif salary_to:
            return min_salary <= salary_to <= max_salary
        else:
            return False

