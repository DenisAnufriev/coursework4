import pytest
from src.parser import HH
from src.file_worker import FileWorker
from src.vacancies import Vacancies, Vacancy
import requests


def test_hh_vacancy1_initialization(hh_vacancy1):
    assert len(hh_vacancy1._HH__vacancies) == 1
    assert hh_vacancy1._HH__max_pages == 0
    assert hh_vacancy1._HH__vacancies[0]['name'] == "Программист Python"
    assert hh_vacancy1._HH__vacancies[0]['employer'] == "YATT"
    assert hh_vacancy1._HH__vacancies[0]['url'] == "hh.ru/vacancy/12345"

def test_hh_vacancy2_initialization(hh_vacancy2):
    assert len(hh_vacancy2._HH__vacancies) == 1
    assert hh_vacancy2._HH__max_pages == 0
    assert hh_vacancy2._HH__vacancies[0]['name'] == "Программист Java"
    assert hh_vacancy2._HH__vacancies[0]['employer'] == "ATT"
    assert hh_vacancy2._HH__vacancies[0]['url'] == "hh.ru/vacancy/123456"
    assert hh_vacancy2._HH__params['page'] == 1

class ServerResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json_data = json_data if json_data else {}

    def json(self):
        return self._json_data


def test_load_vacancies_success(file_worker):
    hh = HH(file_worker=file_worker, max_pages=1)

    success_response = ServerResponse(200, {'items': [{
        "name": "Программист Python",
        "employer": "YATT",
        "salary_info": {
            "from": 10000,
            "to": 50000,
            "currency": "RUR",
            "gross": True
        },
        "url": "hh.ru/vacancy/12345"
    }]})

    def server_get(url, headers, params):
        return success_response

    requests.get = server_get
    hh.load_vacancies('Python')

    assert hh._HH__params['page'] == 1
    assert len(hh._HH__vacancies) == 1
    assert hh._HH__vacancies[0]['name'] == "Программист Python"


def test_load_vacancies_error(file_worker, capsys):
    hh = HH(file_worker=file_worker, max_pages=1)

    error_response = ServerResponse(500)

    def server_get(url, headers, params):
        return error_response

    requests.get = server_get
    hh.load_vacancies('Python')

    captured = capsys.readouterr()
    assert "Ошибка: не удалось загрузить данные. Код состояния: 500" in captured.out
    assert hh._HH__params['page'] == 0
    assert len(hh._HH__vacancies) == 0


def test_load_vacancies_items_missing(file_worker, capsys):
    hh = HH(file_worker=file_worker, max_pages=1)

    error_response = ServerResponse(200, {'other_key': 'value'})

    def server_get(url, headers, params):
        return error_response

    requests.get = server_get
    hh.load_vacancies('Python')

    captured = capsys.readouterr()
    assert "Ошибка: ответ API не содержит ключ 'items'." in captured.out
    assert hh._HH__params['page'] == 0
    assert len(hh._HH__vacancies) == 0
