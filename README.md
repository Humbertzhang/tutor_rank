# tutor_rank
Dorahack2018夏武汉 Backend

# Setup

## Install Pytesser & PIL(for captcha recognization)

### Mac OS

```sh
$ brew install pytesser
```

### Linux

## Install requirements(Python Development Environment)

```sh
$ pip install -r requirements.txt
```

## Run Virtual Environment

```sh
$ virtualenv venv && source venv/bin/activate
```

## Create Database

```sh
$ python3 manager.py db init
$ python3 manager.py db migrate
$ python3 manager.py db upgrade
```

## Register Universities

```sh
$ python3 manager.py register
```

# 其他学校接入

创建`tutor_rank/libs/****.py`, 提供函数

```
/**
@param username {String} 用户名
@param password {String} 密码
@return {Boolean} 是否通过验证
*/
def UserVerify(username, password):
    # Your code Here
    return
```