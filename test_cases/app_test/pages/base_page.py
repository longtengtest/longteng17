

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        size = self.driver.get_window_size()
        self.width = size['width']
        self.height = size['height']

    def find_element_by_text(self, text):
        xpath = "//*[@text='%s']" % text
        # xpath = f"//*[@text='{text}']"
        return self.driver.find_element_by_xpath(xpath)

    def swipe_up(self):
        x1 = self.width / 2
        y1 = self.height * 0.95
        x2 = self.width / 2
        y2 = self.height * 0.05
        self.driver.swipe(x1, y1, x2, y2)

    def swipe_left(self):
        x1 = self.width * 0.95
        y1 = self.height / 2
        x2 = self.width * 0.05
        y2 = self.height / 2
        self.driver.swipe(x1, y1, x2, y2)

    def input(self, element_loc, text):
        print(element_loc)
        element = self.driver.find_element(*element_loc)
        element.clear()
        element.send_keys(text)





