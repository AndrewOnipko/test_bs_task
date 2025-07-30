class AuthError(Exception):
    """Ошибка при аутентификации"""

    pass


class TokenError(Exception):
    """Ошибка при получении токена"""

    pass


class ParseError(Exception):
    """Ошибка при парсинге HTML таблицы"""

    pass
    

class DBError(Exception):
    """Ошибка при поиске таблицы"""

    pass