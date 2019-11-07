[TOC]
# Pytest WEB测试框架

## 结构
```
用例层(测试用例)
  |
Fixtures层(业务流程)
  |
PageObject层
  |
Utils实用方法层  
```
## 使用pytest-selenium
### 基础使用
```python
# test_baidu.py
def test_baidu(selenium):
    selenium.get('https://www.baidu.com')
    selenium.find_element_by_id('kw').send_keys('简书 韩志超')
    selenium.find_element_by_id('su').click()
```
运行
```
$ pytest test_baidu.py --driver=chrome
```
或配置到pytest.ini中
```ini
[pytest]
addopts = --driver=chrome
```
### 使用chrome options
```python
# conftest.py
import pytest
@pytest.fixture
def chrome_options(chrome_options):  # 覆盖原有chrome_options
    chrome_options.add_argument('--start-maximized')
    # chrome_options.add_argument('--headless')
    return chrome_options  
```

## Page Object层
### 基本模型
```python
# baidu_page.py
class BaiduPage(object):
    search_ipt_loc = ('id', 'kw')
    search_btn_loc = ('id', 'su')
    
    def __init__(self, driver):
        self.driver = driver
    
    def input_search_keyword(self, text):
        self.driver.find_element(*self.search_ipt_loc).send_keys(text)
    
    def click_search_button(self):
        self.driver.find_element(*self.search_btn_loc).click()
        
    def search(self, text):
        self.input_search_keyword(text)
        self.click_search_button()
```

调用方法：
```python
# test_baidu_page.py
from baidu_page import BaiduPage

def test_baidu_page(selenium):
    baidu = BaiduPage(selenium)
    baidu.search('简书 韩志超')
```
### 使用页面基类
```python
# pages/base_page.py
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
    def input(self, element_loc, text):
        element = self.driver.find_element(*element_loc)
        element.clear()
        element.send_keys(text)
    
    def click(self, element_loc):
        self.driver.find_element(*element_loc).click()
```
```python
# pages/baidu_page.py
from pages.base_page import BasePage

class BaiduPage(BasePage):
    search_ipt_loc = ('id', 'kw')
    search_btn_loc = ('id', 'su')
    
    def input_search_keyword(self, text):
        self.input(self.search_ipt_loc, text)
    
    def click_search_button(self):
        self.click(self.search_btn_loc)
        
    def search(self, text):
        self.input_search_keyword(text)
        self.click_search_button()
```

## Fixtures业务层
```python
# conftest.py
import pytest
from pages.baidu_page import BaiduPage()

@pytest.fixture(scope='session')
def baidu_page(selenium):
    return BaiduPage(selenium)
```

## 用例层
```python
# test_baidu_page2.py
def test_baidu_page(baidu_page):
    baidu_page.search('简书 韩志超')
    assert '韩志超' in baidu.driver.title
```
## 步骤渐进
用例之间不应相互依赖，如果部分用例拥有相同的业务流程，如都需要，打开登录页->登录->点击添加商品菜单->进入添加商品页面
不建议使用以下方式，并使其按顺序执行。
```python
def test_login():
   ...
  
def test_click_menu():
   ...
   
def test_add_goods():
   ...
```
建议对公共的步骤进行封装，可以使用Fixture方法的相互调用来实现步骤渐进，示例如下。
```python
# conftest.py
import pytest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.add_goods_page import AddGoodsPage

@pytest.fixture(scope='session')
def login_page(selenium):
    return LoginPage(selenium)

@pytest.fixture(scope='session')
def menu_page(selenium, login_page):
    """登录后返回菜单页面"""
    login_page.login('默认用户名', '默认密码') # 也可以从数据文件或环境变量中读取
    return MenuPage(selenium)
    
@pytest.fixture(scope='session')
def add_goods_page(selenium, menu_page):
    """从MenuPage跳到添加商品页面"""
    menu_page.click_menu('商品管理', '添加新商品')
    return AddGoodsPage(selenium)
```

```python
# test_ecshop.py
def test_login(login_page):
    login_page.login('测试用户名', '测试密码')
    assert login_page.get_login_fail_msg() is None

def test_add_goods(add_goods_page):
    add_goods_page.input_goods_name('dell电脑')
    add_goods_page.input_goods_category("电脑")
    add_goods_page.input_goods_price('3999')
    add_goods_page.submit()
    assert add_goods_page.check_success_tip() is True
```

## 使用日志
在项目中必要的输出信息可以帮助我们显示测试步骤的一些中间结果和快速的定位问题，虽然Pytest框架可以自动捕获print信息并输出屏幕或报告中，当时更规范的应使用logging的记录和输出日志。
相比print, logging模块可以分等级记录信息。

### 日志等级

实用方法层、页面对象层、Fixture业务层、用例层都可以直接使用logging来输出日志, 使用方法。
```python
# test_logging.py
import logging

def test_logging():
    logging.debug('调试信息')
    logging.info('步骤信息')
    logging.warning('警告信息，一般可以继续进行')
    logging.error('出错信息')
    try:
       assert 0
    except Exception as ex:
        logging.exception(ex)  # 多行异常追溯信息，Error级别
    logging.critical("严重出错信息")
```
使用pytest运行不会有任何的log信息，因为Pytest默认只在出错的信息中显示WARNING以上等级的日志。
要开启屏幕实时日志，并修改log显示等级。
> Log等级: NOTSET < DEBUG < INFO < WARNING(=WARN) < ERROR < CRITICAL
```ini
# pytest.ini
[pytest]
log_cli=True
log_cli_level=INFO
```
运行pytest test_logging.py，查看结果：
```shell
--------------------------------------------- live log call ----------------------------------------------
INFO     root:test_logging.py:5 步骤信息
WARNING  root:test_logging.py:6 警告信息，一般可以继续进行
ERROR    root:test_logging.py:7 出错信息
ERROR    root:test_logging.py:11 assert 0
Traceback (most recent call last):
  File "/Users/apple/Desktop/demo/test_logging.py", line 9, in test_logging
    assert 0
AssertionError: assert 0
CRITICAL root:test_logging.py:12 严重出错信息
```
由于日志等级设置的为INFO级别，因此debug的日志不会输出。

> 对于不同层日志级别的使用规范，可以在实用方法层输出debug级别的日志，如组装的文件路径，文件读取的数据，执行的sql，sql查询结果等等。
在PageObject层输出info级别的日志，如执行某个页面的某项操作等。
Fixtures层和用例层可以根据需要输出一些必要的info，warning或error级别的信息。

### 日志格式

默认的日志格式没有显示执行时间，我们也可以自定义日志输出格式。
```ini
# pytest.ini
...
log_cli_format=%(asctime)s %(levelname)s %(message)s
log_cli_date_format=%Y-%m-%d %H:%M:%S
```
- `%(asctime)s`表示时间，默认为`Sat Jan 13 21:56:34 2018`这种格式，我们可以使用log_cli_date_format来指定时间格式。
- `%(levelname)s`代表本条日志的级别
- `%(message)s`为具体的输出信息

再次运行pytest test_logging.py，显示为以下格式：
```shell
--------------------------------------------- live log call ----------------------------------------------
2019-11-06 21:44:50 INFO 步骤信息
2019-11-06 21:44:50 WARNING 警告信息，一般可以继续进行
2019-11-06 21:44:50 ERROR 出错信息
2019-11-06 21:44:50 ERROR assert 0
Traceback (most recent call last):
  File "/Users/apple/Desktop/demo/test_logging.py", line 9, in test_logging
    assert 0
AssertionError: assert 0
2019-11-06 21:44:50 CRITICAL 严重出错信息
```

更多日志显示选项
- %(levelno)s: 打印日志级别的数值
- %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
- %(filename)s: 打印当前执行程序名
- %(funcName)s: 打印日志的当前函数
- %(lineno)d: 打印日志的当前行号
- %(thread)d: 打印线程ID
- %(threadName)s: 打印线程名称
- %(process)d: 打印进程ID

### 输出日志到文件
在pytest.ini中添加以下配置
```ini
...
log_file = logs/pytest.log
log_file_level = debug
log_file_format = %(asctime)s %(levelname)s %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S
```
log_file是输出的文件路径，输入到文件的日志等级、格式、日期格式要单独设置。
遗憾的是，输出到文件的日志每次运行覆盖一次，不支持追加模式。

## 使用Hooks
使用Hooks可以更改Pytest的运行流程，Hooks方法一般也写在conftest.py中，使用固定的名称。
Pytest的Hooks方法分为以下6种：
1. 引导时的钩子方法
2. 初始化时的的钩子方法
3. 收集用例时的钩子方法
4. 测试运行时的钩子方法
5. 生成报告时的钩子方法
6. 断点调试时的钩子方法

Pytest完整Hooks方法API，可以参考：[API参考-04-钩子(Hooks)](https://www.cnblogs.com/superhin/p/11733499.html)

### 修改配置
以下方法演示了动态生成测试报告名。
```python
# conftest.py
import os
from datetime import datetime
def pytest_configure(config):
    """Pytest初始化时配置方法"""
    if config.getoption('htmlpath'):  # 如果传了--html参数
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        config.option.htmlpath = os.path.join(config.rootdir, 'reports', f'report_{now}.html')
```
以上示例中无论用户--html传了什么，每次运行，都会在项目reports目录下，生成`report_运行时间.html`格式的新的报告。
pytest_configure是Pytest引导时的一个固定Hook方法，我们在conftest.py或用例文件中重新这个方法可以实现在Pytest初始化配置时，挂上我们要执行的一些方法（因此成为钩子方法）。
config参数是该方法的固定参数，包含了Pytest初始化时的插件、命令行参数、ini项目配置等所有信息。
> 可以使用Python的自省方法，print(config.__dict__)来查看config对象的所有属性。

通常，可以通过config.getoption('--html')来获取命令行该参数项的值。使用config.getini('log_file')可以获取pytest.ini文件中配置项的值。


### 添加自定义选项和配置
假设我们要实现一个运行完发送Email的功能。
我们自定义一个命令行参数项--send-email，不需要参数值。当用户带上该参数运行时，我们就发送报告，不带则不发，运行格式如下：（
```shell
pytest test_cases/ --html=report.html --send-email
```
这里，一般应配合--html先生成报告。
由于Pytest本身并没有--send-email这个参数，我们需要通过Hooks方法进行添加。
```python
# conftest.py
def pytest_addoption(parser):
    """Pytest初始化时添加选项的方法"""
    parser.addoption("--send-email", action="store_true", help="send email with test report")
```
另外，发送邮件我们还需要邮件主题、正文、收件人等配置信息。我们可以把这些信息配置到pytest.ini中，如：
```ini
# pytest.ini
...
email_subject = Test Report
email_receivers = superhin@126.com,hanzhichao@secco.com
email_body = Hi,all\n, Please check the attachment for the Test Report.
```
这里需要注意，自定义的配置选项需要先注册才能使用，注册方法如下。
```python
# conftest.py
def pytest_addoption(parser):
    ...
    parser.addini('email_subject', help='test report email subject')
    parser.addini('email_receivers', help='test report email receivers')
    parser.addini('email_body', help='test report email body')
```

### 实现发送Email功能
前面我们只是添加了运行参数和Email配置，我们在某个生成报告时的Hook方法中，根据参数添加发送Email功能，示例如下。
```python
from utils.notify import Email
# conftest.py
def pytest_terminal_summary(config):
    """Pytest生成报告时的命令行报告运行总结方法"""
    send_email = config.getoption("--send-email")
    email_receivers = config.getini('email_receivers').split(',')
    if send_email is True and email_receivers:
        report_path = config.getoption('htmlpath')
        email_subject = config.getini('email_subject') or 'TestReport'
        email_body = config.getini('email_body') or 'Hi'
        if email_receivers:
            Email().send(email_subject, email_receivers, email_body, report_path)
```

# Pytest APP测试框架
APP和Web同属于UI层，我们可以使用包含Page Object模式的同样的分层结构。不同的是我们需要自定义driver这个Fixture。
```python
# conftest.py
import pytest
from appium import webdriver
@pytest.fixture(scope='session')
def driver():
    caps = {
        "platformName": "Android",
        "platformVersion": "5.1.1",
        "deviceName": "127.0.0.1:62001",
        "appPackage": "com.lqr.wechat",
        "appActivity": "com.lqr.wechat.ui.activity.SplashActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "autoLaunch": False
      }
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
```
然后用其他Fixture或用例中直接以参数形式引入driver使用即可。
```python
# test_weixin.py
def test_weixin_login(driver):
    driver.find_element_by_xpath('//*[@text="登录"]').click()
    ...
```
## 使用pytest-variables
> 通过pip install pytest-variables安装
假如我们需要在运行时指定使用的设备配置以及Appium服务地址，我们可以把这些配置写到一个JSON文件中，然后使用pytest-variables插件加载这些变量。
caps.json文件内容：
```json
{
  "caps": {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62001",
    "appPackage": "com.lqr.wechat",
    "appActivity": "com.lqr.wechat.ui.activity.SplashActivity",
    "unicodeKeyboard": true,
    "resetKeyboard": true,
    "autoLaunch": false
  },
  "server": "http://localhost:4723/wd/hub"
}
```
Fixtures中使用：
```python
# conftest.py
...
@pytest.fixture(scope='session')
def driver(variables):
    caps = variables['caps']
    server = variables['server']
    driver = webdriver.Remote(server, caps)
    ...
```
运行方法：
```bash
pytest test_weixin.py --variables caps.json
```
如果有多个配置可以按caps.json格式，保存多个配置文件，运行时加载指定的配置文件即可。运行参数也可以添加到pytest.ini的addopts中。

## 设置和清理
为了保证每条用例执行完不相互影响，我们可以采取每条用例执行时启动app,执行完关闭app，这属于用例方法级别的Fixture方法。
同时，由于第一条用例执行时也会调用该Fixture启动app，这里我们需要设置默认连接设备是不自动启动app，即caps中配置autoLaunch=False。
在conftest.py中添加以下Fixture方法：
```python
# conftest.py
...
@pytest.fixture(scope='function', autouse=True)
def boot_close_app(driver):
    driver.boot_app()
    yield
    driver.close_app()
```
其他Fixture层的页面对象和业务封装可以参考Web框架的模式。
