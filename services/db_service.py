from utils.logger import simple_logger
from utils.exceptions import DBError

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
                "db": "testDB",
                "table": "users",
                "pos": "0",
                "ajax_request": "true",
                "ajax_page_request": "true",
                "token": self.token
            }

            response = self.client.get('/index.php?route=/', params=params)
            json_data = response.json()

            html = json_data.get('message')
            if not html:
                raise DBError("Ответ не содержит HTML таблицу.")

            return html

        except Exception as e:
            raise DBError(f"Не удалось получить таблицу: {e}") from e