import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

load_dotenv()

# Use a separate test database
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/taskdb_test")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    # create_all is safe: it only creates tables that don't exist
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def db_setup():
    setup_db()
    yield
    # Destructive drop_all() removed to allow testing on persistent databases

@pytest.fixture
def db():
    connection = engine.connect()
    # Begin a transaction. All changes made during the test 
    # will be rolled back at the end, ensuring the DB stays clean.
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    from app.main import app
    from app.database import get_db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
