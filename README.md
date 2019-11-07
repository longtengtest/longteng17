[TOC]
# Pytest API测试框架

## 功能规划

1. 数据库断言 pymysql -> 封装
2. 环境清理  数据库操作 -> Fixtures
3. 并发执行  pytest-xdist 多进程并行
4. 复合断言  pytest-check
5. 用例重跑  pytest-rerunfailures
6. 环境切换  pytest-base-url
7. 数据分离  pyyaml
8. 配置分离  pytest.ini
9. 报告生成  pytest-html, allure-pytest
10. 接口监控
11. 发送报告邮件

### 安装相应的包
pip安装时可以通过`-i https://pypi.doubanio.com/simple/`,指定使用豆瓣的源, 下载稍微快一点
```
pip install requests pymysql pyyaml pytest pyetst-xdist pytest-check pytest-rerunfailures pytest-base-url pytest-html -i https://pypi.doubanio.com/simple/
```

导出依赖到requirements.txt中
```
pip freeze > requirments.txt
```

## 结构规划

### 分层结构
分层设计模式: 每一层为上层提供服务
```
用例层(测试用例)
  |
Fixtures辅助层(全局的数据、数据库操作对象和业务流等)
  |
utils实用方法层(数据库操作, 数据文件操作，发送邮件方法等等)
```

### 静态目录

- data: 存放数据
- reports: 存放报告

### 目录结构

```
longteng17/
  - data/
    - data.yaml: 数据文件
  - reports/: 报告目录
  - test_cases/: 用例目录
    - pytest.ini:  pytest配置
    - api_test/:  接口用例目录
      - conftest.py:  集中管理Fixtures方法
    - web_test/:  web用例目录
    - app_test/:  app用例目录
  - utils/: 辅助方法
    - data.py: 封装读取数据文件方法
    - db.py: 封装数据库操作方法
    - api.py: 封装api请求方法
    - notify.py: 封装发送邮件等通知方法
  - conftest.py: 用来放置通用的Fixtures和Hooks方法
  - pytest.ini: Pytest运行配置
```
> 规划conftest.py的位置，要确保项目跟目录被导入到环境变量路径(sys.path)中去。
conftest.py及用例的导入机制为：
>1. 如果在包（同级有__init__.py）内，则导入最上层包（最外一个包含__init__.py）的父目录。
>2. 如果所在目录没有__init__.py，直接导入conftest.py父目录。

## 数据文件的选择
- 无结构
    - txt: 分行, 无结构的文本数据
- 表格型
    - csv: 表格型, 适合大量同一类型的数据
    - excel: 表格型, 构造数据方便, 文件较大,解析较慢
- 树形
    - json: 可以存储多层数据, 格式严格,不支持备注
    - yaml: 兼容json, 灵活,可以存储多层数据
    - xml: 可以存储多层, 文件格式教繁琐
- 配置型 
    - .ini/.properties/.conf: 只能存储1-2层数据, 适合配置文件

由于用例数据常常需要多层级的数据结构，这里选择yaml文件作为本项目的数据文件，示例格式如下：
```yaml
test_case1: 
    a: 1
    b: 2
```
数据第一层以用例名标识某条用例所使用的数据，这里约定要和用例名称完全一致，方便后面使用Fixture方法自动向用例分配数据。

## 标记规划
 
标记: mark, 也称作标签, 用来跨目录分类用例方便灵活的选择执行。

- 按类型: api, web, app
- 按等级: p0, p1, p2
- 标记有bug: bug
- 标记异常流程: negative

也可以根据自己的需求，按模块、按是否有破坏性等来标记用例。

## utils实用方法层

### 数据文件操作: data.py

#### 组装文件绝对路径
因为运行的目录通常是不确定的,因此数据,报告等静态文件我们一般需要使用绝对路径.
1. 当前文件绝对路径: `data_py=os.path.abspath(__file__)`
2. 所在目录路径: `utils=os.path.dirname(data_py)`
3. 项目根目录: `basedir=os.path.dirname(utils)`
4. 组装文件路径: `file_path = os.path.join(basedir, 'data', 'api_data.yaml')`

#### 使用yaml.safe_load()加载数据
1. 打开文件 with open(..) as f:
2. 加载数据  data=yaml.safe_load(f)

> yaml.safe_load()和yaml.load()的区别:

>由于yaml文件也支持任意的Python对象
从文件中直接加载注入Python是极不安全的, safe_load()会屏蔽Python对象类型,只解析加载字典/列表/字符串/数字等级别类型数据

示例如下:
```python
import yaml

def load_yaml_data(file_path):
    with open(file_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print("加载yaml文件: {file_path} 数据为: {data}")
    return data
```

> 为了示例简单，这里没有对文件不存在、文件格式非yaml等异常做处理。异常处理统一放到Fixture层进行。

> 假如项目要支持多种数据文件, 可以使用类来处理。

### 数据库操作: db.py
这里使用pymysql, 安装方法pip install pymysql
#### 敏感数据处理
#### 数据库配置分离
数据库密码等敏感数据，直接放在代码或配置文件中，会有暴露风险，用户敏感数据我们可以放到环境变量中，然后从环境变量中读取出来。
> 注意：部署项目时，应记得在服务器上配置相应的环境变量，才能运行。

Windows在环境变量中添加变量MYSQL_PWD,值为相应用户的数据库密码，也可以将数据库地址，用户等信息也配置到环境变量中。
Linux/Mac用户可以通过在~/.bashrc或~/.bash_profile或/etc/profile中添加
```
export MYSQL_PWD=数据库密码
```
然后source相应的文件使之生效,如`source ~/.bashrc`。

Python中使用`os.getenv('MYSQL_PWD')`便可以拿到相应环境变量的值。
> 注意：如果使用PyCharm，设置完环境变量后，要重启PyCharm才能读取到新的环境变量值。

我们使用字典来存储整个数据库的配置，然后通过字典拆包传递给数据库连接方法。

```python
import os
import pymysql

DB_CONF = {
    'host': '数据库地址',
    'port': 3306,
    'user': 'test',
    'password': os.getenv('MYSQL_PWD'),
    'db': 'longtengserver',
    'charset': 'utf8'
}

conn = pymysql.connect(**DB_CONF)
```
#### 封装数据库操作方法
数据常见的操作方法有查询，执行修改语句和关闭连接等。对应一种对象的多个方法，我们使用类来封装。
同时为避免查询语句和执行语句的串扰，我们在建立连接时使用autocommit=True来确保每条语句执行后都立即提交，完整代码如下。
```python
import os
import pymysql

DB_CONF = {
    'host': '数据库地址',
    'port': 3306,
    'user': 'test',
    'password': os.getenv('MYSQL_PWD'),
    'db': 'longtengserver',
    'charset': 'utf8'
}

class DB(object):
    def __init__(self, db_conf=DB_CONF)
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        
    def query(self, sql):
        self.cur.execute(sql)
        data = self.cur.fetchall()
        print(f'查询sql: {sql} 查询结果: {data}')
        return data
        
    def change_db(self, sql):
        result = self.cur.execute(sql)
        print(f'执行sql: {sql} 影响行数: {result}')
        
    def close(self):
        print('关闭数据库连接')
        self.cur.close()
        self.conn.close()
```
其中如果查询中包含中文，要根据数据库指定响应的charset，这里的charset值为utf8不能写成utf-8。
self.conn.cursor(pymysql.cursors.DictCursor)这里使用了字典格式的游标，返回的查询结果会包含响应的表字段名，结果更清晰。

由于所有sql语句都是单条自动提交，不支持事务，因此在change_db时，不需要再作事务异常回滚的操作，对于数据库操作异常，统一在Fixture层简单处理。

#### 封装常用数据库操作
```
# db.py
...
class FuelCardDB(DB):
    def del_card(self, card_number):
        print(f'删除加油卡: {card_number}')
        sql = f'DELETE FROM cardinfo WHERE cardNumber="{card_number}"'
        self.change_db(sql)

    def check_card(self, card_number):
        print(f'查询加油卡: {card_number}')
        sql = f'SELECT id FROM cardinfo WHERE cardNumber="{card_number}"'
        res = self.query(sql)
        return True if res else False

    def add_card(self, card_number):
        print(f'添加加油卡: {card_number}')
        sql = f'INSERT INTO cardinfo (cardNumber) VALUES ({card_number})'
        self.change_db(sql)
```

### 发送邮件通知: notify.py
#### 使用Python发送邮件
发送邮件一般要通过SMTP协议发送。首先要在你的邮箱设置中开启SMTP服务，清楚SMTP服务器地址、端口号已经是否必须使用安全加密传输SSL等。
使用Python发送邮件分3步：
1. 组装邮件内容MIMEText
2. 组装邮件头: From、To及Subject
3. 登录SMTP服务器发送邮件

- 组装邮件内容MIMEText
```python
from email.mime.text import MIMEText
import smtplib
body = 'Hi, all\n附件中是测试报告, 如有问题请指出'
body2 = '<h2>测试报告</h2><p>以下为测试报告内容<p>'
# msg = MIMEText(content, 'plain', 'utf-8')
msg = MIMEText(content2, 'html', 'utf-8')
```
使用MIMEText组装Email消息数据对象，正文支持纯文本plain和html两种格式。

- 组装邮件头: From、To及Subject
```
...
msg['From'] = 'zhichao.han@qq.com'
msg['To'] = 'superhin@126.com'
msg['Subject'] = '接口测试报告'
```
msg['From']中也可以声明收件人名称，格式为：
```python
msg['From'] = '<韩志超> zhichao.han@qq.com'
```
msg['To']中也可以写多个收件人，写到一个字符串中使用英文逗号隔开：
```python
msg['To'] = 'superhin@126.com,ivan-me@163.com'
```
> 注意邮件头的From、To只是一种声明，并不一定是实际的发件人和收件人，比如From写A邮箱，实际发送时，使用B邮箱的SMTP发送，便会形成代发邮件（B代表A发送）。

- 登录SMTP服务器发送邮件
```python
...
smtp = smtplib.SMTP('邮箱SMTP地址')
# smtp = smtplib.SMTP_SSL('邮箱SMTP地址')
smtp.login('发件人邮箱', '密码')
smtp.sendmail('发件人邮箱', '收件人邮箱', msg.as_string())
```
这里登录SMTP和SMTP_SSL要看邮箱服务商支持哪种，连接时也可以指定端口号，如：
```
smtp = smtplib.SMTP_SSL('邮箱SMTP地址', 465)
```
登录时的密码根据邮箱的支持可以是授权码或登录密码（一般如QQ邮箱采用授权码，不支持使用登录密码登录SMTP）。
sendmail发送邮件时，使用的发件人邮箱和收件人邮箱是实践的发件人和收件人，可以和邮件头中的不一致。但是发件人邮箱必须和登录SMTP的邮箱一致。
sendmail每次只能给一个收件人发送邮件，当有多个收件人是，可以使用多次sendmail方法，示例如下：
```python
receivers = ['superhin@163.com', 'zhichao.han@qq.com']
for person in receivers:
   smtp.sendmail('发件人邮箱', person, msg.as_string())
```
msg.as_string()是将msg消息对象序列化为字符串后发送。

#### 发送带附件的邮件
由于邮件正文会过滤掉大部分的样式和JavaScript，因此直接将html报告读取出来，放到邮件正文中往往没有任何格式。这时，我们可以通过附件来发送测试报告。

邮件附件一般采用二进制流格式（application/octet-stream），正文则采用文本格式。要混合两种格式我们需要使用MIMEMultipart这种混合的MIME格式，一般步骤为：
1. 建立一个MIMEMultipart消息对象
2. 添加MIMEText格式的正文
3. 添加MIMEText格式的附件（打开附件，按Base64编码转为MIMEText格式）
4. 添加邮件头信息
5. 发送邮件

示例代码如下：
```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# 1. 建立一个MIMEMultipart消息对象
msg = MIMEMultipart()

# 2. 添加邮件正文
body = MIMEText('hi, all\n附件中是测试报告,请查收', 'plain', 'utf-8')
msg.attach(body)

# 3. 添加附件
att = MIMEText(open('report.html', 'rb').read(), 'base64', 'utf-8')
att['Content-Type'] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename=report.html'
msg.attach(att1)

# 4. 添加邮件头信息
...

# 5. 发送邮件
...
```
使用消息对象msg的attach方法来添加MIMEText格式的邮件正文和附件。
构造附件MIMEText对象时，要使用rb模式打开文件，使用base64格式编码，同时要声明附件的内容类型Content-Type以及显示排列Content-Dispositon，这里的`attachment; filename=report.html`，attachment代表附件图标，filename代表显示的文件名，这里表示图标在左，文件名在右，显示为report.html。

添加邮件头信息和发送邮件同发送普通邮件一致。


#### 发送邮件方法封装
同样，我们可以将敏感信息邮箱密码配置到环境变量中去，这里变量名设置为SMTP_PWD。
```python
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

SMTP_HOST = '邮箱SMTP地址'
SMTP_USER = '发件人邮箱'
SMTP_PWD = os.getenv('SMTP_PWD')

def send_email(self, body, subject, receivers, file_path):
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1["Content-Disposition"] = f'attachment; filename={file_name}'
    msg.attach(att1)
    
    msg['From'] = SMTP_USER
    msg['To'] = ','.join(receivers)
    msg['Subject'] = subject
    
    smtp = smtplib.SMTP_SSL(SMTP_HOST)
    smtp.login(SMTP_USER, SMTP_PWD)
    for person in receivers:
        print(f'发送邮件给: {person}')
        smtp.sendmail(SMTP_USER, person, msg.as_string())
    print('邮件发送成功')
```
同样，为了示例简单，这里并没有对SMTP连接、登录、发送邮件做异常处理，读者可以进行相应的补充。

### 请求方法封装：api.py
requests本身已经提供了很好的方法，特别是通用的请求方法requests.request()。这里的封装只是简单加了base_url组装、默认的超时时间和打印信息。
```python
import requests

TIMEOUT = 30

class Api(object):
    def __init__(self, base_url=None):
        self.session = requests.session()
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        url = self.base_url + url if self.base_url else url
        kwargs['timeout'] = kwargs.get('timeout', TIMEOUT)
        res = self.session.request(method, url, **kwargs)
        print(f"发送请求: {method} {url} {kwargs} 响应数据: {res.text}")
        return res

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)
```
这里，Api实例化时如果传递了base_url参数，则所有的url都会拼接上base_url。
`kwargs['timeout'] = kwargs.get('timeout', TIMEOUT)`，设置默认的超时时间设置为30s。

## Fixtures方法层

```python
import pytest
from utils.data import Data
from utils.db import FuelCardDB
from utils.api import Api

@pytest.fixture(scope='session')
def data(request):
    basedir = request.config.rootdir
    try:
        data_file_path = os.path.join(basedir, 'data', 'api_data.yaml')
        data = Data().load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return data

@pytest.fixture(scope='session')
def db():
    try:
        db = FuelCardDB()
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        yield db
        db.close()

@pytest.fixture(scope='session')
def api():
    api = Api()
    return api
```
这里对，utils实用方法层的异常进行简单的skip处理，即当数据连接或数据文件有问题时，所有引用该Fixture的用例都会自动跳过。

### 按用例名分发用例
Fixture方法通过用例参数，注入到用例中使用。Fixture方法中可以拿到用例所在的模块，模块变量，用例方法对象等数据，这些数据都封装在Fixture方法的上下文参数request中。
原有的data这个Fixture方法为用例返回了数据文件中的所有数据，但是一般用例只需要当前用例的数据即可。我们在数据文件中第一层使用和用例方法名同名的项来区分各个用例的数据。如：
```yaml
# api_data.yaml
test_add_fuel_card_normal: 
  data_source_id: bHRz
  cardNumber: hzc_00001
...
```
下面的示例演示了根据用例方法名分配数据的Fixture方法：
```python
# conftest.py
...
@pytest.fixture
def case_data(request, data):
    case_name = request.function.__name__
    return data.get(case_name)
```
request是用例请求Fixture方法的上下文参数，里面包含了config对象、各种Pytest运行的上下文信息，可以通过Python的自省方法`print(request.__dict__)`查看request对象中所有的属性。
- request.function为调用Fixture的函数方法对象，如果是用例直接调用的Fixture，这里便是用例函数对象，通过函数对象的__name__属性获取到函数名。
- 通过request.module拿到用例所在模块，进而根据模块中某些属性作相应动态配置。
- 通过request.config可以拿到pytest运行时的运行参数、配置参数值等信息。

这样，用例中引入的case_data参数就只是该用例的数据。

## 用例层
一条完整的用例应包含以下步骤：
1. 环境检查或数据准备
2. 业务操作
3. 不止一条断言语句（包括数据库断言）
4. 环境清理

另外一般用例还应加上指定的标记。

```python
import pytest

@pytest.mark.p1
@pytest.mark.api
def test_add_fuel_card_normal(api, db, case_data):
    """正常添加加油卡"""
    url = '/gasStation/process'
    data_source_id, card_number = case_data.get('data_source_id'), case_data.get('card_number')

    # 环境检查
    if db.check_card(card_number):
        pytest.skip(f'卡号: {card_number} 已存在')

    json_data = {"dataSourceId": data_source_id, "methodId": "00A",
                 "CardInfo": {"cardNumber": card_number}}
    res_dict = api.post(url, json=json_data).json()

    # 响应断言
    assert 200 == res_dict.get("code"))
    assert "添加卡成功" == res_dict.get("msg")
    assert res_dict.get('success') is True
    
    # 数据库断言
    assert db.check_card(card_number) is True

    # 环境清理
    db.del_card(card_number)
```
### 使用复合断言：pytest-check
使用assert断言时，当某一条断言失败后，该条用例即视为失败，后面的断言不会再进行判断。有时我们需要每一次可以检查所有的检查点，输出所有断言失败项。此时我们可以使用pytest-check插件进行复合断言。
安装方法pip install pytest-check。
所谓复合断言即，当某条断言失败后仍继续检查下面的断言，最后汇总所有失败项。
pytest-check使用方法
```python
import pytest_check as check
...
check.equal(200, es_dict.get("code"))
check.equal("添加卡成功",res_dict.get("msg"))
check.is_true(res_dict.get('success'))
check.is_true(db.check_card(card_number))
```
除此外常用的还有:
- check.is_false()：断言值为False
- check.is_none(): 断言值为None
- check.is_not_none()：断言值不为None

### 标记用例跳过和预期失败
如果某些用例暂时环境不满足无法运行可以标记为skip, 也可以使用skipif()判断条件跳过。 对于已知Bug，尚未完成的功能也可以标记为xfail（预期失败）。
使用方法如下：
```python
import os
import pytest

@pytest.mark.skip(reason="暂时无法运行该用例")
def test_a():
    pass
    
@pytest.mark.skipif(os.getenv("MYSQL_PWD") is None, reason="缺失环境变量MYSQL_PWD配置")
def test_b():
    pass
    
@pytest.mark.xfail(reason='尚未解决的已知Bug')
def test_c():
    pass
```
test_b首先对环境变量做了检查，如果没有配置MYSQL_PWD这个环境变量，则会跳过该用例。
test_c为期望失败，这时如果用例正常通过则视为异常的xpass状态，失败则为视为正常的xfail状态，在--strict严格模式下，xfail视为用例通过，xpass视为用例失败。
这里标记运行时分别使用-r/-x/-X显示skip、xfail、xpass的原因说明：
```
pytest -rsxX
```
这里的-s可以在命令行上显示用例中print的一些信息。

另外，也可以在Fixture方法或用例中，使用pytest.skip("跳过原因"), pytest.xfail("期望失败原因")来根据条件表用例跳过和期望失败。

> 标记skip和xfail属于一种临时隔离策略，等问题修复后，应及时去掉该标记。

## 

# Pytest Web测试框架

## 项目结构
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
### 步骤渐进
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
