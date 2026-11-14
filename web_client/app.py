from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/problem')
def problem():
    return render_template('problem.html')