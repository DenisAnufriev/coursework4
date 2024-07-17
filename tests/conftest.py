import pytest
from src.parser import HH
from src.file_worker import FileWorker

@pytest.fixture
def file_worker():
    return FileWorker('testfile.txt')

@pytest.fixture
def hh_vacancy1(file_worker):
    hh = HH(file_worker=file_worker, max_pages=0)
    hh._HH__vacancies = [{
        "name": "Программист Python",
        "employer": "YATT",
        "salary_info": {
            "from": 10000,
            "to": 50000,
            "currency": "RUR",
            "gross": True
        },
        "url": "hh.ru/vacancy/12345"
    }]
    return hh

@pytest.fixture
def hh_vacancy2(file_worker):
    hh = HH(file_worker=file_worker, max_pages=0)
    hh._HH__params['page'] = 1
    hh._HH__vacancies = [{
        "name": "Программист Java",
        "employer": "ATT",
        "salary_info": {
            "from": 15000,
            "to": 150000,
            "currency": "RUR",
            "gross": True
        },
        "url": "hh.ru/vacancy/123456"
    }]
    return hh
