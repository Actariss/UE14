import threading
import time
from queue import Queue

from utile.network import Proto

from utile import utile_fim


class FimThreadMaster(threading.Thread):

    def __init__(self, config_fim: any, queue: Queue, ref_images: dict):
        super().__init__()
        self.daemon = True

        self.config_fim = config_fim
        self.queue = queue
        self.ref_images = ref_images

    def run(self):
        threads = []

        for row in self.config_fim:
            slave = FimThreadSlave(row, self.queue, self.ref_images)
            threads.append(slave)
            slave.start()

        run = len(threads) == 0

        while run:
            run = False
            for thread in threads:
                run = thread.isAlive()

        for thread in threads:
            thread.join()


class FimThreadSlave(threading.Thread):
    def __init__(self, fim_config, queue: Queue, ref_images: dict):
        super().__init__()
        self.daemon = True

        self.queue = queue
        self.fim_config = fim_config
        self.ref_images = ref_images
        self.fim_rule_id = fim_config[0]
        self.fim_rule_name = fim_config[1]
        self.path = fim_config[2]
        self.start_indo = fim_config[3]
        self.inode = fim_config[4]
        self.parent = fim_config[5]
        self.name = fim_config[6]
        self.type = fim_config[7]
        self.mode = fim_config[8]
        self.nlink = fim_config[9]
        self.uid = fim_config[10]
        self.gid = fim_config[11]
        self.size = fim_config[12]
        self.atime = fim_config[13]
        self.mtime = fim_config[14]
        self.md5 = fim_config[15]
        self.sha1 = fim_config[16]
        self.ctime = fim_config[17]
        self.fim_set_id = fim_config[18]
        self.fim_set_name = fim_config[20]
        self.schedule = fim_config[21]

    def run(self):
        print(f'Starting thread : {self.path}')
        while True:

            stat_files = utile_fim.capture_image_stat_files(self.path)
            self.queue.put([Proto.STAT, stat_files])

            # TODO pas sur de l'index [2:17]
            info = utile_fim.compare_image(stat_files, self.ref_images, [self.fim_config[2:17]])

            if info is not None:
                self.queue.put([Proto.FIM_EVENT, info])

            time.sleep(self.schedule)
