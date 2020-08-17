"""Client (web) app that allows user to send text over TCP to remote server. Config values
are passed as environment variables.

Usage:
    refactored-memory-rest-client

"""
import os
from typing import Final

from flask import Flask
from flask import render_template
from flask import request
from refactored_memory.net.client import Client, send

SERVER_IP: Final = os.environ['SERVER_IP']
SERVER_PORT: Final = os.environ['SERVER_PORT']

app = Flask(__name__)


def main():
    print("initializing server connection @ {}:{}".format(SERVER_IP, SERVER_PORT))
    app.run()


@app.route('/health')
def health():
    return 'UP'


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/hello')
def hello_name():
    return 'Hello {}!'.format(request.args.get('name'))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/text')
def send_text():
    text = request.args.get('value')
    c = Client(SERVER_IP, int(SERVER_PORT))
    client_socket = c.connect()
    response = send(client_socket, text)
    return "Response: {}".format(response)


if __name__ == "__main__":
    main()
