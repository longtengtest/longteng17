from selenium.webdriver.common.by import By
from tests.webtest.ecshop.pages.base_page import BasePage
from selenium.common.exceptions import NoSuchElementException


class AddGoodsPage(BasePage):
    def __init__(self, driver):
        super(AddGoodsPage, self).__init__(driver)
        self.driver.switch_to.frame("main_frame")

    goods_name_ipt_loc = (By.NAME, "goods_name")
    goods_category_ipt_loc = (By.ID, "cat_name")
    goods_price_ipt_loc = (By.NAME, "shop_price")
    submit_btn_loc = (By.ID, "goods_info_submit")
    success_tip = (By.XPATH, '//td[contains(text(),"添加商品成功")]')

    def input_goods_name(self, goods_name):
        print(f"输入商品名:{goods_name}")
        element = self.driver.find_element(*self.goods_name_ipt_loc)
        element.clear()
        element.send_keys(goods_name)

    def input_goods_category(self, goods_category):
        print(f"输入商品分类:{goods_category}")
        element = self.driver.find_element(*self.goods_category_ipt_loc)
        element.clear()
        element.send_keys(goods_category)

    def input_goods_price(self, goods_price):
        print(f"输入商品价格:{goods_price}")
        element = self.driver.find_element(*self.goods_price_ipt_loc)
        element.clear()
        element.send_keys(goods_price)

    def submit(self):
        print("提交")
        self.driver.find_element(*self.submit_btn_loc).click()

    def check_success_tip(self):
        try:
            self.driver.find_element(*self.success_tip)
        except NoSuchElementException:
            return False
        else:
            return True