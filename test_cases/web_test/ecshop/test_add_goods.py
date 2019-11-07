import pytest
from tests.webtest.ecshop.pages.add_goods_page import AddGoodsPage
from tests.webtest.ecshop.pages.menu_page import MenuPage


@pytest.mark.webtest
@pytest.mark.smoke
@pytest.mark.p0
def test_add_goods(selenium, login):
    MenuPage(selenium).click_menu('商品管理', '添加新商品')
    page = AddGoodsPage(selenium)
    page.input_goods_name('dell电脑')
    page.input_goods_category("电脑")
    page.input_goods_price('3999')
    page.submit()
    assert page.check_success_tip()
