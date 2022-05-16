import datetime
import threading
from queue import Queue
from utile.utile_data import select_db
from utile import utile_data as data
from utile.Proto import *
import pickle
from utile import network


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
                len, crc = verify(data_pickled)
                data = data_pickled[:20]
                if len and crc:
                    event = [pickle.load(data)]
                # TODO verify et pickle.load()
                else:
                    print("Il y a eu un problème pendant l'envoi")
                    pass
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
                    config_sa = data.select_db(self.db_conn,
                                               'SELECT sa_set_id, se.sa_job_id, sa_set_name, schedule, sa_job_name, command_script, expected_result, alert_message FROM sa_sets se JOIN sa_jobs sj ON se.sa_job_id = sj.sa_job_id',
                                               ())

                    pass

                elif protocol == Proto.LD_FIM:

                    pass

                elif protocol == Proto.LD_IMG:
                    ref_images = {}
                    tuples_ref_images = data.select_db(self.db_conn,
                                                       'SELECT max(datetime_image), * FROM ref_images GROUP BY '
                                                       'file_inode',
                                                       ())
                    for row in tuples_ref_images:
                        file_infos = {}
                        file_infos['file_inode'] = row[2]
                        file_infos['parent_id'] = row[4]
                        file_infos['file_name'] = row[5]
                        file_infos['file_type'] = row[6]
                        file_infos['file_mode'] = row[7]
                        file_infos['file_nlink'] = row[8]
                        file_infos['file_uid'] = row[9]
                        file_infos['file_gid'] = row[10]
                        file_infos['file_size'] = row[11]
                        file_infos['file_atime'] = row[12]
                        file_infos['file_mtime'] = row[13]
                        file_infos['file_ctime'] = row[14]
                        file_infos['file_md5'] = row[15]
                        file_infos['file_SHA1'] = row[16]
                        ref_images[str(row[2])] = file_infos

                    network.DataSender(infos[0],infos[1],pickler(ref_images))
                    #todo le client evoi le host et le port au serveur, celui-ci le met ici au dessus
                    pass
