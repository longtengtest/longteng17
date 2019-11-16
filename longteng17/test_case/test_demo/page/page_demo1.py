#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Login(object):

    send = ('id', 'kw')
    clk = ('id', 'su')

    def __init__(self, driver):
        self.driver = driver

    def send_keys(self, text):
        self.driver.find_element(*self.send).send_keys(text)

    def click(self):
        self.driver.find_element(*self.clk).click()


