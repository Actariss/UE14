import socket
import threading


class DataSender(threading.Thread):

    def __init__(self, host, port, data):
        super().__init__()
        self.port = port
        self.host = host
        self.data = data

    def run(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(self.data)
        except IOError as e:
            print(f"Erreur {e}")


class DataReceiver(threading.Thread):

    def __init__(self, port, host):
        super().__init__()
        self.port = port
        self.host = host

    def run(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
        except IOError as e:
            print(f"Erreur {e}")


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())
