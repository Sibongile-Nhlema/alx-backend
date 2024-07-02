#!/usr/bin/env python3
'''
Module for the basic babel setup
'''
from flask import Flask, render_template
from flask_babel import Babel


class Config:
    '''
    Class that handles configuration of availiable languages
    '''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@app.route('/')
def index():
    '''
    Method handles the rendering of the index template
    '''
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
