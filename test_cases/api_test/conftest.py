import pytest
from utils.data import load_yaml_data
from utils.db import DB
from utils.api import Api

@pytest.fixture(scope='session')
def data():
    data = load_yaml_data('api_data.yaml').from_yaml()
    return data

@pytest.fixture(scope='session')
def db():
    db = DB()
    yield db
    db.close()


@pytest.fixture(scope='session')
def Api():
    api = Api()
    return api
