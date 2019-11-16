class BaiduPage(object):
    def __init__(self, driver):
        self.driver = driver
    
    # 页面元素
    # 'name', 'class name', 'tag name', 'link text', 'partial link text', 'xpath', 'css selector'
    search_ipt_loc = ('id', 'kw')  # 搜索框
    search_btn_loc = ('id', 'su')  # 搜索按钮

    # 对每一个元素操作，封装一个方法
    def input_keyword(self, text):
        """输入关键字"""
        self.driver.find_element(*self.search_ipt_loc).send_keys(text)

    def click_search_btn(self):
        """点击搜索按钮"""
        self.driver.find_element(*self.search_btn_loc).click()

    # 业务组合
    def search(self, text):
        """输入关键字并搜索"""
        self.input_keyword(text)
        self.click_search_btn()
