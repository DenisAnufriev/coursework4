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
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 20}
        self.__vacancies = []
        self.__max_pages = max_pages
        super().__init__(file_worker)

    def load_vacancies(self, keyword):
        # Загружает вакансии по ключевому слову
        self.__params['text'] = keyword
        while self.__params['page'] < self.__max_pages:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
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
            self.__vacancies.extend(vacancies)
            self.__params['page'] += 1

    def get_vacancies(self, keyword, salary=None):
        # Получаем вакансии по ключевому слову и зарплате
        self.load_vacancies(keyword)
        filtered_vacancies = self.__filter_vacancies(salary)
        return filtered_vacancies if filtered_vacancies else self.__vacancies

    def __filter_vacancies(self, salary=None):
        # Фильтруем вакансии по указанной зарплате
        if salary:
            min_salary, max_salary = map(int, salary.split(' - '))
            filtered_vacancies = [vacancy for vacancy in self.__vacancies if
                                  self.__check_salary(vacancy, min_salary, max_salary)]
        else:
            filtered_vacancies = self.__vacancies

        return filtered_vacancies

    def __check_salary(self, vacancy, min_salary, max_salary):
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
