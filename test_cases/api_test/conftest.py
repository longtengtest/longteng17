import os
import pytest
from utils.data import Data
from utils.db import FuelCardDB
from utils.api import Api


@pytest.fixture(scope='session')
def data(request):
    basedir = request.config.rootdir
    try:
        data_file_path = os.path.join(basedir, 'data', 'api_data.yaml')
        data = Data().load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return data


@pytest.fixture
def case_data(request, data):
    case_name = request.function.__name__
    return data.get(case_name)


@pytest.fixture(scope='session')
def db():
    try:
        db = FuelCardDB()
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        yield db
        db.close()


@pytest.fixture(scope='session')
def api(base_url):
    api = Api(base_url)
    return api

