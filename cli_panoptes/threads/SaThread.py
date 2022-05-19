import subprocess
import threading
import time
from queue import Queue
from utile.network import Proto


class SaThreadMaster(threading.Thread):
    def __init__(self, config_sa: any, queue: Queue):
        super().__init__()
        self.daemon = True

        self.config_sa = config_sa
        self.queue = queue
        self.threads = []

    def run(self):

        for row in self.config_sa:
            slave = SaThreadSlave(row, self.queue)
            self.threads.append(slave)
            slave.start()

        run = len(self.threads) == 0

        while run:
            run = False
            for thread in self.threads:
                run = thread.isAlive()

        for thread in self.threads:
            thread.join()

    def stop(self):
        for thread in self.threads:
            thread.stop()


class SaThreadSlave(threading.Thread):
    def __init__(self, sa_config: any, queue: Queue):
        super().__init__()
        self.daemon = True

        self.sa_config = sa_config
        self.sa_set_id = sa_config[0]
        self.sa_job_id = sa_config[1]
        self.sa_set_name = sa_config[2]
        self.schedule = self.sa_config[3]
        self.sa_job_name = self.sa_config[4]
        self.command_script = self.sa_config[5]
        self.expected_result = self.sa_config[6]
        self.alert_message = self.sa_config[7]
        self.running = True

        self.queue = queue

    def run(self):
        print("oui", self.sa_job_name)
        while True:
            # Executer la commande
            run = subprocess.Popen(self.command_script, shell=True, stdout=subprocess.PIPE)
            result_command = (run.stdout.read()).decode()

            # Determiner s'il y a une erreur -> resultat != expected
            # Passer l'information à la collection synchronisée
            if result_command.strip("\n") != self.expected_result.strip("\n"):
                infos = f"Erreur, {self.sa_job_name} est inactif"  # {}
                print(infos)
                insertion = [self.sa_set_id, self.sa_job_id]
                event = [Proto.SA_EVENT, insertion]
                self.queue.put(event)

            # Sleep
            time.sleep(self.schedule)
            # /!\ Le sleep doit être modifier avec les données de la BD /!\

    def stop(self):
        self.running = False
