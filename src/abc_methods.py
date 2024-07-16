from abc import ABC, abstractmethod

class MethodsAbc(ABC):

    @abstractmethod
    def load_vacancies(self, keyword, salary=None):
        pass

    @abstractmethod
    def save_vacancies(self):
        pass

    @abstractmethod
    def del_files(self):
        pass