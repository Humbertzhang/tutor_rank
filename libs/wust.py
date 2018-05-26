import requests
from pytesseract import *
from PIL import Image
from io import BytesIO

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}

def getRandCode(sess):
    """
    获取登陆验证码，验证码写到 path 所指定的目录，默认为 randcode.jpg
    """
    url = r'http://jwxt.wust.edu.cn/whkjdx/verifycode.servlet'
    ans = sess.get(url)
    ans.raise_for_status()
    return ans.content


def login(sess, username, password, randcode):
    """
    登陆函数，登陆成功返回 True
    """
    url = r'http://jwxt.wust.edu.cn/whkjdx/Logon.do?method=logon'
    SSOurl = r'http://jwxt.wust.edu.cn/whkjdx/Logon.do?method=logonBySSO'
    information = {'USERNAME': username, 'PASSWORD': password, 'RANDOMCODE': randcode}
    ans = sess.post(url, data = information, headers = headers)
    ans.raise_for_status()
    ans.encoding = ans.apparent_encoding
    ans2 = sess.post(SSOurl, headers)
    ans2.raise_for_status()
    if ans.text.find(r'http://jwxt.wust.edu.cn/whkjdx/framework/main.jsp') != -1:
        return True
    else:
        return False

def UserVerify(username, password):
    sess = requests.session();
    res_content = getRandCode(sess)
    image = Image.open(BytesIO(res_content))
    code = image_to_string(image) 
    print('randCode: ', code)
    return login(sess, username, password, code)

if __name__ == '__main__':
    print(UserVerify('201713158028', '201713158028'))
