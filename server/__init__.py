from flask import Flask
from api.routes import api_routes
from website.routes import website_routes
import os

def init_blueprints(app):
    try:
        #ADD Your App routes here
        app.register_blueprint(api_routes)
        app.register_blueprint(website_routes)
        print('Registration Initialized')
    except Exception as e:
        print(e)
        print('Registration is NOT Initialized')
        raise

def init_config(app):
    os.environ.setdefault('CORE_ENV', 'server.config.DevelopmentConfig')
    try:
        app.config.from_object(os.environ['CORE_ENV'])
        print('Config Initialized')
    except Exception as e:
        print(e)
        print('Config NOT initialized')
        raise

def init_app():
    try:
        app = Flask(__name__)
        init_blueprints(app)
        init_config(app)
        print('App Initialized')
        return app
    except Exception as e:
        print(e)
        print('App is NOT Initialized')
        raise