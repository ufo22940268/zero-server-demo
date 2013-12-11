#! ../env/bin/python
#coding:utf-8
import os

from flask import Flask
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.cache import Cache
from flask.ext.admin.form import Select2Widget
from flask.ext.admin.contrib.pymongo import ModelView, filters
from flask.ext.pymongo import PyMongo
from flask.ext.babelex import Babel
from wtforms import form, fields
from appname.model.operator_model import *

from appname import assets
from appname.models import db

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()
mongo = PyMongo()

def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env
    
    #init the cache
    cache.init_app(app)

    #init SQLAlchemy
    db.init_app(app)
    
    # connect to the database
    mongo.init_app(app)
    
    # init admin views
    import flask.ext.admin
    admin = flask.ext.admin.Admin(app, u'用户管理系统')
    babel = Babel(app)
    @babel.localeselector
    def get_locale():
        return 'zh'
    with app.app_context():
        admin.add_view(OperatorView(mongo.db.operator, u'专员管理'))

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)

    # register our blueprints
    from controllers.main import main
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('appname.settings.%sConfig' % env.capitalize(), env=env)

    app.run()
