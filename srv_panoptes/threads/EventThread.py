import threading
from queue import Queue

from utile import utile_data


class EventMaster(threading.Thread):
    def __init__(self, queue: Queue, db_name: str):
        super().__init__()

        self.daemon = True
        self.queue = queue
        self.db_conn = utile_data.connect_db(db_name)

    def run(self) -> None:
        pass
