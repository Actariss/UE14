import pickle
import socket
import threading
from _thread import start_new_thread
from queue import Queue

from utile.Proto import Proto, verify


class DataReceiver:
    def __init__(self, port: int, queue: Queue, proto: Proto):
        self.ip = get_local_ip()
        self.port = port
        self.queue = queue
        self.proto = proto
        # TODO self.client_email = client_email

    def request(self):
        with socket.socket() as client_side_socket:
            print(self.ip)
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


class ConThreadServer(threading.Thread):
    """
    Cette classe permet de gérer les connections effectuées par les clients sur le serveur
    methods:
        run:
            Démarre le thread permettant d'écouter les connections clients
        multi_threaded_client:
            Récupère les informations envoyées par le client et les envoie dans la queue
    """
    def __init__(self, port: int, q: Queue):
        threading.Thread.__init__(self)
        self.ip = get_local_ip()
        self.port = port
        self.queue = q

    def run(self):
        """Démarre le thread permettant d'écouter les connections clients"""
        try:
            server_side_socket = socket.socket()
            server_side_socket.bind((self.ip, self.port))
            server_side_socket.listen()

            print(f'[SERVER_STARTER]Server started on {self.ip} port {self.port} !')

            while True:
                (clientConnection, clientAddress) = server_side_socket.accept()
                start_new_thread(self.multi_threaded_client, (clientConnection, clientAddress))
        except IOError as e:
            print(f"[SERVER_STARTER]An error occurred : {e}")

    def multi_threaded_client(self, socket_to_client, client_address):
        """Récupère les informations envoyées par le client et les envoie dans la queue"""
        try:
            received = socket_to_client.recv(20)
            length = int.from_bytes(received[0:4], 'big')
            received += socket_to_client.recv(length)

            if received and verify(received):
                print(f"[CLIENT_HANDLER]Receiving valid data from {client_address} : {received}")
                event = pickle.loads(received[20:])
                self.queue.put(event)

        except IOError as e:
            print(f'[CLIENT_HANDLER]An error occurred : {e}')
            socket_to_client.close()

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

