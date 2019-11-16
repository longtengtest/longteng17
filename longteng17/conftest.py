#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pytest

from test_case.test_demo.page.page_demo1 import Login
from test_case.test_demo.page.login_page import LoginPage


@pytest.fixture()
def seleniums(selenium):
    selenium.implictly_wait(10)
    selenium.maximize_window()
    return selenium


@pytest.fixture()
def baidu(selenium):
    selenium.get('https://www.baidu.com')
    return Login(selenium)


@pytest.fixture()
def login(selenium):
    selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    return LoginPage(selenium)



