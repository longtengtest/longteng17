from appium.webdriver.common.mobileby import MobileBy as By
from tests.apptest.pages.base_page import BasePage


class LaunchPage(BasePage):
    # 页面元素 -------------------------------------
    login_btn_loc = (By.ID, 'com.lqr.wechat:id/btnLogin')
    reg_btn_loc = (By.ID, 'com.lqr.wechat:id/btnRegister')

    # 元素操作 -------------------------------------
    def click_login_btn(self):
        self.driver.find_element(*self.login_btn_loc).click()

    def click_reg_btn(self):
        self.driver.find_element(*self.reg_btn_loc).click()

