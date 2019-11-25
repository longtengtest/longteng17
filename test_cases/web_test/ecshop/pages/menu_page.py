from selenium.webdriver.common.by import By
from test_cases.web_test.ecshop.pages.base_page import BasePage


class MenuPage(BasePage):
    def click_menu(self, menu, sub_menu):
        print(f'点击菜单:{menu}-{sub_menu}')
        self.driver.switch_to.frame("menu-frame")
        self.driver.find_element(By.LINK_TEXT, menu).click()
        self.driver.find_element(By.LINK_TEXT, sub_menu).click()
        self.driver.switch_to.default_content()
