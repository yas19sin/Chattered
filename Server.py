import threading
import socket

HOST = ""
PORT = 9000
clients = set()


def handle(c, address):
    clients.add(c)
    c.sendall('Welcome to the server'.encode())
    print('Client {id} Connected'.format(id=address[1]))
    while True and c is not None:
        try:
            data = c.recv(1024)
            if data is None:
                break
            else:
                msg = 'Client {id}: '.format(id=address[1]) + data.decode()
                for clt in clients:
                    clt.sendall(msg.encode())
                print(msg)
                data = None
        except:
            print('Client {id} Disconnected'.format(id=address[1]))
            clients.remove(c)
            c.close()
            break


class Server(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(5)

        while True:
            threading.Thread(target=handle, args=(self.socket.accept())).start()


if __name__ == '__main__':
    server = Server(hostname=HOST, port=PORT)
    server.start()
