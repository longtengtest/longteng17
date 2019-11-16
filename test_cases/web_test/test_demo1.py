import pytest
import logging


@pytest.mark.skip
def test_baidu(selenium):
    selenium.get('http://www.baidu.com')
    selenium.find_element_by_id('kw').send_keys('少年的你')
    selenium.find_element_by_id('su').click()


@pytest.mark.skip
def test_baidu2(selenium):
    from test_cases.web_test.pages.baidu_page import BaiduPage
    selenium.get('http://www.baidu.com')
    baidu_page = BaiduPage(selenium)
    baidu_page.search('少年的你')


@pytest.mark.skip
def test_baidu3(baidu_page):
    print('测试百度搜索 少年的你')
    baidu_page.search('少年的你')


@pytest.mark.skip
def test_login(selenium):
    from test_cases.web_test.pages.login_page import LoginPage
    selenium.get(
        'http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    page = LoginPage(selenium)
    page.login('admin', '123456')


@pytest.mark.skip
def test_login1(login_page):
    login_page.login('admin', '123456')


@pytest.mark.skip
def test_login2(login_page):
    login_page.login('admin', '1234567')


@pytest.mark.skip
def test_menu(selenium):
    from test_cases.web_test.pages.login_page import LoginPage
    from test_cases.web_test.pages.menu_page import MenuPage
    selenium.get(
        'http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    page = LoginPage(selenium)
    page.login('admin', '123456')
    page = MenuPage(selenium)
    page.click_menu('商品管理', '添加新商品')


@pytest.mark.skip
def test_add_goods(add_goods_page):
    print('测试添加商品')
    add_goods_page.input_goods_name('dell电脑')
    add_goods_page.input_category_name('电脑')
    add_goods_page.input_price('3999')
    add_goods_page.click_submit_btn()


def test_logging():
    logging.debug('调试日志')
    logging.info('点击登录')
    logging.warning('警告，数据文件缺失！')
    logging.error("出错了")
    logging.critical("严重出错")
