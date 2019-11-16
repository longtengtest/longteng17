#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest
from test_case.test_demo.page.page_demo1 import Login
from test_case.test_demo.page.login_page import LoginPage
from test_case.test_demo.page.login_page import MenuName
from time import sleep


# def test_baidu(baidu):
#     baidu.send_keys('少年的你')
#     baidu.click()


# def test_login(selenium):
#     selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
#     login_shop = LoginPage(selenium)
#     # login.input_user('fengliying')
#     # login.input_pass('123456')
#     # login.click_btn()
#     login_shop.input_user('fengliying')
#     login_shop.input_pass('123456')
#     login_shop.click_btn()
#
#
# def test_login2(selenium):
#     selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
#     login_shop2 = LoginPage(selenium)
#     login_shop2.login('fengliyang', '123456')


# def test_baidu_new(selenium):
#     selenium.get('https://ww.baidu.com')
#     clk = MenuName(selenium)
#     clk.news

def test_login(login):
    login.login('fengliyang', '123456')

