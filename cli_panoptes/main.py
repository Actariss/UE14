import os
from queue import Queue

from toml_config.core import Config

from cli_panoptes.configuration.ConfigWrapper import ConfigWrapper
from cli_panoptes.threads.EventThread import EventMaster
from cli_panoptes.threads.FimThread import FimThreadMaster
from cli_panoptes.threads.SaThread import SaThreadMaster
from utile import utile_fim, utile_data
from utile.network import Proto

def load_configuration_file() -> ConfigWrapper:
    if not os.path.isfile('./configuration/app.config_client.toml'):
        client_configuration = Config('./configuration/app.config_client.toml')
        client_configuration.add_section("GENERAL").set(
            SERVER_IP="192.168.1.7",
            SERVER_PORT=8880,
            CONFIG_SERVER_PORT=8881,
            SCAN_AT_LAUNCH=True,
            PATH="/home/q210079/Desktop/**",
        )
        client_configuration.save()
    else:
        client_configuration = Config('./configuration/app.config_client.toml')

    return ConfigWrapper(client_configuration)

def get_configuration_from_db(db_filename: str):
    with utile_data.connect_db(db_filename) as db_conn:
        config_sa = utile_data.select_db(db_conn,'SELECT sa_set_id, se.sa_job_id, sa_set_name, schedule, sa_job_name, command_script, expected_result, alert_message FROM sa_sets se JOIN sa_jobs sj ON se.sa_job_id = sj.sa_job_id',())
        config_fim = utile_data.select_db(db_conn,'SELECT  * FROM fim_rules ru JOIN fim_sets fs ON ru.fim_rule_id = fs.fim_rule_id',())

    return config_sa, config_fim

def main():
    db_filename = 'data/cli_panoptes.sqlite'
    client_configuration = load_configuration_file()
    path_ref_image = client_configuration.value('GENERAL', 'PATH')
    q = Queue()

    event_thread = EventMaster(q, db_filename)

    ref_images = utile_fim.capture_image_de_reference(path_ref_image)
    q.put([Proto.IMG, ref_images])

    config_sa, config_fim = get_configuration_from_db(db_filename)
    sa_thread = SaThreadMaster(config_sa, q)
    fim_thread = FimThreadMaster(config_fim, q, ref_images)

    event_thread.start()
    sa_thread.start()
    fim_thread.start()

    event_thread.join()
    sa_thread.join()
    fim_thread.join()


if __name__ == '__main__':
    main()
