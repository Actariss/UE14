import os

from threads import EventThread

from toml_config.core import Config

from srv_panoptes.configuration.ConfigWrapper import ConfigWrapper
from utile.network import *


def load_configuration_file() -> ConfigWrapper:
    if not os.path.isfile('./configuration/app.config_server.toml'):
        server_configuration = Config('./configuration/app.config_server.toml')
        server_configuration.add_section("GENERAL").set(SERVER_PORT=8880,
                                                        DB_NAME="./data/srv_panoptes.sqlite")
        server_configuration.save()
    else:
        server_configuration = Config('./configuration/app.config_server.toml')

    return ConfigWrapper(server_configuration)


def main():
    client_configuration = load_configuration_file()
    server_port = client_configuration.value("GENERAL", "SERVER_PORT")
    db_name = client_configuration.value("GENERAL", "DB_NAME")
    q = DataReceiver(server_port, "192.168.1.7")
    EventThread.EventMaster(q, db_name)


if __name__ == '__main__':
    main()
