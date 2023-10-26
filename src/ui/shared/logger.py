import coloredlogs, logging

# set up a logger class
class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        coloredlogs.install(level='DEBUG', logger=self.logger)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        """self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)"""

        self.fh = logging.FileHandler('logs.log')
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def get_logger(self):
        return self.logger
    