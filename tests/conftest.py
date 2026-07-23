from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app import storage

FUTURE_DUE_DATE = (date.today() + timedelta(days=7)).strftime("%d/%m/%Y")


@pytest.fixture(autouse=True)
def _reset_storage():
    storage._reset()
    yield
    storage._reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_task(client):
    r = client.post(
        "/tasks",
        json={"title": "fixture task", "due_date": FUTURE_DUE_DATE},
    )
    assert r.status_code == 201
    return r.json()
