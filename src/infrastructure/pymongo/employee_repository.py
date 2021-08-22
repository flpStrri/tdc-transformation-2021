from src.domain.employee import Employee
from src.infrastructure.pymongo import MONGO_DB


class EmployeeRepository:
    def __init__(self):
        self.__collection = MONGO_DB.employee

    def fetch_by_id(self, id):
        employee = self.__collection.find_one({"_id": id})

        return Employee(id=employee["_id"], name=employee["name"], role=employee["role"])

    def create(self, employee):
        self.__collection.insert_one(
            {"_id": str(employee.id), "name": employee.name, "role": employee.role}
        )

        return employee
