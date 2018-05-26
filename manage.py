import sys
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, app
from app.models import User

# 编码设置
#reload(sys)
#sys.setdefaultencoding('utf-8')


manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """自动加载环境"""
    return dict(
        app = app,
        db = db,
        User = User,
    )


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def register():
    """register all schools"""
    import os
    import redis
    import pi
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    dir_list = os.listdir('../libs')
    university_list = list()
    
    for each in dir_list:
        if each.endsWith('.py'):
            university_list.append(each.strip('.py'))

    r.set('universities', pickle.dumps(university_list))

@manager.command
def test():
    """run your unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def admin():
    """add administrator"""
    from getpass import getpass
    username = raw_input("\_admin username: ")
    email = raw_input("\_admin email: ")
    password = getpass("\_admin password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = 2
    )
    db.session.add(u)
    db.session.commit()
    print("<admin user %s add in database>" % username)


@manager.command
def adduser():
    """add user"""
    from getpass import getpass
    username = raw_input("\_username: ")
    email = raw_input("\_email: ")
    role_id = raw_input("\_[1:moderator 2:admin 3:user]: ")
    password = getpass("\_password: ")
    u = User(
        email = email,
        username = username,
        password = password,
        role_id = role_id
    )
    db.session.add(u)
    db.session.commit()
    print ("<user %s add in database>" % username)


if __name__ == '__main__':
    manager.run()
