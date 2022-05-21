import os

from threads.EventThread import EventMaster

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
    server_configuration = load_configuration_file()
    server_port = server_configuration.value("GENERAL", "SERVER_PORT")
    db_name = server_configuration.value("GENERAL", "DB_NAME")

    q = Queue()
    client_handler = ConThreadServer(server_port, q)
    client_handler.start()
    print('client handler lancé')
    event_thread = EventMaster(q, db_name)
    event_thread.start()
    print("event thread lancé")
    client_handler.join()
    event_thread.join()

if __name__ == '__main__':
    main()
