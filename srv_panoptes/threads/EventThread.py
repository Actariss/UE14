import datetime

from utile import utile_data as data
from utile.Proto import *
from utile.network import *


class EventMaster(threading.Thread):
    def __init__(self, queue: Queue, db_name: str):
        super().__init__()

        self.daemon = True
        self.queue = queue
        self.db_conn = data.connect_db(db_name)

    def run(self):
        while True:
            if not self.queue.empty():
                print("[srv_event] Packet bien reçus")
                event = self.queue.get()
                protocol = event[0]
                infos = event[1]

                if protocol == Proto.SA_EVENT:
                    date = str(datetime.datetime.now())
                    data.simple_insert_db(self.db_conn,
                                          f"INSERT INTO sa_events (sa_set_id, sa_job_id, datetime_event, except_active)"
                                          f" VALUES (?,?,?,?)", (infos[0], infos[1], date, True))

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
                    pickled_data = pickler(config_sa)
                    data_sender = DataSender(infos[0], infos[1], pickled_data)
                    data_sender.start()
                    data_sender.join()

                elif protocol == Proto.LD_FIM:
                    config_fim = data.select_db(self.db_conn,
                                                'SELECT  * FROM fim_rules ru JOIN fim_sets fs ON ru.fim_rule_id = fs.fim_rule_id',
                                                ())
                    pickled_data = pickler(config_fim)
                    data_sender = DataSender(infos[0], infos[1], pickled_data)
                    data_sender.start()
                    data_sender.join()

                elif protocol == Proto.LD_IMG:
                    ref_images = {}
                    tuples_ref_images = data.select_db(self.db_conn,
                                                       'SELECT max(datetime_image), * FROM ref_images GROUP BY '
                                                       'file_inode',
                                                       ())
                    for row in tuples_ref_images:
                        file_infos = {'file_inode': row[2], 'parent_id': row[4], 'file_name': row[5],
                                      'file_type': row[6], 'file_mode': row[7], 'file_nlink': row[8],
                                      'file_uid': row[9], 'file_gid': row[10], 'file_size': row[11],
                                      'file_atime': row[12], 'file_mtime': row[13], 'file_ctime': row[14],
                                      'file_md5': row[15], 'file_SHA1': row[16]}
                        ref_images[str(row[2])] = file_infos

                    pickled_data = pickler(ref_images)
                    data_sender = DataSender(infos[0],infos[1],pickled_data)
                    data_sender.start()
                    data_sender.join()
