import json
import os
import logging
import logging.config

from flask import Flask, make_response
from flask_restful import Api

from . import routes


def create_app(test_config=None):
    # setup logging
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': 'logs/app.log',
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5,
            }
        },
        'root': {
            'handlers': [ 'file', ]
        }
    })

    # overwrite if necessary
    api_prefix = '/api/v1'

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        API_PREFIX=api_prefix
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello, plain Flask style
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'

    # Flask RESTful style
    api = Api(app)
    api.add_resource(
        routes.Greetings, f'{api_prefix}/greetings',
        resource_class_kwargs={ 'logger': app.logger }
    )

    # auto convert to json in response
    @api.representation('application/json')
    def ouptut_json(data, code, headers=None):
        resp = make_response(json.dumps(data), code)
        resp.headers.extend(headers or {})
        return resp

    return app
