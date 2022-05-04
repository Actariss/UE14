from queue import Queue

from cli_panoptes.threads.EventThread import EventMaster
from cli_panoptes.threads.FimThread import FimThreadMaster
from cli_panoptes.threads.SaThread import SaThreadMaster
from utile import utile_data, utiles_fim


def main():
    db_filename = 'data/cli_panoptes.sqlite'
    db_conn = utile_data.connect_db(db_filename)

    # delete pour repartir sur des bonnes bases

    config_sa = utile_data.select_db(db_conn, 'select sa_set_id, se.sa_job_id, sa_set_name, schedule, sa_job_name, command_script, expected_result, alert_message from sa_sets se join sa_jobs sj on se.sa_job_id = sj.sa_job_id', ())
    config_fim = utile_data.select_db(db_conn, 'SELECT  * FROM fim_rules ru join fim_sets fs on ru.fim_rule_id = fs.fim_rule_id')

    db_conn.close()

    q = Queue()

    event_thread = EventMaster(q, db_filename)

    utiles_fim.capture_image_de_reference('/home/q210079/Desktop/**')

    sa_thread = SaThreadMaster(config_sa, q)
    fim_thread = FimThreadMaster(config_fim, q)

    event_thread.start()
    sa_thread.start()
    fim_thread.start()

    event_thread.join()
    sa_thread.join()
    fim_thread.join()


if __name__ == '__main__':
    main()
