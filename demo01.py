# # 1.导入requests
# import requests
# # 2.组装请求报文并发送
# response = requests.get('http://httpbin.org/get')
# # 3.解析响应
# print(response.status_code)  # 状态码
# print(response.text)  # 响应数据（文本格式）

# 1.导入requests
import requests


def get_01():
    # 2.组装请求报文并发送
    response = requests.get('http://httpbin.org/get')
    # 3.解析响应
    print(response.status_code)  # 状态码
    print(response.text)  # 响应数据（文本格式）


def get_02():
    # url = 'http://www.tuling123.com/openapi/api?key=ec961279f453459b9248f0aeb6600bbe&info=你好'
    url = 'http://www.tuling123.com/openapi/api'
    p = {'key': 'ec961279f453459b9248f0aeb6600bbe', 'info': '你好'}  # 字典变量
    response = requests.get(url, params=p)
    print(response.status_code)  # 状态码
    print(response.text)  # 响应数据（文本格式）


def get_03():
    url = 'http://115.28.108.130:5000/add/'
    p = {'a': 1, 'b': 2}  # 字典变量
    response = requests.get(url, params=p)
    print(response.status_code)  # 状态码
    print(response.text)  # 响应数据（文本格式）


def post_form01():
    """纯文本表单格式Content-Type:application/x-www-form-urlencoded"""
    url = 'http://115.28.108.130:5000/api/user/login/'
    data = {
        'name': '张三',
        'password': '123456'
    }  # 字典类型的请求数据
    response = requests.post(url, data=data)  # data接受字典格式的数据是会进行url编码
    print(response.text)


def post_form02():
    url = 'http://httpbin.org/post'
    data = {
        'name': 'kevin',
        'age': '21',
        'gender': 'male'
    }
    response = requests.post(url, data=data)
    print(response.text)


def post_json03():
    url = 'http://115.28.108.130:5000/api/user/reg/'
    # 字典 True/False/None-->JSON true/false/null
    play_load = {
        "name": "张三",
        "password": "123456"
    }
    res = requests.post(url, json=play_load)
    print(res.text)  # 响应的文本格式
    print(res.json())  # 将响应文本转化为字典，只有当响应数据是json格式时才能转为字典，否则会报错
    res_dict = res.json()
    print(res_dict['code'])
    print(res_dict['msg'])
    print(res_dict['data']['name'])


def add_card_json():
    url = 'http://115.28.108.130:8080/gasStation/process'
    play_load = {
        "dataSourceId": "bHRz",
        "methodId": "00A",
        "CardInfo": {
            "cardNumber": "0100020"
        }
    }
    response = requests.post(url, json=play_load)
    print(response.json())
    print(response.text)


def put_xml():
    """发送xml格式的数据（发送原始格式的数据）"""
    url = 'http://httpbin.org/put'
    play_load = '''
        <xml>
	        <msg>hello</msg>
        </xml>'''
    headers = {"Content-Type":"application/xml"}  # 使用原始格式发送时应手动在请求头中指定内容类型
    res = requests.put(url, data=play_load, headers=headers)  # 当赋给data以字符串格式的话，会原样发送
    print(res.json())
    # print(res.text)


def post_json():
    """发送json格式的数据（发送原始格式的数据）"""
    url = 'http://115.28.108.130:5000/api/user/reg/'
    play_load = '''{
            "name": "张三",
            "password": "123456"
        }'''.encode('utf-8').decode('latin-1')
    headers = {"Content-Type": "application/json"}  # 使用原始格式发送时应手动在请求头中指定内容类型
    res = requests.post(url, data=play_load, headers=headers)  # 当赋给data以字符串格式的话，会原样发送
    print(res.json())
    print(res.text)


def post_file():
    """上传文件接口"""
    url = 'http://115.28.108.130:5000/api/user/uploadImage/'
    files = {'file': open(r'C:\Users\majie\Desktop\1.png', 'rb')}  # 'rb'是以2进制格式打开
    res = requests.post(url=url, files=files)
    print(res.text)


def get_baidu():
    url = 'https://www.baidu.com'
    res = requests.get(url)
    print(res.status_code, res.reason)
    # print(res.json())  # 会报错
    print(res.text)
    print(res.content)
    print(res.encoding)
    print(res.apparent_encoding)
    res.encoding='utf-8'
    print(res.text)
    print(res.headers)  # 会报错
    print(res.cookies.items())
    print(res.cookies.get("BDORZ"))


# 关联/接口依赖----------------------------------------
def post_session():
    """会话保持"""
    session = requests.session()  # 新建一个会话
    # 第一个请求----------------------------------------
    url = 'http://115.28.108.130:5000/api/user/login/'
    data = {
        'name': '张三',
        'password': '123456'
    }
    response = session.post(url, data=data)
    print(response.text)
    # 第二个请求----------------------------------------
    url = 'http://115.28.108.130:5000/api/user/getUserList'
    response = session.get(url)
    print(response.text)


def post_cookies():
    url = 'http://115.28.108.130:5000/api/user/login/'
    data = {
        'name': '张三',
        'password': '123456'
    }
    response = requests.post(url, data=data)
    print(response.text)
    print(response.cookies)

    url = 'http://115.28.108.130:5000/api/user/getUserList'
    response = requests.get(url, cookies=response.cookies)
    print(response.text)


def baidu_orc():
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=kPoFYw85FXsnojsy5bB9hu6x&client_secret=l7SuGBkDQHkjiTPU3m6NaNddD6SCvDMC'
    res = requests.get(url)
    # url = 'https://aip.baidubce.com/oauth/2.0/token'
    # data = {
    #     'grant_type': 'client_credentials',
    #     'client_id':'kPoFYw85FXsnojsy5bB9hu6x',
    #     'client_secret':'l7SuGBkDQHkjiTPU3m6NaNddD6SCvDMC'
    # }
    # res = requests.get(url,params=data)
    print(res.json())
    res_dict = res.json()
    print(res_dict['access_token'])
    token = res_dict['access_token']
    # token = res.json()['access_token']  # 中间变量的提取
    url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}'
    # url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?'
    # params = {"access_token":"token"}
    play_load = {'url': 'http://upload-images.jianshu.io/upload_images/7575721-40c847532432e852.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240'}
    res = requests.post(url, data=play_load)
    print(res.json())
    print(res.json()['words_result'][0])
    print(res.json()['words_result'][0]['words'])

def update_user():
    # 第一步:请求获取token接口拿到token
    url = ' http://115.28.108.130:5000/api/user/getToken/?appid=136425'
    res = requests.get(url)
    print(res.text)
    # 第二步，使用第一步返回的响应数据，组装报文并发送
    # url = f'http://115.28.108.130:5000/api/user/updateUser/?{res.text}'
    url = f'http://115.28.108.130:5000/api/user/updateUser/?'+res.text
    data = {'name':'张三','password':'123456'}
    res = requests.post(url, json=data)
    print(res.json())

# get_01()
# get_02()
# get_03()
# post_form01()
# post_form02()
# post_json03()
# add_card_json()
# put_xml()
# post_json()
# post_file()
# get_baidu()
# post_session()
# post_cookies()
# baidu_orc()
# update_user()