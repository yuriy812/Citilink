import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import setup_edge
from selenium.common.exceptions import TimeoutException


def test_search_example(setup_edge):
    driver = setup_edge
    driver.get('https://yourroom.ru/')
    wait = WebDriverWait(driver, 10)

    try:
        search_input = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-control"))
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys('Кухонные столы')

        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "form#mod-search-form > div > div:nth-of-type(2) > button > svg"))
        )

        search_button.click()
        print("Клик выполнен, ожидаю загрузки результатов...")

        product_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-card')))
        print(f'Количество карточек продукта: {len(product_cards)}')

        dict_descriptions = {}

        for card in product_cards:
            try:
                name_element = card.find_element(By.CSS_SELECTOR, 'div.product-card__title > a.link.link_default').text
                price_element = card.find_element(By.CSS_SELECTOR, '.product-card__price-new')

                name = name_element.strip()
                price = price_element.text.strip()

                if name and price:
                    dict_descriptions[name] = price

            except Exception as e:
                print(f"Ошибка при извлечении данных из карточки: {e}")

    except TimeoutException:
        print("Время ожидания истекло, элементы не были найдены.")

    finally:
        driver.quit()

    # Output and save data to file
    filename = "kitchen_tables_results.xlsx"  # Default filename
    print_descriptions(dict_descriptions)
    save_to_file(dict_descriptions, filename)


def print_descriptions(dict_descriptions):
    print("Список товаров:")
    for name, price in dict_descriptions.items():
        print(f"{name}: {price}")


def save_to_file(dict_descriptions, filename):
    if os.path.exists(filename):
        update = input(f"Файл {filename} уже существует. Хотите обновить? (y/n): ").lower()
        if update != 'y':
            filename = input("Введите новое имя файла: ") + ".xlsx"

    df = pd.DataFrame(dict_descriptions.items(), columns=["Название", "Цена"])
    df.to_excel(filename, index=False)
    print(f"Данные сохранены в файл: {filename}")


if __name__ == "__main__":
    test_search_example(setup_edge)
