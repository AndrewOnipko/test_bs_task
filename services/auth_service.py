from bs4 import BeautifulSoup
from utils.exceptions import AuthError, TokenError
from utils.logger import simple_logger

class AuthService:
    def __init__(self, client, username, password, logger):
        self.client = client
        self.username = username
        self.password = password
        self.logger = logger


    @simple_logger
    def login(self):
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
            error_msg = error_box.text.strip() if error_box else 'Неизвестная ошибка при логине'
            raise AuthError(error_msg)

        self.logger.info("Успешный вход в phpMyAdmin.")
        return token
            

    @simple_logger
    def get_token(self, html: str):
        """Получаем токен"""

        soup = BeautifulSoup(html, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})

        if not token_input or not token_input.get('value'):
            raise TokenError("Не удалось найти токен авторизации")

        return token_input['value']