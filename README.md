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
创建 `/app/universities/universityname.py`
编写一个类
包括登录所需信息类型 schema
模拟登录函数login
```
class UniversityName():
    schema = {
		"username":"str",
		"password":"password",
		"verify": 0 or 1 // 表示是否需要验证码	
	}
	# return True if success 
	# return False if failed
	def login(request_body):
		if success:
			return True
		else:
			return False
```
