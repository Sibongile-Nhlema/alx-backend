#!/usr/bin/env python3
'''
The module for the Flask Appication
'''
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    '''
    Method handles the rendering of the index template
    '''
    return render_template('0-index/html')


if __name__ = '__main__':
    app.run(debug=True)
