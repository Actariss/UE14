import datetime
import threading
from queue import Queue

from utile import utile_data as data
from utile.Proto import Proto


class EventMaster(threading.Thread):
    def __init__(self, queue: Queue, db_name: str):
        super().__init__()

        self.daemon = True
        self.queue = queue
        self.db_conn = data.connect_db(db_name)

    def run(self):
        while True:
            if not self.queue.empty():
                data_pickled = self.queue.get()

                # TODO verify et pickle.load()
                event = []

                protocol = event[0]
                infos = event[1]

                if protocol == Proto.SA_EVENT:
                    date = str(datetime.datetime.now())
                    data.simple_insert_db(self.db_conn,
                                          f"INSERT INTO sa_events (sa_set_id, sa_job_id, datetime_event, except_active)"
                                          f" VALUES (?,?,?,?)", (infos[0], infos[1], date, True))
                    # Insert into SA_Event

                elif protocol == Proto.FIM_EVENT:
                    date = str(datetime.datetime.now())
                    for erreur in infos:
                        data.simple_insert_db(self.db_conn,
                                              f"INSERT INTO fim_events (fim_set_id, fim_rule_id, image_id, file_inode, datetime_event, except_msg, except_active)"
                                              f" VALUES (?,?,?,?,?,?,?)", (1, 1, 1, 1, date, erreur, True))

                    # Insert into FIM_Event
                elif protocol == Proto.STAT:
                    # VALUES car les données passées sont sous la forme [inode]:[file_info]
                    for file_infos in infos.values():
                        data.insert_db('stat_files', file_infos)

                elif protocol == Proto.IMG:
                    # VALUES car les données passées sont sous la forme [inode]:[file_info]
                    for file_infos in infos.values():
                        data.insert_db('ref_images', file_infos)

                elif protocol == Proto.LD_SA:

                    pass

                elif protocol == Proto.LD_FIM:

                    pass

                elif protocol == Proto.LD_IMG:

                    pass
