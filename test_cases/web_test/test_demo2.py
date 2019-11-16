from test_cases.web_test.pages.login_page import LoginPage
import pytest

@pytest.mark.skip
def test_login(selenium):
    selenium.get(
        'http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    page = LoginPage(selenium)
    page.login('admin', '123456')

