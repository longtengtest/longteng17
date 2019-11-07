from selenium.webdriver.common.by import By
from tests.webtest.ecshop.pages.base_page import BasePage


class LoginPage(BasePage):
    username_ipt_loc = (By.NAME, 'username')
    password_ipt_loc = (By.NAME, 'password')
    login_btn = (By.CLASS_NAME, 'button2')

    def input_username(self, username):
        element = self.driver.find_element(*self.username_ipt_loc)
        element.clear()
        element.send_keys(username)

    def input_password(self, password):
        element = self.driver.find_element(*self.password_ipt_loc)
        element.clear()
        element.send_keys(password)

    def click_login_btn(self):
        self.driver.find_element(*self.login_btn).click()

    def login(self, username, password):
        print("登录")
        self.input_username(username)
        self.input_password(password)
        self.click_login_btn()

