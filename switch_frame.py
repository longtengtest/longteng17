# from selenium import webdriver
# from time import sleep
#
# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.get("http://115.28.108.130/control.html")
#
# '''
# 1. 层层切入：switch_to.frame(frame/iframe的id/name/index/定位到元素)
# 2. 同级直接不能相互切，只能父子切入切出
# 3. 切出switch_to.parent_frame():切出到父框架
# 4. switch_to.default_content()：切出所有框架
# '''
#
# driver.switch_to.frame('parent_frame')
# driver.switch_to.frame('left')
# driver.find_element_by_link_text('链接2').click()
#
# driver.switch_to.parent_frame()
#
# driver.switch_to.frame('main')
# print(driver.find_element_by_tag_name('h2').text)
#
# driver.switch_to.default_content()
# sleep(5)
# driver.quit()
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
driver.implicitly_wait(30)
driver.find_element_by_name('username').send_keys('admin')
driver.find_element_by_name('password').send_keys('123456')
driver.find_element_by_class_name('button2').click()
driver.switch_to.frame("menu-frame")
driver.find_element_by_link_text("商品管理").click()
driver.find_element_by_link_text("商品分类").click()
driver.switch_to.parent_frame()
driver.switch_to.frame("main-frame")
driver.find_element_by_link_text("添加分类").click()
driver.find_element_by_name("cat_name").send_keys("大还丹")
driver.find_element_by_css_selector("#general-table > tbody > tr:nth-child(3) > td:nth-child(2) > select").click()
driver.find_element_by_css_selector("#general-table > tbody > tr:nth-child(3) > td:nth-child(2) > select > option:nth-child(86)").click()
driver.find_element_by_class_name("button").click()
driver.quit()