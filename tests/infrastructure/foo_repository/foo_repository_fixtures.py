from faker import Faker
from pytest import fixture

from infrastructure.foo_repository import FooRepository
from tests.infrastructure.database.dynamo_db_test_wrapper import DynamoDBWrapper


class FooRepositoryFixtures(DynamoDBWrapper):
    @fixture
    def fake(self):
        return Faker("pt_BR")

    @fixture
    def repository(self, data_table):
        return FooRepository(data_table)
