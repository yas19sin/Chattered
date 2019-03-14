import threading
import socket

HOST = ''
PORT = 9000
clients = set()
names = {}


def sendMsg(msg):
    for clt in clients:
        if clt is not None:
            clt.sendall(msg.encode())


def handle(c, address):
    name = c.recv(256)
    names[address[1]] = name.decode()
    c.sendall('Welcome to the server {username}'.format(username=names[address[1]]).encode())
    print('Client {username} Connected'.format(username=names[address[1]]))
    sendMsg('Client {username} Connected'.format(username=names[address[1]]))
    clients.add(c)
    while True and c is not None:
        try:
            data = c.recv(1024)
            if data is None:
                break
            else:
                msg = 'Client {username}: '.format(username=names[address[1]]) + data.decode()
                sendMsg(msg)
                print(msg)
                data = None
        except:
            print('Client {username} Disconnected'.format(username=names[address[1]]))
            clients.remove(c)
            sendMsg('Client {username} Disconnected'.format(username=names[address[1]]))
            del names[address[1]]
            c.close()
            break


class Server(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket()
        print(self.hostname)
        # self.socket.bind((self.hostname, self.port))
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(10)

        while True:
            threading.Thread(target=handle, args=(self.socket.accept())).start()


if __name__ == '__main__':
    server = Server(hostname=HOST, port=PORT)
    server.start()
