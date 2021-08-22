import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.domain.employee import Employee as EmployeeDomain
from src.infrastructure.sqlalchemy.model import Base


class Employee(Base):
    __tablename__ = "employee"

    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("name", String(150), nullable=False)
    role = Column("role", String(150), nullable=False)

    @classmethod
    def from_domain(cls, domain):
        return cls(id=domain.id, name=domain.name, role=domain.role)

    def to_domain(self):
        return EmployeeDomain(id=self.id, name=self.name, role=self.role)
