from selenium import webdriver
from selenium.webdriver.support.select import Select
from time import sleep


driver = webdriver.Chrome()

driver.maximize_window()
driver.get("http://115.28.108.130/control.html")

area = driver.find_element_by_id('areaID')
s = Select(area)
s.select_by_index(1)
s.select_by_value('1')
s.select_by_visible_text('天津')


sleep(5)
driver.quit()