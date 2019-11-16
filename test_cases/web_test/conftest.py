import pytest
from test_cases.web_test.pages.baidu_page import BaiduPage
from test_cases.web_test.pages.login_page import LoginPage
from test_cases.web_test.pages.menu_page import MenuPage
from test_cases.web_test.pages.add_goods_page import AddGoodsPage
from test_cases.web_test.pages.goods_list_page import GoodsListPage


@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(10)
    # selenium.maximize_window()
    return selenium

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('--start-maximized')
    # chrome_options.add_argument('--headless')
    # chrome_options.headless = True
    return chrome_options

@pytest.fixture
def baidu_page(selenium):
    selenium.get('http://www.baidu.com')
    page = BaiduPage(selenium)
    return page

@pytest.fixture
def login_page(selenium):
    # 1. 进入这个页面
    selenium.get(
        'http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    # 生成并返回页面对象
    return LoginPage(selenium)

@pytest.fixture
def menu_page(selnium, login_page):
    # 1. 进入这个页面
    login_page.login('admin', '123456')
    # 2. 生成并返回页面对象
    return MenuPage(selenium)


@pytest.fixture
def add_goods_page(selenium, menu_page):
    # 1. 进入这个页面
    menu_page.click_menu('商品管理', '添加新商品')
    # 2. 把页面对象返回给用例
    return AddGoodsPage(selenium)

@pytest.fixture
def goods_list_page(selenium, menu_page):
    # 1. 进入这个页面
    menu_page.click_menu('商品管理', '商品列表')
    # 2. 把页面对象返回
    return GoodsListPage(selenium)
    

