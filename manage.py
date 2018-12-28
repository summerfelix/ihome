from flask_script import Manager
from utils.app import create_app


# 获取flask对象app
app = create_app()

# 管理app
manage = Manager(app)


if __name__ == '__main__':
    manage.run()
