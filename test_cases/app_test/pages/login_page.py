from appium.webdriver.common.mobileby import MobileBy as By
from tests.apptest.pages.base_page import BasePage


class LoginPage(BasePage):
    # 页面元素 ---------------------------------
    phone_ipt_loc = (By.ID, 'com.lqr.wechat:id/etPhone')
    password_ipt_loc = (By.ID, 'com.lqr.wechat:id/etPwd')
    login_btn_loc = (By.ID, 'com.lqr.wechat:id/btnLogin')

    # 元素操作 ---------------------------------
    def input_phone_num(self, phone_num):
        self.input(self.phone_ipt_loc, phone_num)

    def input_password(self, password):
        self.input(self.password_ipt_loc, password)

    def click_login(self):
        self.driver.find_element(*self.login_btn_loc).click()

    # 业务操作 ---------------------------------
    def login(self, phone_num, password):
        self.input_phone_num(phone_num)
        self.input_password(password)
        self.click_login()
