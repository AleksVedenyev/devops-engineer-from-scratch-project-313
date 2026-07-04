import os

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from main import app, get_session
from model import Link  # noqa: F401

DB_FILE = "test.db"


@pytest.fixture
def test_db():
    engine = create_engine(f"sqlite:///{DB_FILE}")
    SQLModel.metadata.create_all(engine)
    
    yield engine

    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)


@pytest.fixture
def client(test_db):    
    def override_get_session():
        with Session(test_db) as session:
            yield session
    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()