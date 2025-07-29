class MainController:
    def __init__(self, auth_service, db_service, parser, formatter):
        self.auth_service = auth_service
        self.db_service = db_service
        self.parser = parser
        self.formatter = formatter

    def run(self):
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