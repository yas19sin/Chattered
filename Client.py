import sys
import socket
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QTextBrowser, QWidget, QFormLayout

HOST = 'localhost'
PORT = 9000


class ClientUI(QMainWindow):
    def __init__(self, host, port, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.HOST = host
        self.PORT = port
        self.sock = None
        self.setupUi()

    def setupUi(self):

        # Extra Vars:
        # self.Connected = False

        self.setGeometry(50, 50, 500, 500)
        self.setFixedSize(500, 500)
        self.setWindowTitle('Client')

        centralWidget = QWidget(self)
        # layout = QFormLayout()
        # centralWidget.setLayout(layout)

        self.Logger = QTextBrowser()
        self.Logger.setParent(centralWidget)
        self.Logger.setGeometry(100, 100, 300, 150)
        # self.layout().addWidget(self.Logger)
        # self.Logger.setEnabled(False)

        self.inputField = QLineEdit()
        self.inputField.setParent(centralWidget)
        self.inputField.setGeometry(125, 300, 250, 30)
        self.inputField.setText('')
        # self.layout().addWidget(self.inputField)

        self.disconBtn = QPushButton('Disconnect | Ctrl+D')
        self.disconBtn.setParent(centralWidget)
        self.disconBtn.setGeometry(40, 350, 110, 30)
        self.disconBtn.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_D))
        self.disconBtn.clicked.connect(self.disconnecting)
        self.disconBtn.setEnabled(False)
        # self.layout().addWidget(self.disconBtn)

        self.SendBtn = QPushButton('Send | Enter')
        self.SendBtn.setParent(centralWidget)
        self.SendBtn.setGeometry(150, 350, 100, 30)
        self.SendBtn.setShortcut(QKeySequence(Qt.Key_Enter))
        self.SendBtn.clicked.connect(self.sendMsg)
        self.SendBtn.setEnabled(False)
        # self.layout().addWidget(self.SendBtn)

        self.conBtn = QPushButton('Connect | Ctrl+C')
        self.conBtn.setParent(centralWidget)
        self.conBtn.setGeometry(250, 350, 100, 30)
        self.conBtn.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_C))
        self.conBtn.clicked.connect(self.connect)
        # centralWidget.layout().addWidget(self.conBtn)

        self.setCentralWidget(centralWidget)

        self.show()

    def disconnecting(self):
        self.Logger.append('Disconnecting...')
        self.sock.close()
        self.conBtn.setEnabled(True)
        self.SendBtn.setEnabled(False)
        self.disconBtn.setEnabled(False)
        self.msgReader.exit()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.myclient(HOST, PORT)

    def myclient(self, ip, port):
        try:
            print('Attempting connection')
            self.sock.connect((ip, port))
        except:
            print('Couldn\'t find the server!!')
            self.Logger.append('Couldn\'t find the server!!')
            return
        self.conBtn.setEnabled(False)
        self.SendBtn.setEnabled(True)
        self.disconBtn.setEnabled(True)
        self.Logger.append('Connected to the Server!')
        self.msgReader = Reader(self.sock)
        self.msgReader.signal_result.connect(self.handleMsgLogging)
        self.msgReader.start()

    def handleMsgLogging(self, result):
        self.Logger.append(result)

    def sendMsg(self):
        message = self.inputField.text()
        print(message)
        while True:
            try:
                if message != '':
                    self.sock.sendall(message.encode())
                    message = ''
                else:
                    break
            except:
                self.Logger.append('Either Server Closed or an Error accrued please restart the client!!')
                # self.Connected = False
                print('Either Server Closed or an Error accrued please restart the client!!')
                break
                # raise SystemExit


class Reader(QThread):
    signal_result = pyqtSignal(object)

    def __init__(self, sock):
        QThread.__init__(self)
        self.sock = sock
        print('made the thread')

    def run(self):
        while True:
            try:
                result = self.sock.recv(1024)
                self.signal_result.emit(result.decode())
                # self.Logger.append(result.decode())
                print(result.decode())
            except:
                print('Lost Connection!')
                result = 'Lost Connection'
                self.signal_result.emit(result)
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)

    client = ClientUI(HOST, PORT)

    sys.exit(app.exec_())
