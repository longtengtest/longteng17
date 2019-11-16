"""读取数据文件"""
import yaml
import os
import json

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Data(object):
    def __init__(self, file_name):
        # 组装绝对路径, 绑定给对象
        self.file_path = os.path.join(basedir, 'data', file_name)

    def from_yaml(self):
        with open(self.file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data

    def from_json(self):
        with open(self.file_path, encoding='utf-8') as f:
            data = json.load(f)
        return data

if __name__ == '__main__':
    data = Data('api_data.yaml').from_yaml()
    print(data)
