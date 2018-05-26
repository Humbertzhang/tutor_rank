import requests
from bs4 import BeautifulSoup

class Ccnu():
    # 登录需要的信息的schema
    # type: string(明文) password(密码) verifycode(验证码图片URL)
    schema = {
        "username":"str",
        "password":"password",
        "verify": 0
    }
    def __init__(self, schema):
        self.schema = schema

    # need return True if success. False if falied.
    def login(self, request_body):
        sid = request_body.get("username")
        password = request_body.get("password")

        r = requests.get("https://account.ccnu.edu.cn/cas/login")
        cookie = r.headers.get("set-cookie")
        Cookie = cookie[0:49]

        soup = BeautifulSoup(r.content)
        lt = soup.find('input', {'name' : 'lt'}) ['value']
        execution = soup.find('input',{'name' : 'execution'}) ['value']

        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'157',
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie':Cookie,
            'Host':'account.ccnu.edu.cn',
            'Origin':'https://account.ccnu.edu.cn',
            'Referer':'https://account.ccnu.edu.cn/cas/login',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

        data = { 
            'username' : '2017211661',
            'password' : 'TAM137731',
            'lt' : lt,
            'execution' : execution,
            '_eventId' : 'submit',
            'submit' : '登录'
        }

        r2 = requests.post("https://account.ccnu.edu.cn/cas/login", data = data, headers = headers)
        if "CASTGC=" in r2.headers.get('Set-Cookie'):
            return True
        else:
            return False




