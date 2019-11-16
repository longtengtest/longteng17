#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from selenium import webdriver
# webdriver.Chrome().find_element_by_partial_link_text()


class LoginPage(object):
    def __init__(self, driver):
        self.driver = driver

    username = ('name', 'username')
    password = ('name', 'password')
    login_btn = ('class name', 'button2')

    def input_user(self, name):
        self.driver.find_element(*self.username).send_keys(name)

    def input_pass(self, passwo):
        self.driver.find_element(*self.password).send_keys(passwo)

    def click_btn(self):
        self.driver.find_element(*self.login_btn).click()

    def login(self, name, password):
        self.input_user(name)
        self.input_pass(password)
        self.click_btn()


class MenuName(object):
    def __init__(self, driver):
        self.driver = driver

    news = ('partial_link_text', '新闻')
    hao123 = ('partial_link_text', '新闻')
    maps = ('partial_link_text', '地图')

    def click_new(self):
        self.driver.find_element(*self.news).click()

    def click_hao123(self):
        self.driver.find_element(*self.hao123).click()