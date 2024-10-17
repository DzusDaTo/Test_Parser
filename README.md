# Metro Product Parser

Этот проект представляет собой парсер, который извлекает данные о продуктах с сайта Metro (https://online.metro-cc.ru/). Парсер собирает информацию о товарах из заданной категории и для указанных городов, включая идентификатор товара, название, ссылку, обычную цену, акционную цену и бренд. Данные сохраняются в формате CSV, JSON и XLSX.

## Установка


Для работы парсера вам потребуется установить следующие зависимости:

- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [lxml](https://pypi.org/project/lxml/)
- [openpyxl](https://pypi.org/project/openpyxl/)

Вы можете установить все зависимости, используя файл `requirements.txt`. Для этого выполните следующую команду:

```bash
pip install -r requirements.txt
```
