import os

from toml_config.core import Config

from srv_panoptes.configuration.ConfigWrapper import ConfigWrapper


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

    pass

if __name__ == '__main__':
    main()