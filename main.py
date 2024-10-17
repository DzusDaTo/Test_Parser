import requests
from bs4 import BeautifulSoup
import csv
import json
from openpyxl import Workbook


# Функция для запроса HTML страницы
def get_page_content(city, category_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }
    url = f"{category_url}?city={city}"  # Подставляем нужный город в URL
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Ошибка при запросе для города {city}: {response.status_code}")
        return None


# Функция для парсинга товаров с одной страницы
def parse_products(city, category_url):
    html_content = get_page_content(city, category_url)

    if html_content is None:  # Проверка, что HTML контент был успешно получен
        return []  # Возвращаем пустой список, если произошла ошибка

    soup = BeautifulSoup(html_content, 'html.parser')

    # Ищем все карточки товара по селектору data-sku
    product_cards = soup.select('[data-sku]')

    # Список для хранения данных о товарах
    products = []

    # Итерируемся по карточкам товаров
    for card in product_cards:
        # Извлекаем необходимые данные
        product_id = card['data-sku']
        name_tag = card.select_one('.product-card-name__text')
        name = name_tag.get_text(strip=True) if name_tag else 'Неизвестно'
        link_tag = card.select_one('.product-card-photo__link')
        link = link_tag['href'] if link_tag else 'Неизвестно'
        regular_price_tag = card.select_one('.product-unit-prices__old .product-price__sum-rubles')
        promo_price_tag = card.select_one('.product-unit-prices__actual .product-price__sum-rubles')
        regular_price = regular_price_tag.get_text(strip=True).replace('\xa0', '') if regular_price_tag else 'Неизвестно'
        promo_price = promo_price_tag.get_text(strip=True).replace('\xa0', '') if promo_price_tag else 'Неизвестно'
        brand_tag = card.select_one('.product-card-name__text')
        if brand_tag:
            brand_full = brand_tag.get_text(strip=True)
            brand_words = brand_full.split()  # Разделяем строку на слова
            brand = ' '.join(brand_words[:2])  # Объединяем первые два слова
        else:
            brand = 'Неизвестно'

        # Сохраняем данные в словарь
        product_data = {
            'id': product_id,
            'name': name,
            'link': link,
            'regular_price': regular_price,
            'promo_price': promo_price,
            'brand': brand
        }

        products.append(product_data)

    # Пример вывода собранных данных
    for product in products:
        print(product)

    return products  # Возвращаем список собранных продуктов


# Функция для сохранения в CSV
def save_to_csv(products, filename):
    keys = products[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)


# Функция для сохранения в JSON
def save_to_json(products, filename):
    with open(filename, 'w', encoding='utf-8') as output_file:
        json.dump(products, output_file, ensure_ascii=False, indent=4)


# Функция для сохранения в XLSX
def save_to_xlsx(products, filename):
    wb = Workbook()
    ws = wb.active
    ws.append(list(products[0].keys()))  # Заголовки

    for product in products:
        ws.append(list(product.values()))

    wb.save(filename)


# Основная функция для парсинга товаров и экспорта данных
def main():
    category_url = "https://online.metro-cc.ru/category/chaj-kofe-kakao/kofe?from=under_search"  # Пример, нужно заменить на реальную категорию
    cities = ['moscow', 'saint-petersburg']  # Города, для которых собираем данные

    all_products = []

    # Парсим товары для каждого города
    for city in cities:
        products = parse_products(city, category_url)
        all_products.extend(products)  # Объединяем товары из всех городов

    # Сохраняем данные в файлы
    if all_products:  # Проверяем, что товары собраны
        save_to_csv(all_products, 'metro_products.csv')
        save_to_json(all_products, 'metro_products.json')
        save_to_xlsx(all_products, 'metro_products.xlsx')
        print("Данные успешно сохранены.")
    else:
        print("Не удалось собрать данные о товарах.")


if __name__ == "__main__":
    main()
