"""
此conftest.py文件用作确保直接在项目下执行pytest命令时能正常导入utils等模块。
也可以不使用该文件，但是在项目中执行时要使用python -m pytest来执行用例。
"""
import os
from datetime import datetime
import pytest
from dotenv import load_dotenv
from utils.notify import Email

load_dotenv()  # 将项目下的.env文件中变量添加到环境变量中


def pytest_configure(config):
    """更改生成报告的路径"""
    htmlpath = config.getoption('htmlpath')
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    config.option.htmlpath = os.path.join(config.rootdir, 'reports', htmlpath.format(now))


def pytest_addoption(parser):
    parser.addoption("--send-email", action="store_true", help="发送邮件")
    parser.addini('email_subject', help='邮件主题')
    parser.addini('email_receivers', help='收件人')
    parser.addini('email_body', help='邮件正文')


def pytest_terminal_summary(config):
    send_email = config.getoption("--send-email")
    email_receivers = config.getini('email_receivers').split(',')
    if send_email is True and email_receivers:
        report_path = config.getoption('htmlpath')
        email_subject = config.getini('email_subject') or 'TestReport'
        email_body = config.getini('email_body') or 'Hi'
        if email_receivers:
            Email().send(email_subject, email_receivers, email_body, report_path)
