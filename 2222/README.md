# API测试框架
基于Pytest

## 功能规划
1. 数据库断言 pymysql -> 封装
2. 环境清理 数据库操作 -> Fixtures
3. 并发执行 pytest -> xdist 多进程并行
4. 复合断言 pytest -> check
5. 用例重跑 pytest-rerunfailures
6. 环境切换 pytest-base-url
7. 数据分离 pyyaml
8. 配置分离 pytest.ini
9. 报告生成 pytest-html,allure-pytest
10. 接口监控
11. 发送报告邮件

## 结构规划
### 分层结构
分层设计模式：每一层为上层提供服务

```
用例 test_case/ 集中管理
|
fixtures层 conftest.py
|
[业务层]
|
辅助方法层（数据库封装，发送邮件等等）utils/common/public
```


### 静态目录
- data: 存放数据
- reports: 存放报告
- logs: 存放日志
### 目录结构
day09
 - data
 - logs
 - reports
 - test_cases
  - api_test
   - conftest.py
  - web_test
  - app_test
 - utils
  - data.py
  - db.py
  - api.py
  - notify.py
## 数据文件的选择
- 无结构
    - txt: 分行，无结构的文本数据
- 表格型
    - csv: 表格型，适合大量同一类型的数据
    - excel：表格型，构造数据方便，文件较大，解析较慢
- 树型
    - json: 可以存储多层数据，格式严格，不支持备注
    - yaml: 兼容json,灵活，可以存储多层数据
    - xml:可以存储多层，文件格式较繁琐
- 配置型
    - .ini/.properties/.conf：只能存储1-2层数据，适合配置文件

## 标记规划

标记：mark,也称作标签，用来跨目录分类用例，方便灵活的选择执行。
- 按类型：api,web,app
- 按等级：p0,p1,p2
- 标记有bug: bug
- 标记异常流程：negative
- 按功能模块：
- 按是否有破坏性：


### 数据库操作：db.py
#### 使用字典+解包分离数据库配置

#### 封装query和change_db方法




##Fixtures方法层
import pytest
from utils.data import load_yaml_data
from utils.db import DB
from utils.api import Api

@pytest.fixture(scope='session')
def data():
    data = load_yaml_data('api_data.yaml').from_yaml()
    return data

@pytest.fixture(scope='session')
def db():
    db = DB()
    yield db
    db.close()


@pytest.fixture(scope='session')
def Api():
    api = Api()
    return api
##用例层



