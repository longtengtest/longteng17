class LoginPage(object):
    def __init__(self, driver):
        self.driver = driver

    username_ipt_loc = ('name', 'username')
    password_ipt_loc = ('name', 'password')
    login_btn_loc = ('class name', 'button2')

    def input_username(self, username):
        self.driver.find_element(*self.username_ipt_loc).send_keys(username)

    def input_password(self, password):
        self.driver.find_element(*self.password_ipt_loc).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_btn_loc).click()

    def login(self, username, password):
        self.input_username(username)
        self.input_password(password)
        self.click_login()

