import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.infrastructure.sqlalchemy.model.employee import Employee  # noqa

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:@localhost:5432/tdc")

engine = create_engine(DATABASE_URL)

session = scoped_session(sessionmaker(bind=engine))
