# -*- coding: UTF-8 -*-
"""
flask main function

Author: Bingwei Chen
Date: 2017.07.20
"""
from flask import Flask
from flask_cors import CORS

from peewee import *
from server.database.db import database
from server.route import user_route

app = Flask(__name__, static_url_path='')

CORS(app, supports_credentials=True)

app.register_blueprint(user_route.user_app)


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


def main():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
