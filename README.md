[toc]
# API测试框架
基于Pytest

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
用例  test_cases/  集中管理
  |
Fixtures层 conftest.py 
  |
[业务层]
  |
辅助方法层(数据库封装, 发送邮件等等)  utils/common/public
```

### 静态目录

- data: 存放数据
- reports: 存放报告
- logs: 存放日志

### 目录结构

```
longteng17/
  - data/
    - data.yaml: 数据文件
  - logs/:  日志目录
  - reports/: 报告目录
  - test_cases/: 用例目录
    - pytest.ini:  pytest配置
    - api_test/:  接口用例目录
      - conftest.py:  集中管理fixtures方法
    - web_test/:  web用例目录
    - app_test/:  app用例目录
  - utils/: 辅助方法
    - data.py: 封装读取数据文件方法
    - db.py: 封装数据库操作方法
    - api.py: 封装api请求方法
    - notify.py: 封装发送邮件等通知方法
```

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
 
 ## 标记规划
 
标记: mark, 也称作标签, 用来跨目录分类用例方便灵活的选择执行。

- 按类型: api, web, app
- 按等级: p0, p1, p2
- 标记有bug: bug
- 标记异常流程: negative
- 按功能模块:
- 按是否有破坏性: 


## utils辅助方法层

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
import os

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_yaml_data(yaml_file):
    file_path = os.path.join(basedir, 'data', yaml_file)
    with open(file_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data

```
#### 使用类
假如项目要支持多种数据文件, 可以使用类来处理, 示例如下:
```python
import yaml
import os
import json

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Data(object):
    def __init__(self, file_name):
        # 组装绝对路径, 绑定给对象
        self.file_path = os.path.join(basedir, 'data', file_name)

    def from_yaml(self):
        with open(self.file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

    def from_json(self):
        with open(self.file_path, encoding='utf-8') as f:
            data = json.load(f)
        return data
```

> 注: 如果使用Jenkins等运行时报导入错误的话, 可以加上
```python
import sys
sys.path.append('..')
```

### 数据库操作: db.py

#### 使用字典+解包分离数据库配置

#### 封装query和change_db方法

#### 使用字典格式的游标

### 发送通知, notify.py
```python
from email.mime.text import MIMEText
import smtplib
# 1. 组装邮件内容MIMEText
content = '''Hi, all
附件中是测试报告, 如有问题请指出
'''
content2 = '''<h2>测试报告</h2>
<p>附件中是测试报告, 如有问题请指出<p>
'''
# msg = MIMEText(content, 'plain', 'utf-8')
msg = MIMEText(content2, 'html', 'utf-8')

# 2. 邮件头, From To 邮件主题
msg['From'] = '<韩志超> zhichao.han@qq.com'
# msg['From'] = 'zhichao.han@qq.com'
msg['To'] = 'ivan-me@163.com, superhin@126.com'
msg['Subject'] = '接口测试报告'

# 3. 登录smtp服务器,并发送
smtp = smtplib.SMTP('smtp.163.com')
# smtp = smtplib.SMTP_SSL('smtp.sina.com')
smtp.login('ivan-me@163.com', 'hanzhichao123')  # 一般情况下要使用授权密码
receivers = ['zhichao.han@qq.com', 'superhin@126.com']
for person in receivers:
    smtp.sendmail('ivan-me@163.com', person, msg.as_string())
print("邮件发送成功")
```
#### 携带附件
```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# 1. 复合格式(多部分)
msg = MIMEMultipart()
# 2. 邮件正文
body = MIMEText('hi, all\n附件中是测试报告,请查收', 'plain', 'utf-8')
msg.attach(body)

# 3.邮件头
msg['From'] = 'ivan-me@163.com'
msg['To'] = 'superhin@126.com'
msg['Subject'] = '接口测试报告'

# 4. 附件
f = open('report.html', 'rb')
att1 = MIMEText(f.read(), 'base64', 'utf-8')
att1['Content-Type'] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename=report2.html'
f.close()

msg.attach(att1)

# 5. 发送
smtp = smtplib.SMTP_SSL('smtp.163.com')
smtp.login('ivan-me@163.com', 'hanzhichao123')

smtp.sendmail('ivan-me@163.com', 'superhin@126.com', msg.as_string())
```

#### 方法封装
```python
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Notice(object):
    def email(self, body, subject, receivers, file_name):
        """发送邮件
        body是正文信息
        subject邮件主题
        receivers是收件人列表
        file_path是附件路径"""

        smtp_conf = os.getenv('SMTP_CONFIG')
        smtp_host, is_ssl, user, password = smtp_conf.split(',')

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        msg['From'] = user
        msg['To'] = ','.join(receivers)
        msg['Subject'] = subject

        file_path = os.path.join(basedir, 'reports', file_name)
        att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1["Content-Disposition"] = f'attachment; filename={file_name}'
        msg.attach(att1)

        smtp = smtplib.SMTP_SSL(smtp_host)
        smtp.login(user, password)
        for person in receivers:
            smtp.sendmail(user, person, msg.as_string())

```

## Fixtures方法层
> 所有辅助方法的异常在Fixtures层做skip处理

```python
import pytest
from utils.data import Data
from utils.db import DB
from utils.api import Api


@pytest.fixture(scope='session')
def data():
    data = Data('api_data.yaml').from_yaml()
    return data


@pytest.fixture(scope='session')
def db():
    db = DB()
    yield db
    db.close()


@pytest.fixture(scope='session')
def api():
    api = Api()
    return api

```

## 用例层
