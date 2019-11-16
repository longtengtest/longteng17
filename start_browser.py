from selenium import webdriver

driver = webdriver.Chrome()   # 启动Chrome
# driver = webdriver.Firefox()
# driver = webdriver.Ie()
# driver = webdriver.Edge()

driver.maximize_window()  # 最大化

driver.get('https://www.baidu.com')
print(driver.title)
print(driver.page_source)
driver.get('https://www.qq.com')
driver.set_window_size(800,600)

driver.save_screenshot('qq.png')  # 截图

driver.back()  # 后退
driver.forward()  # 前进
driver.refresh()  # 前进
print(driver.title)

# driver.close()  # 关闭
driver.quit()   # 退出
