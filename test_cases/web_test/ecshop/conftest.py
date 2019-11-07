import pytest
from tests.webtest.ecshop.pages.login_page import LoginPage
from selenium import webdriver


@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--headless')
    return chrome_options


@pytest.fixture
def login(selenium):
    selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    selenium.implicitly_wait(10)
    page = LoginPage(selenium)
    page.login('admin', '123456')
