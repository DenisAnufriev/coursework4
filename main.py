from src.vacancies import Vacancies

def main():
    keyword = input("Введите ключевое слово для поиска вакансий:\n")
    salary = input("Введите зарплатный диапазон (например, '10000 - 150000') или нажмите Enter:\n")
    advertisements = input("Введите топ N вакансий по зарплате которое нужно вывести (например, 5) или нажмите Enter:\n")

    advertisements = int(advertisements) if advertisements else None

    vacancies = Vacancies()
    vacancies.load_vacancies(keyword, salary)
    vacancies.limit_advertisements(advertisements)
    print(f"Топ {advertisements} вакансий:\n")
    print(vacancies)

if __name__ == "__main__":
    main()
