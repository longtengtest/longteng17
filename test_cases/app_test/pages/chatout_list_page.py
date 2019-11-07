from tests.apptest.pages.base_page import BasePage
from appium.webdriver.common.mobileby import MobileBy as By
from selenium.common.exceptions import NoSuchElementException


class ChatoutListPage(BasePage):
    weixin_ico_loc = (By.ID, 'com.lqr.wechat:id/tvMessagePress')

    def check_weixin_ico(self):
        try:
            self.driver.find_element(*self.weixin_ico_loc)
            return True
        except NoSuchElementException:
            return False
