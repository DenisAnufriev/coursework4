import pytest
from src.vacancies import Vacancy


def test_vacancy_initialization_with_data():
    vacancy_data = {
        "name": "Программист Python",
        "employer": {"name": "YATT"},
        "salary": {
            "from": 10000,
            "to": 50000,
            "currency": "RUR",
            "gross": True
        },
        "alternate_url": "hh.ru/vacancy/12345"
    }
    vacancy = Vacancy(vacancy_data)

    assert vacancy.name == "Программист Python"
    assert vacancy.employer == "YATT"
    assert vacancy.salary_info == {
        "from": 10000,
        "to": 50000,
        "currency": "RUR",
        "gross": True
    }
    assert vacancy.url == "hh.ru/vacancy/12345"


def test_vacancy_initialization_without_data():
    vacancy_data = {}
    vacancy = Vacancy(vacancy_data)

    assert vacancy.name == "Не указано"
    assert vacancy.employer == "Не указан"
    assert vacancy.salary_info == {}
    assert vacancy.url == "Не указана"


def test_format_salary():
    vacancy_data = {
        "salary": {
            "from": 15000,
            "to": 25000,
            "currency": "USD"
        }
    }
    vacancy = Vacancy(vacancy_data)

    assert vacancy.format_salary() == "от 15000 до 25000 USD"


def test_get_max_salary():
    vacancy_data = {
        "salary": {
            "from": 10000,
            "to": 50000
        }
    }
    vacancy = Vacancy(vacancy_data)

    assert vacancy.get_max_salary() == 50000


def test_lt_comparison():
    vacancy_data1 = {
        "salary": {
            "from": 10000,
            "to": 50000
        }
    }
    vacancy_data2 = {
        "salary": {
            "from": 15000,
            "to": 25000
        }
    }
    vacancy1 = Vacancy(vacancy_data1)
    vacancy2 = Vacancy(vacancy_data2)

    assert vacancy1 < vacancy2
