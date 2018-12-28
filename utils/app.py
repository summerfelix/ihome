from flask import Flask

from app.models import db
from app.user_views import blue_user
from app.house_views import blue_house
from app.order_views import blue_order
from utils.config import Conf
from utils.settings import STATIC_PATH, TEMPLATES_PATH


def create_app():
    app = Flask(__name__, static_folder=STATIC_PATH,
                template_folder=TEMPLATES_PATH)

    # 加载配置
    app.config.from_object(Conf)

    # 蓝图
    app.register_blueprint(blueprint=blue_user, url_prefix='/user')
    app.register_blueprint(blueprint=blue_house, url_prefix='/house')
    app.register_blueprint(blueprint=blue_order, url_prefix='/order')

    # 初始化
    db.init_app(app)

    return app




