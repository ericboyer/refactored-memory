import socket, sys, traceback


class Client:
    def __init__(self, ip, port):
        self.server_ip = ip
        self.server_port = port

    def run(self):
        try:
            while True:
                # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # connect the client
                client.connect((self.server_ip, self.server_port))
                # enter string to send
                text = input("Enter text: ")
                if (text == "quit") or (text == "q"):
                    break

                # print text to send
                print(">>> '{}'".format(text))
                # send the data
                client.sendall(text.encode('utf-8'))
                # receive the response data (4096 is recommended buffer size)
                response = client.recv(4096)
                print("<<< '{}'".format(response.decode('utf-8')))
                client.close()
        except Exception:
            print("We had issues talking talking to the server, exiting...")
            traceback.print_exc(file=sys.stdout)
            # traceback.print_stack()
            return -1


if __name__ == '__main__':
    server_ip = input("Enter server IP: ")
    server_port = input("Enter server port: ")
    print("Establishing connection to server running at {}:{}".format(server_ip, server_port))
    print("Enter 'q' or 'quit' to exit")
    c = Client(server_ip, int(server_port))
    c.run()
