from appium import webdriver
import pytest
from test_cases.app_test.pages.launch_page import LaunchPage
from test_cases.app_test.pages.login_page import LoginPage
from test_cases.app_test.pages.chatout_list_page import ChatoutListPage
import logging


@pytest.fixture(scope='session')
def driver(variables):
    caps = variables['caps']
    server = variables['server']
    try:
        driver = webdriver.Remote(server, caps)
    except Exception as ex:
        pytest.skip('Appium服务未启动')
    else:
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
