#!/usr/bin/env python3
'''
Module for the basic babel setup
'''
from flask import Flask, render_template, request
from flask_babel import Babel, _
from typing import Union


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
def get_locale() -> Union[str, None]:
    '''
    Selects the best match for supported languages based on
    the client's request.
    '''
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    '''
    Method handles the rendering of the index template
    '''
    return render_template('3-index.html',
                           home_title=_("home_title"),
                           home_header=_("home_header"))


if __name__ == '__main__':
    app.run(debug=True)
