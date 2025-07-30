from bs4 import BeautifulSoup
from utils.logger import simple_logger
from utils.exceptions import ParseError

class TableParser:
    def __init__(self, logger):
        self.logger = logger


    @simple_logger
    def parse(self, html: str):
        """Парсим переданный HTML текст и приводим в читаемый вид"""

        try:
            soup = BeautifulSoup(html, 'html.parser')
            rows = soup.find_all('tr')
            result = []

            for row in rows:
                id_td = row.find('td', attrs={"data-type": "int"})
                name_td = row.find('td', attrs={"data-type": "blob"})

                if not id_td or not name_td:
                    continue

                id_text = id_td.get_text(strip=True)
                name_text = name_td.get_text(strip=True)

                result.append({'id': id_text, 'name': name_text})

            if not result:
                raise ParseError("Таблица не содержит валидных строк.")

            return result

        except Exception as e:
            raise ParseError(f"Не удалось распарсить HTML таблицу: {e}") from e