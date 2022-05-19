import os

from toml_config.core import Config

from cli_panoptes.configuration.ConfigWrapper import ConfigWrapper
from cli_panoptes.threads.FimThread import FimThreadMaster
from cli_panoptes.threads.SaThread import SaThreadMaster
from cli_panoptes.threads.EventThread import EventMaster
from cli_panoptes.threads.SuperThreadMasterOfDoom import SuperThreadMasterOfDoom
from utile import utile_fim
from utile.network import *


def load_configuration_file() -> ConfigWrapper:
    if not os.path.isfile('./configuration/app.config_client.toml'):
        client_configuration = Config('./configuration/app.config_client.toml')
        client_configuration.add_section("GENERAL").set(
            SERVER_IP="127.0.0.1",
            SERVER_PORT=8880,
            CONFIG_SERVER_PORT=8881,
            SCAN_AT_LAUNCH=True,
            PATH="/home/q210079/Desktop/**",
        )
        client_configuration.save()
    else:
        client_configuration = Config('./configuration/app.config_client.toml')

    return ConfigWrapper(client_configuration)


def get_data_from_server(port: int, queue: Queue, proto: Proto):
    data_receiver = DataReceiver(port, queue, proto)
    data = data_receiver.request()
    return data


def main():
    db_filename = 'data/cli_panoptes.sqlite'
    client_configuration = load_configuration_file()
    path_ref_image = client_configuration.value('GENERAL', 'PATH')
    scan_at_launch = client_configuration.value('GENERAL', 'SCAN_AT_LAUNCH')
    srv_port = client_configuration.value('GENERAL', 'SERVER_PORT')
    config_srv_port = client_configuration.value('GENERAL', 'CONFIG_SERVER_PORT')
    srv_ip = client_configuration.value('GENERAL', 'SERVER_IP')

    q = Queue()
    event_thread = EventMaster(q, client_configuration)

    if scan_at_launch:
        ref_images = utile_fim.capture_image_de_reference(path_ref_image)
        q.put([Proto.IMG, ref_images])
        client_configuration.set({'SCAN_AT_LAUNCH': False})
        client_configuration.save()
    else:
        ref_images = get_data_from_server(config_srv_port, q, Proto.LD_IMG)

    config_sa = get_data_from_server(config_srv_port, q, Proto.LD_SA)
    config_fim = get_data_from_server(config_srv_port, q, Proto.LD_FIM)

    sa_thread = SaThreadMaster(config_sa, q)
    fim_thread = FimThreadMaster(config_fim, q, ref_images)
    super_thread = SuperThreadMasterOfDoom(q, client_configuration)

    event_thread.start()
    sa_thread.start()
    fim_thread.start()
    super_thread.start()

    event_thread.join()
    sa_thread.join()
    fim_thread.join()
    super_thread.join()


if __name__ == '__main__':
    main()
