from tests.apptest.pages.base_page import BasePage
from appium.webdriver.common.mobileby import MobileBy as By


class PersonDetailPage(BasePage):
    send_btn_loc = (By.ID, 'com.lqr.wechat:id/btnCheat')

    def click_send_btn(self):
        self.driver.find_element(*self.send_btn_loc).click()
