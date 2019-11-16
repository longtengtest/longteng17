class AddGoodsPage(object):
    goods_name_ipt_loc = ('name', 'goods_name')
    category_name_ipt_loc = ('id', 'cat_name')
    price_ipt_loc = ('name', 'shop_price')
    submit_btn_loc = ('id', 'goods_info_submit')

    def __init__(self, driver):
        self.driver = driver
        self.driver.switch_to.frame('main-frame')

    def input_goods_name(self, goods_name):
        self.driver.find_element(
            *self.goods_name_ipt_loc).send_keys(goods_name)

    def input_category_name(self, category_name):
        self.driver.find_element(
            *self.category_name_ipt_loc).send_keys(category_name)

    def input_price(self, price):
        self.driver.find_element(
            *self.price_ipt_loc).send_keys(price)

    def click_submit_btn(self):
            self.driver.find_element(
                *self.submit_btn_loc).click()
