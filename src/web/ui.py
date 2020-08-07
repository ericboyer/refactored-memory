"""Client (web) app that allows user to send text over TCP to remote server.

Usage:
    refactored-memory-ui [--server_port=SERVER_PORT] [--server_ip=SERVER_IP]

"""
from flask import Flask
from flask import render_template
from flask import request
from net import client

app = Flask(__name__)


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
    import docopt
    args = docopt.docopt(__doc__)
    text = request.args.get('value')
    server_ip = args['--server_ip'] or input("Enter server IP: ")
    server_port = args['--server_port']
    c = Client(server_ip, int(server_port))
    client_socket = c.connect()
    c.send(client_socket, text)


if __name__ == "__main__":
    app.run()