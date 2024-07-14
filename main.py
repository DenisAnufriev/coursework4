from src.file_worker import FileWorker
from src.hhru import HH, format_salary

def main(keyword, salary=None, advertisements=None):
    filename = 'data/vacancies.json'
    file_worker = FileWorker(filename)
    hh = HH(file_worker)

    if salary:
        print(f"\nЗапрос: {keyword}, Зарплата: {salary}")
    else:
        print(f"\nЗапрос: {keyword}")

    vacancies = hh.get_vacancies(keyword, salary)
    hh.save_vacancies()  # Сохраняем вакансии в файл
    print(f"Найдено вакансий: {len(vacancies)}")

    if advertisements:
        vacancies = vacancies[:advertisements]

    for vacancy in vacancies:
        name = vacancy.get('name', 'Не указано')
        employer = vacancy.get('employer', {}).get('name', 'Не указан')
        salary_info = vacancy.get('salary', {})
        salary_str = format_salary(salary_info)
        url = vacancy.get('alternate_url', 'Не указана')

        print(f"Название: {name}")
        print(f"Работодатель: {employer}")
        print(f"Зарплата: {salary_str}")
        print(f"Ссылка: {url}")
        print("---------------------")

if __name__ == "__main__":
    keyword = input("Введите ключевое слово для поиска вакансий:\n")
    salary = input("Введите зарплатный диапазон (например, '10000 - 500000') или нажмите Enter:\n")
    advertisements = input("Введите кол-во объявлений которое нужно вывести (например, 5) или нажмите Enter:\n")

    advertisements = int(advertisements) if advertisements else None

    main(keyword, salary, advertisements)
