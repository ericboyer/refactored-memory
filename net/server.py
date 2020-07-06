import socket
import threading


class Server:
    def __init__(self, ip, port):
        self.bind_ip = ip
        self.bind_port = port

    def handle_client_connection(self, client_socket):
        request = client_socket.recv(1024)
        print('Received {}'.format(request))
        response = "hello"
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.bind_ip, self.bind_port))
        s.listen(5)  # max backlog of connections

        print("Listening on {}:{}".format(self.bind_ip, self.bind_port))

        while True:
            client_socket, address = s.accept()
            print("Accepted connection from {}:{}".format(address[0], address[1]))
            t = threading.Thread(
                target=self.handle_client_connection,
                # without comma you'd get a... TypeError: handle_client_connection() argument after
                # * must be a sequence, not _socketobject
                args=(client_socket,)
            )
            t.start()

if __name__ == '__main__':
    # read IP/port values from env SERVER_IP and SERVER_PORT
    import os
    server = Server('0.0.0.0', int(os.environ['SERVER_PORT']))
    server.run()
