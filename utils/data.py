"""读取数据文件"""
import yaml
import json
import logging


class Data(object):
    def __init__(self):
        pass

    def load_yaml(self, file_path):
        logging.debug(f'加载yaml文件: {file_path}')
        with open(file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

    def load_json(self, file_path):
        logging.debug('加载json文件: {file_path}')
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        return data
