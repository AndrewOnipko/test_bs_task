from utils.logger import simple_logger
from bs4 import BeautifulSoup

class DBService:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger
        self.token = None


    @simple_logger
    def get_users_table(self):
        """Получаем данные из таблицы"""
        
        try:
            params = {
            "route": "/sql",
            "db":"testDB",
            "table":"users",
            "pos":"0",
            "ajax_request": "true",
            "ajax_page_request": "true",
            "token": self.token
            }

            response = self.client.get('/index.php?route=/', params=params)
            json_data = response.json()
            html = json_data.get('message', '')

            return html
        
        except Exception as e:
            self.logger.error(f"Ошибка при получении таблицы: {e}")
            raise
        