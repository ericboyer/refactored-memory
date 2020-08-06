from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/hello')
def hello_name():
    return 'Hello {}'.format(request.args.get('name'))

@app.route('/')
def hello_world():
    return 'Hello World!'