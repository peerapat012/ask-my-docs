import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()

@pytest.fixture(scope="session")
def engine():
    url = os.getenv("TEST_DATABASE_URL").replace("postgresql://", "postgresql+psycopg://", 1)
    engine = create_engine(url)
    yield engine
    engine.dispose()
    
@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode='create_savepoint')
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()