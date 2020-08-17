"""Client (console) app that allows user to send text over TCP to remote server.

Usage:
    refactored-memory-client [--server_port=SERVER_PORT] [--server_ip=SERVER_IP]

"""
import socket, sys, traceback


def main():
    import docopt
    args = docopt.docopt(__doc__)
    server_ip = args['--server_ip'] or input("Enter server IP: ")
    server_port = args['--server_port'] or input("Enter server port: ")
    print("Establishing connection to server running at {}:{}".format(server_ip, server_port))
    print("Enter 'q' or 'quit' to exit")
    c = Client(server_ip, int(server_port))
    c.run()


def send(client, text):
    # print text to send
    print(">>> '{}'".format(text))
    # send the data
    client.sendall(text.encode('utf-8'))
    # receive the response data (4096 is recommended buffer size)
    response = client.recv(4096).decode('utf-8')
    print("<<< '{}'".format(response))
    client.close()
    return response


class Client:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port

    def connect(self):
        # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect the client
        client_socket.connect((self.server_ip, self.server_port))
        return client_socket

    def run(self):
        try:
            while True:
                # enter string to send
                text = input("Enter text: ")
                if (text == "quit") or (text == "q"):
                    break

                client_socket = self.connect()
                send(client_socket, text)
        except Exception:
            print("We had issues talking to the server, exiting...")
            traceback.print_exc(file=sys.stdout)
            # traceback.print_stack()
            return -1


if __name__ == '__main__':
    main()
