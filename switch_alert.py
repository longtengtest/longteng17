from selenium import webdriver
from time import sleep


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://115.28.108.130/control.html")

# driver.find_element_by_id('alert').click()
# sleep(2)
# driver.switch_to.alert.accept()

driver.find_element_by_id('prompt').click()
sleep(2)
prompt = driver.switch_to.alert
prompt.send_keys('Kevin')
prompt.accept()


sleep(5)
driver.quit()

'''
Selenim弹出框怎么处理
1. js警告框： switch_to.alert + accept()/dismiss()
2. div对话框： 先触发显示，直接操作
3. 弹出小窗口（新页面）： 切换到新页面+driver.close()

'''