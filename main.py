from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json
import time

# URL категории товаров (например, "Чай")
category_url = "https://online.metro-cc.ru/category/chaj-kofe-kakao/chay"

# Функция для получения данных о товарах


def get_products(driver, url, city_id):
    driver.get(url)
    time.sleep(5)  # Даем время на загрузку страницы

    # Устанавливаем город
    driver.execute_script(
        f'window.localStorage.setItem("cityId", "{city_id}");')
    driver.refresh()
    time.sleep(5)  # Даем время на обновление страницы

    products = []

    # Парсинг товаров
    for product in driver.find_elements(By.CLASS_NAME, "product-card"):
        product_id = product.get_attribute("data-sku")
        name = product.find_element(
            By.CLASS_NAME, "product-card__title").text.strip()
        link = "https://online.metro-cc.ru" + \
            product.find_element(
                By.CLASS_NAME, "product-card__link").get_attribute("href")
        regular_price = product.find_element(
            By.CLASS_NAME, "product-card__price--regular").text.strip()
        promo_price = product.find_element(By.CLASS_NAME, "product-card__price--promo").text.strip(
        ) if product.find_elements(By.CLASS_NAME, "product-card__price--promo") else "Нет"
        brand = product.find_element(By.CLASS_NAME, "product-card__brand").text.strip(
        ) if product.find_elements(By.CLASS_NAME, "product-card__brand") else "Нет"

        # Проверка наличия товара
        availability = product.find_element(
            By.CLASS_NAME, "product-card__availability").text.strip()
        if "в наличии" in availability.lower():
            products.append({
                "id": product_id,
                "name": name,
                "link": link,
                "regular_price": regular_price,
                "promo_price": promo_price,
                "brand": brand
            })

    return products


# Получение данных для Москвы и Санкт-Петербурга
cities = {
    "Москва": "5e896c8e9c4a9e000187d5b5",
    "Санкт-Петербург": "5e896c8e9c4a9e000187d5b6"
}

all_products = []

# Настройки для Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Путь к ChromeDriver
service = Service('D:/projects/my_parser/driver/chromedriver.exe')

# Инициализация драйвера
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    for city, city_id in cities.items():
        print(f"Парсинг товаров для города {city}...")
        products = get_products(driver, category_url, city_id)
        all_products.extend(products)
finally:
    driver.quit()

# Сохранение данных в JSON
with open("metro_products.json", "w", encoding="utf-8") as jsonfile:
    json.dump(all_products, jsonfile, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в файл metro_products.json")
