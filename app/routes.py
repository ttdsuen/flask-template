from flask import request
from flask_restful import Resource


class Greetings(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')


    def get(self):
        # get query param x, returns None if query param x is not defined
        # x = request.args.get('x')

        # get query param x, return a 400 if query param x is not defined
        # x = request.args['x']

        # get request body
        # req_payload = request.get_json()

        return {
            'hello': 'world'
        }, 200
