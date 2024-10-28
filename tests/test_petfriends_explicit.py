from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import setup_edge, USER_EMAIL, USER_PASSWORD  # Импортируйте переменные


def test_show_all_pets(setup_edge):
    driver = setup_edge
    driver.get("https://petfriends.skillfactory.ru/login")
    wait = WebDriverWait(driver, 10)

    field_email = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    field_email.clear()
    field_email.send_keys(USER_EMAIL)

    field_pass = wait.until(EC.visibility_of_element_located((By.ID, "pass")))
    field_pass.clear()
    field_pass.send_keys(USER_PASSWORD)

    btn_submit = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']")))
    btn_submit.click()
    # Визуально , заголовок страницы станет видимым и проверяем его текст
    assert wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h1'))).text == "PetFriends"
    # Получаем элементы с карточками питомцев
    images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-img-top')))
    images = [img for img in images if img.is_displayed() and img.get_attribute('src') != '']
    names = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-title')))
    descriptions = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-deck .card-text')))
    # Получаем элементы с карточками питомцев
    try:
        for image, name, description in zip(images, names, descriptions):
            img_src = image.get_attribute('src')
            print(f"Источник изображения: '{img_src}'")
            assert img_src != '', "Источник изображения пуст"
            assert name.text != '', "Имя пустое"
            assert description.text != '', "Описание пустое"
            assert ', ' in description.text, "Неверный формат описания"
            parts = description.text.split(", ")
            assert len(parts) >= 2, "Описание должно состоять как минимум из двух частей"
            assert len(parts[0]) > 0, "Первая часть описания пуста"
            assert len(parts[1]) > 0, "Вторая часть описания пуста"

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

    print(f"Количество изображений: {len(images)}")
    print(f"Список имен питомцев: {['Питомец: ' + n.text for n in names]}")
    print(f"Список описаний: {['Описание: ' + d.text for d in descriptions]}")
