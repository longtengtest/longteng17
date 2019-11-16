'''读取数据文件'''
import yaml
import os
# import sys
# sys.path.append('..')
# sys.path.append(basedir)


# 计算文件的绝对路径
# data_py=os.path.abspath(__file__)当前文件绝对路径
# utils=os.path.dirname(__file__):计算所在目录
# basedir=os.path.dirname(utils):再往上找一级
# basedir2=os.path.abspath(basedir):绝对路径

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_yaml_data(yaml_file):

    '''加载数据文件，yaml_file是项目data下的文件名'''
    # D:/
    # file_path = basedir+'/'+'data'+'/'+ yaml_file
    file_path = os.path.join(basedir,'data',yaml_file)
    with open(yaml_file, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


if __name__ == '__main__':
    data = load_yaml_data('api_data.yaml')
    print(data)


# """读取数据文件"""
# import yaml
# import os
# # 计算文件的绝对路径
# # data_py=os.path.abspath(__file__)当前文件绝对路径
# # utils=os.path.dirname(data_py): 计算所在目录
# # basedir=os.path.dirname(utils): 再往上赵一级
# basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# def load_yaml_data(yaml_file):
#     """加载数据文件,yaml_file是项目data下的文件名, 如api_data.yaml"""
#     # D:/Projects/longteng17/data/api_data.yaml
#     # file_path = basedir + '/' + 'data' + '/' + yaml_file
#     file_path = os.path.join(basedir, 'data', yaml_file)
#     with open(file_path, encoding='utf-8') as f:
#         data = yaml.safe_load(f)
#     return data
# if __name__ == '__main__':
#     data = load_yaml_data('api_data.yaml')
#     print(data)