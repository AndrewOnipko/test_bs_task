import logging
import os
import sys
from controllers.main_controller import MainController
from services.auth_service import AuthService
from services.db_service import DBService
from clients.http_client import HTTPClient
from parsers.table_parser import TableParser
from utils.table_formatter import TableFormatter
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('user')
PASSWORD = os.getenv('password')
URL = os.getenv('url')
script_name = os.path.basename(__file__)
script_path = os.path.abspath(sys.argv[0])
file_directory = os.path.dirname(script_path)
log_file = os.path.join(file_directory, 'logs.log')


formatter = logging.Formatter('%(asctime)s - %(message)s')

logging.basicConfig(level=logging.DEBUG,
                    handlers=[
                        logging.FileHandler(log_file, encoding='utf-8', mode='w'),
                        logging.StreamHandler()
                    ])

for handler in logging.getLogger().handlers:
    handler.setFormatter(formatter)


def main():
    logger = logging.getLogger()
    client = HTTPClient(URL, logger)
    auth = AuthService(client, USERNAME, PASSWORD, logger)
    db = DBService(client, logger)
    parser = TableParser(logger)
    formatter = TableFormatter(logger)
    controller = MainController(auth, db, parser, formatter, logger)
    controller.run()

if __name__ == "__main__":
    main()