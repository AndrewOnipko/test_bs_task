from bs4 import BeautifulSoup
from utils.logger import simple_logger

class AuthService:
    def __init__(self, client, username, password, logger):
        self.client = client
        self.username = username
        self.password = password
        self.logger = logger


    @simple_logger
    def login(self):
        try:
            response = self.client.get('/')
            html = response.text

            token = self.get_token(html)
            data = {
                'pma_username': self.username,
                'pma_password': self.password,
                'server': '1',
                'route': '/',
                'token': token
            }

            login_response = self.client.post('/index.php', data=data)
            login_html = login_response.text
            login_soup = BeautifulSoup(login_html, 'html.parser')

            if login_soup.find('form', {'id': 'login_form'}):
                error_box = login_soup.find('div', {'id': 'pma_errors'})
                error_msg = error_box.text.strip() if error_box else 'Неизвестная ошибка при попытке логина'
                raise Exception(f'Ошибка логина: {error_msg}')

            self.logger.info("Успешный вход в phpMyAdmin.")
            return token
        
        except Exception as e:
            self.logger.error(f"Ошибка при входе: {e}")
            raise
            

    @simple_logger
    def get_token(self, html):
        """Получаем токен"""

        soup = BeautifulSoup(html, 'html.parser')
        try:
            token_input = soup.find('input', {'name': 'token'})
            token = token_input['value'] if token_input else None
            return token
        
        except Exception as e:
            self.logger.error(f"Токен не найден, ошибка: {e}")
            raise