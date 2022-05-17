import threading

from queue import Queue

from cli_panoptes.configuration.ConfigWrapper import ConfigWrapper
from utile.network import DataReceiver
from utile.Proto import Proto

class SuperThreadMasterOfDoom(threading.Thread):

    def __int__(self, q : Queue, client_configuration : ConfigWrapper, timeout: int = 60):
        super().__init__()

        self.queue = q
        self.client_configuration = client_configuration
        self.config_server_port = self.client_configuration.value('GENERAL', 'CONFIG_SERVER_PORT')
        self.timeout = timeout

        # SETUP CONFIG FROM SERVER
        self.last_sa_config = None
        self.last_fim_config = None

        self.ev_master = EventThread(q, client_configuration)
        self.ev_master.start()

        while self.last_sa_config is None or self.last_fim_config is None:
            self.last_sa_config = DataReceiver(self.config_server_port, q, Proto.LD_SA).request()

            self.last_fim_config = DataReceiver(self.config_server_port, q, Proto.LD_FIM).request()

        self.sa_master = SaThread(q, self.last_sa_config)
        self.fim_master = FimThread(q, self.last_fim_config)

