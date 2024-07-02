#!/usr/bin/env python3
'''
Module for the basic babel setup
'''
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)


class Config:
    '''
    Class that handles configuration of availiable languages
    '''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


def get_user(user_id):
    '''
    Checks if the user is in the mock database
    '''
    return users.get(user_id)


@app.before_request
def before_request():
    '''
    should use get_user to find a user if any,
    and set it as a global on flask.g.user
    '''
    login_as = request.args.get('login_as')
    if login_as:
        user_id = int(login_as)
        g.user = get_user(user_id)
    else:
        g.user = None


@babel.localeselector
def get_locale():
    '''
    Selects the best match for supported languages based on
    the client's request.
    '''
    # 1. find locale from URL parameter
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. find locale from user settings
    if g.user and 'locale' in g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # 3. find locale from request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    '''
    Method handles the rendering of the index template
    '''
    return render_template('5-index.html',
                           home_title=_("home_title"),
                           home_header=_("home_header"))


if __name__ == '__main__':
    app.run(debug=True)
