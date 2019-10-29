"""请求方法的封装"""
import logging
import requests

TIMEOUT = 30


class Api(object):
    def __init__(self, base_url=None):
        self.session = requests.session()
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        url = self.base_url + url if self.base_url else url
        kwargs['timeout'] = kwargs.get('timeout', TIMEOUT)
        logging.debug(f"请求数据: GET {url} {kwargs}")
        res = self.session.request(method, url, **kwargs)
        logging.debug(f"响应数据: {res.text}")
        return res

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)
