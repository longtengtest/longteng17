from test_cases.app_test.pages.base_page import BasePage
from appium.webdriver.common.mobileby import MobileBy as By


class ChatPage(BasePage):
    msg_ipt_loc = (By.ID, 'com.lqr.wechat:id/etContent')
    send_btn_loc = (By.XPATH, '//*[@text="发送"]')

    def input_msg(self, msg):
        self.input(self.msg_ipt_loc, msg)

    def click_send_btn(self):
        self.driver.find_element(*self.send_btn_loc).click()

    def send_msg(self, msg):
        self.input_msg(msg)
        self.click_send_btn()
