import pytest
from test_cases.app_test.pages.contacts_page import ContactsPage
from test_cases.app_test.pages.person_detail_page import PersonDetailPage
from test_cases.app_test.pages.chat_page import ChatPage


@pytest.mark.nondestructive
def test_login(login, driver):
    pass


@pytest.mark.nondestructive
def test_chat_with_yy(login, driver):
    login.swipe_left()

    ContactsPage(driver).click_yy()
    PersonDetailPage(driver).click_send_btn()
    ChatPage(driver).send_msg('你好,歪歪')


if __name__ == '__main__':
    import pytest
    # pytest.main(["test_login.py::test_login", "-vs", "--variables caps.json"])
    pytest.main(["test_login.py::test_login", "-vs", "--variables caps2.json"])
