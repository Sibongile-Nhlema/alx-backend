#!/usr/bin/env python3
'''
Module for the basic babel setup
'''
from flask import Flask, render_template, request
from flask_babel import Babel, _


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


@babel.localeselector
def get_locale():
    '''
    Selects the best match for supported languages based on
    the client's request.
    '''
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    '''
    Method handles the rendering of the index template
    '''
    return render_template('2-index.html',
                           home_title=_("home_title"),
                           home_header=_("home_header"))


if __name__ == '__main__':
    app.run(debug=True)
