from test_cases.app_test.pages.base_page import BasePage
from appium.webdriver.common.mobileby import MobileBy as By


class ContactsPage(BasePage):
    yy_loc = (By.XPATH, "//*[@text='歪歪']")
    # yy_loc = (By.ID, "com.lqr.wechat:id/tvName")

    def click_yy(self):
        print("点击歪歪")
        self.driver.find_element(*self.yy_loc).click()
