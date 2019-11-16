'''请求方法的封装'''
import requests


TIMEOUT = 30
class Api(object):
    def __init__(self):
        self.session = requests.session()
        # self.login()
    def request(self,method,url,**kwargs):
        kwargs['timeout'] = kwargs.get('timeout',TIMEOUT)
        print(f"请求数据：GET {url} {kwargs}")
        res = self.session.request(method, url,**kwargs)
        print(f"响应数据：{res.text}")
        print(res)
    def get(self,url,**kwargs):
        self.request('get', url,**kwargs)
    def post(self,url,**kwargs):
        self.request('post', url,**kwargs)
    def login(self):
        pass

if __name__ == '__main__':
    api = Api()
    api.get('http://www.baidu.com')