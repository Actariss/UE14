import threading

from queue import Queue
from time import sleep

from cli_panoptes.configuration.ConfigWrapper import ConfigWrapper
from cli_panoptes.threads.EventThread import EventMaster
from cli_panoptes.threads.FimThread import FimThreadMaster
from cli_panoptes.threads.SaThread import SaThreadMaster
from utile.network import DataReceiver
from utile.Proto import Proto


class SuperThreadMasterOfDoom(threading.Thread):
    def __init__(self, q: Queue, client_configuration: ConfigWrapper, timeout: int = 60):
        super().__init__()

        self.daemon = True
        self.queue = q
        self.client_configuration = client_configuration
        self.config_server_port = self.client_configuration.value('GENERAL', 'CONFIG_SERVER_PORT')
        self.timeout = timeout

        # SETUP CONFIG FROM SERVER
        self.last_sa_config = None
        self.last_fim_config = None
        self.last_ref_images = None

        self.ev_master = EventMaster(q, client_configuration)
        self.ev_master.start()

        while self.last_sa_config is None or self.last_fim_config is None or self.last_ref_images is None:
            self.last_sa_config = DataReceiver(self.config_server_port, q, Proto.LD_SA).request()

            self.last_fim_config = DataReceiver(self.config_server_port, q, Proto.LD_FIM).request()

            self.last_ref_images = DataReceiver(self.config_server_port, q, Proto.LD_IMG).request()

        self.sa_master = SaThreadMaster(q, self.last_sa_config)
        self.fim_master = FimThreadMaster(q, self.last_fim_config, self.last_ref_images)

    def run(self):
        """Permet de démarrer le thread"""
        self.sa_master.start()
        self.fim_master.start()

        while self.ev_master.is_alive() or self.sa_master.is_alive() or self.fim_master.is_alive():
            sleep(self.timeout)

            new_sa_config = DataReceiver(self.config_server_port, self.queue, Proto.LD_SA).request()

            new_fim_config = DataReceiver(self.config_server_port, self.queue, Proto.LD_FIM).request()

            new_ref_images = DataReceiver(self.config_server_port, self.queue, Proto.LD_IMG).request()

            if self.last_sa_config != new_sa_config:
                print(f'[HOT_RELOAD_CONFIG]New version of sa_config from server !!')
                self.sa_reload(new_sa_config)

            if self.last_fim_config != new_fim_config or self.last_ref_images!= new_ref_images:
                print(f'[HOT_RELOAD_CONFIG]New version of fim_config from server !!')
                self.fim_reload(new_fim_config, new_ref_images)

        self.sa_master.join()
        self.fim_master.join()
        self.ev_master.join()

    def sa_reload(self, new_sa_config):
        self.sa_master.stop()
        self.last_sa_config = new_sa_config

        threadsa = SaThreadMaster(self.last_sa_config, self.queue)
        threadsa.start()

    def fim_reload(self, new_fim_config, new_ref_images):
        self.fim_master.stop()
        self.last_fim_config = new_fim_config
        self.last_ref_images = new_ref_images

        threadfim = FimThreadMaster(self.last_fim_config, self.queue, self.last_ref_images)
        threadfim.start()


