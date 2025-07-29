from tabulate import tabulate
from utils.logger import simple_logger

class TableFormatter:
    def __init__(self, logger):
        self.logger = logger


    @simple_logger
    def format(self, data: list[list], headers: list[str]) -> str:
        return tabulate(data, headers=headers, tablefmt="grid")