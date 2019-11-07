from appium import webdriver
import pytest
from tests.apptest.pages.launch_page import LaunchPage
from tests.apptest.pages.login_page import LoginPage
from tests.apptest.pages.chatout_list_page import ChatoutListPage


@pytest.fixture(scope='session')
def driver(variables):
    print(variables)
    caps = variables['caps']
    server = variables['server']
    driver = webdriver.Remote(server, caps)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope='function', autouse=True)
def launch_close_app(driver):
    driver.launch_app()
    yield
    driver.close_app()


@pytest.fixture
def login(driver):
    LaunchPage(driver).click_login_btn()
    LoginPage(driver).login('18010181267', '123456')
    chatout_list_page = ChatoutListPage(driver)
    assert chatout_list_page.check_weixin_ico() is True
    return chatout_list_page