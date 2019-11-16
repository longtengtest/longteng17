from datetime import datetime
import os
from utils.notify import Notice


def pytest_configure(config):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    config.option.htmlpath = os.path.join(
        config.rootdir, 'reports', f'report_{now}.html')

    # config.option.log_file = os.path.join(
    #     config.rootdir, 'reports', f'pytest_{now}.log')


def pytest_addoption(parser):
    parser.addoption("--send-email", action="store_true", help="是否发送邮件")


def pytest_terminal_summary(config):
    if config.getoption("--send-email"):
        htmlpath = config.getoption('htmlpath')
        Notice().email('正文', '主题', ['ivan-me@163.com'], htmlpath)
