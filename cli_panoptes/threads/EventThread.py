import queue
import threading
from queue import Queue

from cli_panoptes.configuration.ConfigWrapper import ConfigWrapper
from utile import utile_data
from utile.Proto import pickler
from utile.network import DataSender


class EventMaster(threading.Thread):
    def __init__(self, q: Queue, client_configuration: ConfigWrapper):
        super().__init__()

        self.daemon = True
        self.running = True
        self.queue = q
        self.client_configuration = client_configuration
        self.server_ip = client_configuration.value("GENERAL", "SERVER_IP")
        self.server_port = client_configuration.value("GENERAL", "SERVER_PORT")

    def run(self) -> None:
        while self.running:
            try:
                print("[cli_event] q is empty")
                while not self.queue.empty():
                    print("[cli_event] Quelquechose dans la q")
                    event = self.queue.get()

                    pickled = pickler(event)

                    socket = DataSender(self.server_ip, self.server_port, pickled)
                    socket.start()
                    socket.join()

            except IOError as e:
                print(f'[EVENT_THREAD_MASTER]An error occurred in EVThread : {e}')

    def kill(self):
        self.running = False