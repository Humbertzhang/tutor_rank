class Ccnu():
    # 登录需要的信息的schema
    # type: string(明文) password(密码) verifycode(验证码图片URL)
    schema = {
        "username":"str",
        "password":"password"
    }

    def __init__(self, schema):
        self.schema = schema

    # need return True if success. False if falied.
    def login(self, request_body):
        pass
