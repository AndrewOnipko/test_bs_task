from utils.exceptions import AuthError, TokenError, ParseError, DBError

class MainController:
    def __init__(self, auth_service, db_service, parser, formatter, logger):
        self.auth_service = auth_service
        self.db_service = db_service
        self.parser = parser
        self.formatter = formatter
        self.logger = logger


    def run(self):
        try:
            self.db_service.token = self.auth_service.login()
            html_table = self.db_service.get_users_table()
            rows = self.parser.parse(html_table)

            if rows:
                headers = list(rows[0].keys())
                data = [list(row.values()) for row in rows]
                output = self.formatter.format(data, headers)
                print(output)
            else:
                self.logger.warning("Пустая таблица.")
        except (AuthError, TokenError) as e:
            self.logger.error(f"Ошибка авторизации: {e}", exc_info=True)
        except DBError as e:
            self.logger.error(f"Ошибка БД: {e}", exc_info=True)
        except ParseError as e:
            self.logger.error(f"Ошибка парсинга: {e}", exc_info=True)
        except Exception as e:
            self.logger.critical(f"Непредвиденная ошибка: {e}", exc_info=True)