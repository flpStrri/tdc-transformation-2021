import abc

from src.domain.employee import Employee


class EmployeeRepository(abc.ABC):
    @abc.abstractmethod
    def fetch_by_id(self, id) -> Employee:
        pass

    @abc.abstractmethod
    def create(self, employee: Employee) -> Employee:
        pass
