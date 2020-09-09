"""Server that echos text sent from client over TCP.

Usage:
    refactored-memory-server [--port=BIND_PORT]

"""
import socket, threading, sys, traceback


# static method for handling client connection
def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print(">>> '{}'".format(request))
    response = "{}".format(request)
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()


def main():
    import os, docopt
    args = docopt.docopt(__doc__)
    # read port parameter or from BIND_PORT environment variable
    server_port = args['--port'] or os.environ['BIND_PORT']
    server = Server('0.0.0.0', int(server_port))
    server.run()


class Server:
    def __init__(self, ip, port):
        self.bind_ip = ip
        self.bind_port = port

    def run(self):
        try:
            # bind to ip/port and listen
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.bind_ip, self.bind_port))
            s.listen(5)  # max backlog of connections

            print("Listening on {}:{}".format(self.bind_ip, self.bind_port))

            while True:
                # accept incoming connections (max 5)
                client_socket, address = s.accept()
                print("Accepted connection from {}:{}".format(address[0], address[1]))
                t = threading.Thread(
                    target=handle_client_connection,
                    # without comma you'd get a... TypeError: handle_client_connection() argument after
                    # * must be a sequence, not _socketobject
                    args=(client_socket,)
                )
                t.start()
        except Exception:
            traceback.print_exc(file=sys.stdout)
        finally:
            print('Closing connection')
            if not client_socket is None:
                client_socket.close()
                

if __name__ == '__main__':
    main()
