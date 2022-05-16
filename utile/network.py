import pickle
import socket
import threading
from queue import Queue

from utile.Proto import Proto, verify


class ConfigReceiver:
    def __init__(self, port: int, queue: Queue, proto: Proto):
        self.ip = get_local_ip()
        self.port = port
        self.queue = queue
        self.proto = proto
        # TODO self.client_email = client_email

    def run(self):
        client_side_socket = socket.socket()
        client_side_socket.bind((self.ip, self.port))
        client_side_socket.listen()

        try:
            self.queue.put([self.proto, [self.ip, self.port]])

            (server_connection, server_address) = client_side_socket.accept()

            received = server_connection.recv(20)
            length = int.from_bytes(received[0:4], 'big')
            received += server_connection.recv(length)

            if received and verify(received):
                print(f"[CONFIG]Receiving valid data from {server_address} : {received}")
                config = pickle.loads(received[20:])
                return config

            return {}

        except IOError as e:
            print(f'[CONFIG_RECEIVER]An error occurred while fetching configuration: {e}')


class ImgReceiver:

    def __init__(self, port: int):#, queue: Queue, proto: Proto):
        self.ip = get_local_ip()
        self.port = port
        # self.queue = queue
        # self.proto = proto
        # self.client_email = client_email

    def run(self):
        client_side_socket = socket.socket()
        client_side_socket.bind((self.ip, self.port))
        client_side_socket.listen()

        try:
            # self.queue.put([self.proto, [self.ip, self.port]])
            # todo demander a Fred
            (server_connection, server_address) = client_side_socket.accept()

            received = server_connection.recv(20)
            length = int.from_bytes(received[0:4], 'big')
            received += server_connection.recv(length)

            if received and verify(received):
                print(f"[IMG]Receiving valid data from {server_address} : {received}")
                images = pickle.loads(received[20:])
                return images

            return {}

        except IOError as e:
            print(f'[IMG_RECEIVER]An error occurred while fetching images: {e}')


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

