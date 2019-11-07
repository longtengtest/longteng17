from tests.apptest.pages.launch_page import LaunchPage
from tests.apptest.pages.login_page import LoginPage
from tests.apptest.pages.chatout_list_page import ChatoutListPage
from tests.apptest.pages.contacts_page import ContactsPage
from tests.apptest.pages.person_detail_page import PersonDetailPage
from tests.apptest.pages.chat_page import ChatPage


def test_login(login, driver):
    pass


def test_chat_with_yy(login, driver):
    login.swipe_left()

    ContactsPage(driver).click_yy()
    PersonDetailPage(driver).click_send_btn()
    ChatPage(driver).send_msg('你好,歪歪')


if __name__ == '__main__':
    import pytest
    # pytest.main(["test_login.py::test_login", "-vs", "--variables caps.json"])
    pytest.main(["test_login.py::test_login", "-vs", "--variables caps2.json"])
